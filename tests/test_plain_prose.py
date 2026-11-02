"""Checks on tools/plain_prose.py: running text loses its bullets, real lists keep theirs."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from plain_prose import plain_prose, sentences  # noqa: E402


def test_bullet_with_three_sentences_becomes_three_paragraphs():
    text = "* Python ran both lines. Only the last shows. Wrap each in `print()`."
    assert plain_prose(text) == "Python ran both lines.\n\nOnly the last shows.\n\nWrap each in `print()`."


def test_one_sentence_bullet_loses_its_bullet():
    assert plain_prose("* A format code changes the display.") == "A format code changes the display."


def test_list_under_a_colon_keeps_its_bullets():
    text = "The desk holds three things:\n* A bond.\n* A loan.\n* Cash."
    assert plain_prose(text) == text


def test_list_under_a_bold_label_keeps_its_bullets():
    text = "**Observations**\n* The first rises.\n* The second falls."
    assert plain_prose(text) == text


def test_fragments_keep_their_bullets():
    text = "* `print`: show something\n* `len`: count the items"
    assert plain_prose(text) == text


def test_two_sentence_bullets_with_no_lead_in_become_paragraphs():
    assert plain_prose("* First.\n* Second.\n\n**Excel side by side.** Same.") == "First.\n\nSecond.\n\n**Excel side by side.** Same."


def test_plain_paragraph_splits_and_bold_lead_in_stays_with_first_sentence():
    text = "**Excel side by side.** It adds. It also rounds."
    assert plain_prose(text) == "**Excel side by side.** It adds.\n\nIt also rounds."


def test_periods_inside_code_numbers_and_abbreviations_do_not_split():
    assert sentences("Use `a. B` here.") == ["Use `a. B` here."]
    assert sentences("The price is 98.50 today.") == ["The price is 98.50 today."]
    assert sentences("Ratios, e.g. Attr64, matter.") == ["Ratios, e.g. Attr64, matter."]


def test_no_ends_a_sentence_unless_a_number_follows():
    assert sentences("No. That red block is a traceback.") == ["No.", "That red block is a traceback."]
    assert sentences("See Item No. 5 here.") == ["See Item No. 5 here."]


def test_a_quoted_prompt_stays_whole():
    line = "For example: 'I have a list of prices. Write a loop that totals them.'"
    assert sentences(line) == [line]


def test_structure_is_left_alone():
    for text in ("## 1.1 Variables. Then more", "> STORY: One. Two.", "Q. The desk bought it. How much?", "1. Run it. Then read it.",
                 "| a. B | c |", "```\nprint('One. Two.')\n```", "<table align=\"left\">"):
        assert plain_prose(text) == text


def test_title_cell_is_left_alone():
    text = "Week 1. A title.\n\n> This course is educational content created in a personal capacity. Nothing here."
    assert plain_prose(text) == text


def test_running_it_twice_changes_nothing():
    once = plain_prose("* One. Two.\n\nThree. Four.\n\nHere are the items:\n* Alpha.\n* Beta.")
    assert plain_prose(once) == once
