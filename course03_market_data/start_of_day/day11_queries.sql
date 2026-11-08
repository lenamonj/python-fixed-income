-- queries.sql: the day 11 queries on the course's synthetic book. Values go in as ? parameters.

-- four columns of every bond
SELECT cusip, issuer, sector, oas FROM holdings;

-- WHERE: one sector, spreads above a level (parameters: 'Energy', 200)
SELECT cusip, issuer, oas FROM holdings WHERE sector = ? AND oas > ?;

-- ORDER BY and LIMIT: the largest positions by market value (parameter: 5)
SELECT cusip, issuer, market_value FROM holdings ORDER BY market_value DESC LIMIT ?;

-- dates are ISO text, so < compares in date order (parameter: '2030-01-01')
SELECT cusip, issuer, maturity FROM holdings WHERE maturity < ? ORDER BY maturity;

-- GROUP BY: bonds, market value in dollars, and simple average OAS in bp by sector
SELECT sector, COUNT(*) AS bonds, SUM(market_value) AS market_value, AVG(oas) AS avg_oas
FROM holdings GROUP BY sector ORDER BY market_value DESC;

-- HAVING: sectors with at least this many bonds (parameter: 20)
SELECT sector, COUNT(*) AS bonds FROM holdings GROUP BY sector HAVING COUNT(*) >= ? ORDER BY sector;

-- market-value weighted OAS in bp by sector
SELECT sector, SUM(oas * market_value) / SUM(market_value) AS weighted_oas, AVG(oas) AS avg_oas
FROM holdings GROUP BY sector;
