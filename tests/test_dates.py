import datetime as dt

import pytest

from iran_bourse_mcp import dates


@pytest.mark.parametrize(
    ("greg", "jalali"),
    [
        ((2026, 11, 3), (1405, 8, 12)),
        ((2026, 10, 28), (1405, 8, 6)),
        ((2026, 3, 21), (1405, 1, 1)),
        ((2025, 3, 21), (1404, 1, 1)),
        ((2024, 3, 20), (1403, 1, 1)),
    ],
)
def test_jalali_known_pairs(greg, jalali):
    assert dates.gregorian_to_jalali(*greg) == jalali
    assert dates.jalali_to_gregorian(*jalali) == greg


def test_every_day_roundtrips_over_a_decade():
    day = dt.date(2018, 1, 1)
    while day < dt.date(2028, 1, 1):
        j = dates.gregorian_to_jalali(day.year, day.month, day.day)
        assert dates.jalali_to_gregorian(*j) == (day.year, day.month, day.day)
        day += dt.timedelta(days=1)


@pytest.mark.parametrize("text", ["2026-11-03", "20261103", "1405/08/12", "14050812", "۱۴۰۵/۰۸/۱۲", "1405-8-12"])
def test_parse_date_accepts_both_calendars(text):
    assert dates.parse_date(text) == 20261103


@pytest.mark.parametrize("bad", ["", "abc", "2026-13-01", "1405/13/40", "2026/02/30", "1405/07/31", "1405/12/30"])
def test_parse_date_rejects_garbage(bad):
    with pytest.raises(dates.DateError):
        dates.parse_date(bad)


def test_formatting():
    assert dates.fmt_date(20261103) == "2026-11-03"
    assert dates.jdate(20261103) == "1405/08/12"
    assert dates.fmt_time(90013) == "09:00:13"
    assert dates.fmt_time(123000) == "12:30:00"
    assert dates.fmt_date(0) is None


@pytest.mark.parametrize(
    ("text", "expected"),
    [("09:30", 93000), ("09:30:15", 93015), ("0930", 93000), ("093015", 93015), ("12:30", 123000)],
)
def test_parse_time(text, expected):
    assert dates.parse_time(text) == expected


def test_parse_time_rejects_invalid():
    with pytest.raises(dates.DateError):
        dates.parse_time("25:00")


def test_session_hours():
    # 2026-11-04 is a Wednesday (trading); Thursday and Friday are not.
    assert dates.is_session_hours(dt.datetime(2026, 11, 4, 10, 0))
    assert not dates.is_session_hours(dt.datetime(2026, 11, 4, 13, 0))
    assert not dates.is_session_hours(dt.datetime(2026, 11, 5, 10, 0))
    assert not dates.is_session_hours(dt.datetime(2026, 11, 6, 10, 0))


def test_tehran_offset():
    assert dates.tehran_now(dt.datetime(2026, 11, 4, 6, 30)) == dt.datetime(2026, 11, 4, 10, 0)
