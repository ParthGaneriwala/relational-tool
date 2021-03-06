import datetime
import keyword
import re
from typing import Union, Set, Any, Callable, Type, Optional
from dataclasses import dataclass

RELATION_NAME_REGEXP = re.compile(r'^[_a-z][_a-z0-9]*$', re.IGNORECASE)
_date_regexp = re.compile(
        r'^([0-9]{1,4})(\\|-|/)([0-9]{1,2})(\\|-|/)([0-9]{1,2})$'
    )
CastValue = Optional[Union[str, int, float, 'Rdate']]


def guess_type(value: str) -> Set[Union[Callable[[Any], Any], Type['Rdate']]]:
    r: Set[Union[Callable[[Any], Any], Type['Rdate']]] = {str}
    if _date_regexp.match(value) is not None:
        r.add(Rdate)

    try:
        int(value)
        r.add(int)
    except ValueError:
        pass

    try:
        float(value)
        r.add(float)
    except ValueError:
        pass
    return r


def cast(value: str, guesses: Set) -> CastValue:
    if int in guesses:
        return int(value)
    if Rdate in guesses:
        return Rdate.create(value)
    if float in guesses:
        return float(value)
    return value


@dataclass(frozen=True)
class Rdate:
    '''Represents a date'''
    year: int
    month: int
    day: int

    @property
    def intdate(self) -> datetime.date:
        return datetime.date(self.year, self.month, self.day)

    @property
    def weekday(self) -> int:
        return self.intdate.weekday()

    @staticmethod
    def create(date: str) -> 'Rdate':
        '''date: A string representing a date YYYY-MM-DD'''
        r = _date_regexp.match(date)
        if not r:
            raise ValueError(f'{date} is not a valid date')

        year = int(r.group(1))
        month = int(r.group(3))
        day = int(r.group(5))
        return Rdate(year, month, day)

    def __str__(self):
        return self.intdate.__str__()

    def __ge__(self, other):
        return self.intdate >= other.intdate

    def __gt__(self, other):
        return self.intdate > other.intdate

    def __le__(self, other):
        return self.intdate <= other.intdate

    def __lt__(self, other):
        return self.intdate < other.intdate


def is_valid_relation_name(name: str) -> bool:
    '''Checks if a name is valid for a relation.
    Returns boolean'''
    return re.match(RELATION_NAME_REGEXP, name) != None and not keyword.iskeyword(name)
