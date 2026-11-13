"""Every notebook follows one standard, so the series reads as one piece of work. A course joins COURSES at its pass.

The standard itself is in COURSE1_SPEC.md under "The notebook standard". Jeff, 2026-11-02: "assure there is a
standardization we are following otherwise it shows we are not professional".
"""
import re
from pathlib import Path

import nbformat
import pytest

REPO = Path(__file__).resolve().parents[1]
COURSES = ["course01_python_foundations", "course02_bond_math", "course03_market_data", "course04_machine_learning", "course05_advanced_ml"]
TEACHING = sorted(
    path for course in COURSES for path in (REPO / course).glob("week*/day*/*.ipynb")
    if not path.stem.endswith("_solutions")
)
SMALL_WORDS = {"a", "an", "and", "as", "at", "but", "by", "for", "in", "nor", "of", "on", "or", "per", "the", "to", "vs"}
LIBRARY_NAMES = {"os", "csv", "pathlib", "merge", "concat", "apply", "pandas", "plotly", "pivot_table", "pytest", "bp", "sqlite3", "t-SNE"}
INSTALL_HEADINGS = {"Before You Start: Install the Libraries", "Before You Start: Nothing to Install"}
LEAD_IN = "By the end of this notebook, you can:"
WITHIN_TITLE = re.compile(r"\b(with|from|into|over)\b")
# Code spans may teach f-strings, so a format code is only a fault in prose. A dictionary lookup is a fault anywhere.
CODE_TEXT = re.compile(r"```.*?```|`[^`\n]*`|<code>.*?</code>|\$\$.*?\$\$", re.S)
UNFILLED = re.compile(r"\{[A-Za-z_]\w*(?:\[|\(|!r|:[,+.0-9]*[a-z%]\})")
UNFILLED_LOOKUP = re.compile(r"\{[A-Za-z_]\w*\[['\"]")
# Jeff 2026-11-07: from Course 4 on, notebooks follow his sample template; a day joins this set when rebuilt
NEW_STYLE = {"14_shap_values", "13_resampling_smote_and_class_weights", "12_feature_engineering_on_financial_ratios", "11_randomized_search_and_honest_tuning", "10_case_study_boosting_on_credit_card_default", "09_lightgbm_and_stacking", "08_xgboost_regularization_and_early_stopping", "07_gradient_boosting_from_residuals", "06_adaboost", "05_case_study_bagging_and_the_spread_cross_section", "04_impurity_and_permutation_importance", "03_random_forests", "02_bagging_and_out_of_bag_scores", "01_tree_instability_and_the_bootstrap", "course4_capstone", "14_pca_and_t_sne", "13_hierarchical_clustering_and_cluster_profiling", "12_scaling_and_k_means", "11_dated_data_and_walk_forward_validation", "10_case_study_credit_card_default", "09_decision_trees", "08_roc_curves_and_choosing_a_threshold", "07_confusion_matrix_precision_and_recall", "06_logistic_regression_and_odds", "05_case_study_ridge_lasso_and_the_spread_cross_section", "04_regression_assumptions_and_log_spreads", "03_coefficients_p_values_and_multicollinearity", "01_the_ml_workflow_and_simple_regression", "02_multiple_regression_and_dummy_variables", "0_start_here", "01_python_for_fixed_income_intro",
             "01_part2_python_for_fixed_income_intro", "02_files_and_folders",
             "03_debugging", "04_classes_a_bond_object", "05_case_study_a_small_portfolio",
             "06_numpy", "06_part2_numpy",
             "07_pandas_series_and_dataframes", "07_part2_pandas_series_and_dataframes",
             # the rest of Course 1, added up front (2026-11-07) so two build teams never edit this line at once
             "08_pandas_combining_and_loading", "08_part2_pandas_combining_and_loading",
             "09_case_study_first_look_at_the_data", "10_case_study_joining_the_tables",
             "11_visualization", "12_visualization_more", "13_exploratory_data_analysis",
             "14_case_study_treasury_yields", "15_case_study_trade_blotter",
             "16_case_study_consumer_credit", "17_analyzing_text", "17_part2_analyzing_text",
             "18_case_study_statement_sentiment", "19_from_notebook_to_module", "course1_project",
             # Course 2 as redesigned
             "01_time_value_of_money", "02_cash_flows_and_price_from_yield",
             "03_the_price_yield_relationship", "04_yield_from_price", "05_case_study_a_new_issue_calendar",
             "06_dates_and_coupon_schedules", "07_day_counts_and_accrued_interest", "08_clean_and_dirty_price",
             "09_duration_and_dv01", "10_case_study_convexity_and_the_september_book",
             "11_treasury_curve_interpolation", "12_spread_over_the_curve",
             "13_spread_duration_and_dts", "14_portfolio_aggregation_and_scenarios", "course2_capstone",
             # Course 3 as redesigned, a stem added as each notebook is pushed
             "01_apis_keys_and_secrets", "02_json_and_the_fred_api", "03_market_calendars_and_cleaning",
             "04_resampling_and_the_as_of_value", "05_case_study_the_market_dataset",
             "06_changes_in_bp_and_percent", "07_rolling_windows_and_volatility",
             "09_slopes_and_butterflies", "10_case_study_three_years_of_curve_and_spreads",
             "11_sql_with_sqlite3", "12_sql_joins_and_time_series", "13_working_with_an_ai_assistant",
             "14_the_daily_market_snapshot", "course3_capstone",
             "08_z_scores_and_percentile_ranks"}
