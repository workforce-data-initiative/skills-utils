from skills_utils.time import dates_in_range
from datetime import date

def test_dates_in_range():
    start = date(2012, 5, 29)
    end = date(2012, 6, 3)
    assert dates_in_range(start, end) == [
        date(2012, 5, 29),
        date(2012, 5, 30),
        date(2012, 5, 31),
        date(2012, 6, 1),
        date(2012, 6, 2),
    ]
