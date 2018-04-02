# Copyright (c) 2013, Nick Stevens <nick@bitcurry.com>
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the <organization> nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

'''
Generate a filtered set of dates between a start date and an end date where
filters can be based on day of the week, day of the month, month, or relative
dates (i.e. first Tuesday, 2nd Wednesday, etc). The increment between
occurrences can also be adjusted - for example, every 2 days, 3 months, etc.
'''
import calendar as cal
from datetime import date

# Shortcuts for common functions
_toord = date.toordinal
_fromord = date.fromordinal

class Generator:

    '''
    Base class for `Generator` types - classes that generate dates at a
    specified interval. By default generates days at a given increment.
    '''

    def __init__(self, start, stop, inc):
        self.startdate = start if start is not None else date.today()
        self.stopdate = stop if stop is not None else date.max
        self.inc = inc
        
    def __iter__(self):
        cur = _toord(self.startdate)
        stopord = _toord(self.stopdate)
        inc = self.inc
        while cur <= stopord:
            yield cur
            cur += inc

    def filter(self, receiver):
        return receiver._attach(self)


class DayIncrementGenerator(Generator):

    '''
    Generates days at a given interval (1 by default).
    '''

    def __init__(self, start=None, stop=None, inc=1):
        super().__init__(start, stop, inc)


class WeekIncrementGenerator(Generator):

    '''
    Generates days at a given weekly interval (1 by default).
    '''

    def __init__(self, start=None, stop=None, inc=1):
        super().__init__(start, stop, inc*7)


class MonthIncrementGenerator(Generator):

    '''
    Generates days at a given monthly interval (1 by default).

    If start day is 29th, 30th, or 31st of the month, this class remembers the
    start day and will pick the latest day in the month if the selected day is
    not available.

    For example: the start day is January 30, 2011 with an interval of 1 month.
    The next day returned will be February 28, followed by March 30, and so on.
    '''

    def __init__(self, start=None, stop=None, inc=1):
        super().__init__(start, stop, inc)

    def __iter__(self):
        cur = _toord(self.startdate)
        day = self.startdate.day
        month = self.startdate.month
        year = self.startdate.year
        _, endday = cal.monthrange(curyear, curmonth)
        monthend = date(curyear, curmonth, endday)
        endord = monthend.toordinal()
        stopord = self.stopdate.toordinal()
        inc = self.inc
        while cur <= stopord:
            if cur <= endord:
                yield cur
                cur += 1
            else:
                curmonth += inc
                if curmonth > 12:
                    div, mod = divmod(curmonth, 12)
                    curmonth = mod + 1
                    curyear += div
                _, endday = cal.monthrange(curyear, curmonth)
                monthend = date(curyear, curmonth, endday)
                endord = monthend.toordinal()
                monthstart = date(curyear, curmonth, 1)
                cur = monthstart.toordinal()
class YearlyGenerator(Generator):

    '''
    Generates all days for each <n> years (1 by default).
    '''

    def __init__(self, start=None, stop=None, inc=1):
        super().__init__(start, stop, inc)

    def __iter__(self):
        cur = self.startdate.toordinal()
        curyear = self.startdate.year
        yearstart = date(curyear, 1, 1)
        yearend = date(curyear, 12, 31)
        endord = yearend.toordinal()
        stopord = self.stopdate.toordinal()
        inc = self.inc
        while cur <= stopord:
            if cur <= endord:
                yield cur
                cur += 1
            else:
                curyear += inc
                yearend = date(curyear, 12, 31)
                endord = yearend.toordinal()
                yearstart = date(curyear, 1, 1)
                cur = yearstart.toordinal()







class Filter:

    def filter(self, receiver):
        return receiver._attach(self)

    def _attach(self, source):
        self.source = source
        return self

    def _check_source(self):
        if not self.source:
            raise ValueError("Must connect a source to filter")

    @classmethod
    def rangetype(parent, cls):
        def _init_(self, *args):
            self.source = None
            self.include = frozenset(args)
            if not self.include.issubset(frozenset(cls._all_values_)):
                raise ValueError("Values must be in " + str(tuple(cls._all_values_)))
        def _iter_(self):
            self._check_source()
            for item in self.source:
                if cls._include_if_(item) in self.include:
                    yield item
        cls.__init__ = _init_
        cls.__iter__ = _iter_
        return cls


@Filter.rangetype
class WeekdayFilter(Filter):
    '''
    Limits values from source to weekdays (0[mon]-6[sun]) given
    '''
    _all_values_ = range(0, 7)
    _include_if_ = lambda d: date.fromordinal(d).weekday()


@Filter.rangetype
class MonthFilter(Filter):
    '''
    Limits values from source to months (1-12) given
    '''
    _all_values_ = range(1, 13)
    _include_if_ = lambda d: date.fromordinal(d).month
       

@Filter.rangetype
class MonthDayFilter(Filter):
    '''
    Limits values from source to days of the month (1-31) given
    '''
    _all_values_ = range(1, 32)
    _include_if_ = lambda d: date.fromordinal(d).day


def compile(expr):
    "Compiles a date expression"
    pass




if __name__ == '__main__':
    main()