# A course mid-pass joins notebook by notebook: each rebuilt notebook is held to the standard from its release
IN_PASS = ["course05b_time_series"]
TEACHING += sorted(
    path for course in IN_PASS for path in (REPO / course).glob("week*/day*/*.ipynb")
    if path.stem in NEW_STYLE
)


def ids(path: Path) -> str:
    return path.stem


def is_project(path: Path) -> bool:
    return path.stem == "course1_project" or path.stem.endswith("_capstone")


def in_course_1(path: Path) -> bool:
    return "course01" in str(path)


def course_number(path: Path) -> int:
    return int(re.match(r"course(\d+)", path.relative_to(REPO).parts[0]).group(1))


def is_case_study(path: Path) -> bool:
    return "case_study" in path.stem


def new_style_ml(path: Path) -> bool:
    """Course 4 on, rebuilt on Course 4 Day 1's ladder (Jeff's sample template): case studies and the capstone too."""
    return path.stem in NEW_STYLE and course_number(path) >= 4


def number(path: Path) -> int:
    return int(re.match(r"\d+", path.stem).group())


def markdown(path: Path) -> list[str]:
    return [cell.source for cell in nbformat.read(path, as_version=4).cells if cell.cell_type == "markdown"]


def headings(path: Path, level: int) -> list[str]:
    return re.findall(rf"^{'#' * level} (.+)$", "\n".join(markdown(path)), re.M)


def expected_label(path: Path) -> str:
    week = re.search(r"week(\d)", str(path)).group(1)
    day, part = re.search(r"day(\d)(_part2)?", str(path).replace("\\", "/").split("/week")[1]).groups()
    if "_part" in path.stem or "Part 1" in markdown(path)[1].split("\n")[0]:
        return f"Week {week}, Day {day}, Part {2 if part else 1}."
    return f"Week {week}, Day {day}."


def title_cased(heading: str) -> bool:
    words = re.sub(r"`[^`]*`", "", heading).replace(":", " ").split()
    for word in words:
        bare = word.strip("?.,()'")
        if bare.lower() in SMALL_WORDS or bare in LIBRARY_NAMES or not bare or not bare[0].isalpha():
            continue
        if bare[0].islower():
            return False
    return True


def test_the_four_splits_are_in_place():
    stems = {path.stem for path in TEACHING}
    assert {"06_part2_numpy", "07_part2_pandas_series_and_dataframes", "08_part2_pandas_combining_and_loading",
            "17_part2_analyzing_text"} <= stems


