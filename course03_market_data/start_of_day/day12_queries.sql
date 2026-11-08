-- queries.sql: the day's queries, run with ? parameters from Python (marketdata.run_query)

-- every holding with its issuer and its rating's bucket and grade (many to one, twice)
SELECT h.cusip, h.ticker, i.issuer, i.country, h.rating, r.bucket, r.grade, h.market_value
FROM holdings AS h
JOIN issuers AS i ON h.ticker = i.ticker
JOIN ratings AS r ON h.rating = r.rating;

-- trades and principal by grade: trades to holdings on cusip, then to ratings
SELECT r.grade, COUNT(*) AS trades, SUM(t.principal) AS principal
FROM trades AS t
JOIN holdings AS h ON t.cusip = h.cusip
JOIN ratings AS r ON h.rating = r.rating
GROUP BY r.grade
ORDER BY r.grade;

-- benchmark bonds the book does not hold
SELECT b.cusip, b.ticker, b.sector, b.weight_pct
FROM benchmark AS b
LEFT JOIN holdings AS h ON b.cusip = h.cusip
WHERE h.cusip IS NULL;

-- keys that repeat: a ticker with more than one bond in the benchmark
SELECT ticker, COUNT(*) AS bonds
FROM benchmark
GROUP BY ticker
HAVING COUNT(*) > 1
ORDER BY bonds DESC, ticker;


-- one tenor between two dates; dates are ISO text, and BETWEEN includes both ends
SELECT date, yield_pct
FROM treasury
WHERE tenor = ? AND date BETWEEN ? AND ?
ORDER BY date;

-- the daily change in bp, from the previous row of the same tenor
SELECT date, yield_pct,
       (yield_pct - LAG(yield_pct) OVER (ORDER BY date)) * 100 AS change_bp
FROM treasury
WHERE tenor = ?
ORDER BY date;

-- the last observation of each month, labelled by its own date
SELECT date, yield_pct FROM (
    SELECT date, yield_pct,
           ROW_NUMBER() OVER (PARTITION BY substr(date, 1, 7) ORDER BY date DESC) AS row_in_month
    FROM treasury
    WHERE tenor = ?
) WHERE row_in_month = 1
ORDER BY date;
