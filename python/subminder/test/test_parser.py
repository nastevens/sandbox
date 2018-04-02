import unittest
import re
import collections
import subminder.parser as parser
from subminder.parser import DateRepeat, Date, Generator

# "Test simple days of the month", tuple(str(x) for x in range(1,32)) ),
# "Test days of the month with 'st', 'nd', 'rd', or 'th' appended",
# "Test years 2000 to 2999", tuple(str(x) for x in range(2000, 3000)),
# "Test months",
# "Test compound statements using 'and'",
# "Test limiters using 'in'",
# "Test ranges using 'through'",
# "Test ranges using '-'",
# "Test relative days of the month using <1st, 2nd, etc> <day of week>",
# "Test relative days of the month with 'of' or 'in' to limit months",
# "Test start dates",
# "Test end dates",

def permute_case(input_string):
    '''
    Returns all permutations of upper and lower case for a string
    '''
    if not input_string:
        yield ""
    else:
        first = input_string[:1]
        if first.lower() == first.upper():
            for sub_case in permute_case(input_string[1:]):
                yield first + sub_case
        else:
            for sub_case in permute_case(input_string[1:]):
                yield first.lower() + sub_case
                yield first.upper() + sub_case


def permute_optional(input_string):
    '''
    Given a string with optional components returns all combinations of 
    characters possible within those options.

    Optional types:
        [] - options expanded one character at a time starting from the 
             right-most character i.e. ju[st] => just, jus, and ju
        {} - option is 'all or nothing' i.e. {option}al => optional, al

    Example:
        "{every }5 da[ys]" returns ['every 5 days', 'every 5 day', 'every 5 da',
                                    '5 days', '5 day', '5 da']
    '''

    regexpr = r'\[(?P<PARTIAL>.+?)]|\{(?P<COMPLETE>.+?)}|(?P<TEXT>[^[{]+)'
    pattern = re.compile(regexpr)
    scanner = pattern.scanner(input_string)
    Token = collections.namedtuple('Token', ['type', 'value'])
    token_list = [Token(m.lastgroup, m.groupdict()[m.lastgroup]) 
                     for m in iter(scanner.match, None)]
    for val in _permute_recursive('', token_list):
        yield val

def _permute_recursive(base_string, token_list):
    if not token_list:
        yield base_string
    else:
        tok = token_list[0]
        rest = token_list[1:]
        if tok.type == 'PARTIAL':
            string = tok.value
            while string:
                for val in _permute_recursive(base_string + string, rest):
                    yield val
                string = string[:-1]
            for val in _permute_recursive(base_string, rest):
                yield val
        elif tok.type == 'COMPLETE':
            for val in _permute_recursive(base_string + tok.value, rest):
                yield val
            for val in _permute_recursive(base_string, rest):
                yield val
        else:
            for val in _permute_recursive(base_string + tok.value, rest):
                yield val
    

class GeneratorTest(unittest.TestCase):
    #special = ('daily', 'weekdays', 'weekends', 'weekly', 'monthly', 'yearly') 
    #t_values = ('day', 'weekday', 'week', 'month', 'year')
    #test_strings = ('every {n} {time}', 'every {n} {time}s',
    #                '{n} {time}', '{n} {time}s')

    n_values = (1, 10, 243)

    def _test_strings(self, test_string, *, ignore_n=False):
        if not ignore_n:
            for n in self.n_values:
                test_n = test_string.format(n = n)
                for opt in permute_optional(test_n):
                    yield (opt.lower(), n)
                    yield (opt.upper(), n)
        else:
            for opt in permute_optional(test_string.format()):
                yield opt.lower()
                yield opt.upper()

    def _check(self, expected, string):
        actual = parser.parse(string)
        self.assertEqual(expected, actual, 'Failed parsing ' + string)

    def test_day(self):
        test_string = '{{every}} {n} da{{y}}{{s}}'
        for string, n in self._test_strings(test_string):
            expected = DateRepeat(Generator('DAY', n), None, None)
            self._check(expected, string)

    def test_daily(self):
        test_string = 'd{{a}}{{i}}l{{y}}'
        expected = DateRepeat(Generator('DAY', 1), None, None)
        for string in self._test_strings(test_string, ignore_n=True):
            self._check(expected, string)

    def test_weekday(self):
        test_string = '{{every}} {n} w[ee]{{k}}d{{a}}{{y}}{{s}}'
        for string, n in self._test_strings(test_string):
            expected = DateRepeat(Generator('WEEKDAY', n), None, None)
            self._check(expected, string)

    def test_weekday_no_n(self):
        test_string = '{{every}} w[ee]{{k}}d{{a}}{{y}}{{s}}'
        expected = DateRepeat(Generator('WEEKDAY', 1), None, None)
        for string in self._test_strings(test_string, ignore_n=True):
            self._check(expected, string)

    def test_weekend(self):
        test_string = '{{every}} {n} w[ee]{{k}}{{e}}n{{d}}{{s}}'
        for string, n in self._test_strings(test_string):
            expected = DateRepeat(Generator('WEEKEND', n), None, None)
            self._check(expected, string)

    def test_weekend_no_n(self):
        test_string = '{{every}} w[ee]{{k}}{{e}}n{{d}}{{s}}'
        expected = DateRepeat(Generator('WEEKEND', 1), None, None)
        for string in self._test_strings(test_string, ignore_n=True):
            self._check(expected, string)

    def test_week(self):
        test_string = '{{every}} {n} w[ee]k[s]'
        for string, n in self._test_strings(test_string):
            expected = DateRepeat(Generator('WEEK', n), None, None)
            self._check(expected, string)

    def test_weekly(self):
        test_string = 'w[eek]l{{y}}'
        expected = DateRepeat(Generator('WEEK', 1), None, None)
        for string in self._test_strings(test_string, ignore_n=True):
            self._check(expected, string)

    def test_month(self):
        test_string = '{{every}} {n} m{{o}}n{{t}}{{h}}{{s}}'
        for string, n in self._test_strings(test_string):
            expected = DateRepeat(Generator('MONTH', n), None, None)
            self._check(expected, string)

    def test_monthly(self):
        test_string = 'm{{o}}{{n}}{{t}}{{h}}l{{y}}'
        expected = DateRepeat(Generator('MONTH', 1), None, None)
        for string in self._test_strings(test_string, ignore_n=True):
            self._check(expected, string)

    def test_year(self):
        pass

    def test_yearly(self):
        pass


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(GeneratorTest))
    return suite