@pytest.mark.parametrize("path", TEACHING, ids=ids)
def test_title_is_title_case(path):
    assert title_cased(headings(path, 1)[0]) and not WITHIN_TITLE.search(headings(path, 1)[0])


@pytest.mark.parametrize("path", TEACHING, ids=ids)
def test_no_builder_placeholder_reaches_the_student(path):
    for cell in markdown(path):
        prose = CODE_TEXT.sub("", cell)
        assert not UNFILLED.search(prose) and not UNFILLED_LOOKUP.search(cell), cell[:200]


@pytest.mark.parametrize("path", TEACHING, ids=ids)
def test_each_notebook_has_its_solutions_and_overview(path):
    assert path.with_name(path.stem + "_solutions.ipynb").exists()
    assert path.with_name(path.stem + "_overview.pdf").exists()


@pytest.mark.parametrize("path", TEACHING, ids=ids)
def test_opening(path):
    cells = nbformat.read(path, as_version=4).cells
    title = cells[1].source
    assert title.startswith("# ")
    assert expected_label(path) in title
    assert "educational content created in a personal capacity" in title
    assert "colab.research.google.com" in title


# Jeff, 2026-11-07: the new style has no install cell; requirements.txt and Colab cover it
@pytest.mark.parametrize("path", [p for p in TEACHING if p.stem not in NEW_STYLE], ids=ids)
def test_first_section_is_the_install_section(path):
    assert headings(path, 2)[0] in INSTALL_HEADINGS


@pytest.mark.parametrize("path", [p for p in TEACHING if not is_project(p)], ids=ids)
def test_sections_carry_the_notebook_number(path):
    for heading in headings(path, 2) + headings(path, 3):
        found = re.match(r"(\d+)\.(\d+)", heading)
        if found:
            assert int(found.group(1)) == number(path), heading
            assert found.group(2) != "0", heading


@pytest.mark.parametrize("path", TEACHING, ids=ids)
def test_headings_are_title_case(path):
    wrong = [heading for heading in headings(path, 2) + headings(path, 3) + headings(path, 4)
             if not heading.startswith("Exercise") and not title_cased(heading)]
    assert wrong == []


@pytest.mark.parametrize("path", [p for p in TEACHING if not is_project(p)], ids=ids)
def test_ending(path):
    level_two = [heading for heading in headings(path, 2) if heading != "Tidying Up"]
    assert level_two[-3:] == ["You Can Now", "Exercises", "Congratulations!"]
    if is_case_study(path) and in_course_1(path):
        assert level_two[-4] == "Summary"


@pytest.mark.parametrize("path", [p for p in TEACHING if is_project(p)], ids=ids)
def test_project_ends_on_the_closing(path):
    assert headings(path, 2)[-1] == "Congratulations!"


@pytest.mark.parametrize("path", TEACHING, ids=ids)
def test_last_cell_is_the_closing(path):
    last = nbformat.read(path, as_version=4).cells[-1]
    assert last.cell_type == "markdown" and last.source.startswith("## Congratulations!")


@pytest.mark.parametrize("path", [p for p in TEACHING if not is_project(p)], ids=ids)
def test_you_can_now_is_a_list_under_its_lead_in(path):
    cell = next(source for source in markdown(path) if source.startswith("## You Can Now"))
    assert LEAD_IN in cell
    assert len(re.findall(r"^\* ", cell, re.M)) >= 3


@pytest.mark.parametrize("path", [p for p in TEACHING if not is_project(p)], ids=ids)
def test_last_exercise_is_an_ai_check(path):
    exercises = [heading for heading in headings(path, 3) if heading.startswith("Exercise")]
    assert exercises[-1].endswith(": AI check")
    assert all(re.fullmatch(r"Exercise \d+(: AI check)?", heading) for heading in exercises)


@pytest.mark.parametrize("path", [p for p in TEACHING if is_case_study(p) and not new_style_ml(p)], ids=ids)
def test_case_study_opens_with_the_problem_definition(path):
    assert "Problem Definition" in headings(path, 2)
    level_three = headings(path, 3)
    start = level_three.index("Context")
    assert level_three[start:start + 4] == ["Context", "Objective", "The Data", "How We Will Work"]


@pytest.mark.parametrize("path", [p for p in TEACHING if not is_case_study(p) and not is_project(p) and not new_style_ml(p)],
                         ids=ids)
def test_hands_on_notebook_has_a_scenario_before_its_first_section(path):
    sources = markdown(path)
    # Courses 1 to 3 as redesigned: no install section, so the scenario sits between the title and section 1
    if path.stem in NEW_STYLE and course_number(path) <= 3:
        # sources[0] is the banner, sources[1] the title; a scenario cell sits before the first numbered section
        first_section = next(i for i, source in enumerate(sources) if re.match(rf"## {number(path)}\.\d", source))
        assert sources[1].startswith("# ") and first_section >= 3, "no scenario between the title and section 1"
        return
    first_section = next(i for i, source in enumerate(sources) if re.match(rf"## {number(path)}\.\d", source))
    install = next(i for i, source in enumerate(sources) if source.startswith("## Before You Start"))
    assert first_section - install >= 2, "no scenario between the install section and section 1"


# Course 4 on, as redesigned: Day 1's ladder. The title, then # Problem Statement with Business Context, Objectives
# and Data Dictionary; unnumbered headings; no install section and no Excel; # Wrapping Up last of the # topics, over
# the ending that test_ending, test_last_exercise_is_an_ai_check and test_predict_cells_run_from_day_5 check (the
# capstone ends on its closing: test_project_ends_on_the_closing).
@pytest.mark.parametrize("path", [p for p in TEACHING if new_style_ml(p)], ids=ids)
def test_new_style_ml_follows_day_1s_ladder(path):
    sources = markdown(path)
    # sources[0] is the banner, sources[1] the title
    assert sources[1].startswith("# ") and sources[2].startswith("# Problem Statement")
    assert re.findall(r"^## (.+)$", "\n".join(sources[2:]), re.M)[:3] == ["Business Context", "Objectives", "Data Dictionary"]
    assert [h for h in headings(path, 1) + headings(path, 2) + headings(path, 3) if re.match(r"\d+\.\d", h)] == []
    assert [h for h in headings(path, 2) if h.startswith("Before You Start")] == []
    assert not re.search(r"\bExcel\b", "\n".join(sources))
    if not is_project(path):
        assert headings(path, 1)[-1] == "Wrapping Up"


@pytest.mark.parametrize("path", [p for p in TEACHING if not is_project(p)], ids=ids)
def test_questions_are_q_lines_never_bold(path):
    text = "\n".join(markdown(path))
    assert re.findall(r"^\*\*[^*\n]*\?\*\*$", text, re.M) == []
    assert len(re.findall(r"^Q\. ", text, re.M)) >= 8


@pytest.mark.parametrize("path", [p for p in TEACHING if not is_project(p) and (not in_course_1(p) or number(p) >= 5)], ids=ids)
def test_predict_cells_run_from_day_5(path):
    found = re.findall(r"^\*\*Predict (\d+)\*\*$", "\n".join(markdown(path)), re.M)
    assert len(found) >= 3
    assert [int(n) for n in found] == list(range(1, len(found) + 1))


# Jeff 2026-11-07: no Excel from Course 4 on
@pytest.mark.parametrize("path", [p for p in TEACHING if not is_project(p) and course_number(p) < 4], ids=ids)
def test_excel_comparisons_use_one_label(path):
    text = "\n".join(markdown(path))
    assert "**Excel side by side.**" in text
    assert "**Compared with Excel" not in text


@pytest.mark.parametrize("path", TEACHING, ids=ids)
def test_stories_sit_in_a_cell_of_their_own(path):
    for source in markdown(path):
        if re.search(r"^> \*{0,2}STORY", source, re.M):
            assert all(line.startswith(">") or not line.strip() for line in source.split("\n")), source[:80]
