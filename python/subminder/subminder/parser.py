import re 
from collections import namedtuple

MO = r'[Mm][Oo][Nn]?'
TU = r'[Tt][Uu][Ee]?[Ss]?'
WE = r'[Ww][Ee][Dd]?[Nn]?[Ee]?[Ss]?'
TH = r'[Tt][Hh][Uu]?[Rr]?[Ss]?'
FR = r'[Ff][Rr][Ii]?'
SA = r'[Ss][Aa][Tt]?[Uu]?[Rr]?'
SU = r'[Ss][Uu][Nn]?'
WEEKDAY = r'(?P<WEEKDAY>(?:' + '|'.join([MO, TU, WE, TH, 
                                     FR, SA, SU]) + r')[Dd]?[Aa]?[Yy]?)'

JAN = r'[Jj][Aa][Nn][Uu]?[Aa]?[Rr]?[Yy]?'
FEB = r'[Ff][Ee][Bb][Rr]?[Uu]?[Aa]?[Rr]?[Yy]?'
MAR = r'[Mm][Aa][Rr][Cc]?[Hh]?'
APR = r'[Aa][Pp][Rr][Ii]?[Ll]?'
MAY = r'[Mm][Aa][Yy]'
JUN = r'[Jj][Uu][Nn][Ee]?'
JUL = r'[Jj][Uu][Ll][Yy]?'
AUG = r'[Aa][Uu][Gg][Uu]?[Ss]?[Tt]?'
SEP = r'[Ss][Ee][Pp][Tt]?[Ee]?[Mm]?[Bb]?[Ee]?[Rr]?'
OCT = r'[Oo][Cc][Tt][Oo]?[Bb]?[Ee]?[Rr]?'
NOV = r'[Nn][Oo][Vv][Ee]?[Mm]?[Bb]?[Ee]?[Rr]?'
DEC = r'[Dd][Ee][Cc][Ee]?[Mm]?[Bb]?[Ee]?[Rr]?'
MONTH = r'(?P<MONTH>' + '|'.join([JAN, FEB, MAR, APR, MAY, JUN, JUL, AUG, SEP, 
                                  OCT, NOV, DEC]) + r')'

# Generator increment types
DAY     = r'(?P<DAY>[Dd][Aa][Yy]?[Ss]?)'
DAILY   = r'(?P<DAILY>[Dd][Aa]?[Ii]?[Ll][Yy]?)'
WEEKDAY = r'(?P<WEEKDAY>[Ww][Ee]?[Ee]?[Kk]?[Dd][Aa]?[Yy]?[Ss]?)'
WEEKEND = r'(?P<WEEKEND>[Ww][Ee]?[Ee]?[Kk]?[Ee]?[Nn][Dd]?[Ss]?)'
WEEK    = r'(?P<WEEK>[Ww][Ee]?[Ee]?[Kk][Ss]?)'
WEEKLY  = r'(?P<WEEKLY>[Ww][Ee]?[Ee]?[Kk]?[Ll][Yy]?)'
MONTH   = r'(?P<MONTH>[Mm][Oo]?[Nn][Tt]?[Hh]?[Ss]?)'
MONTHLY = r'(?P<MONTHLY>[Mm][Oo]?[Nn]?[Tt]?[Hh]?[Ll][Yy]?)'
YEAR    = r'(?P<YEAR>[Yy][Ee][Aa]?[Rr]?[Ss]?)'
YEARLY  = r'(?P<YEARLY>[Yy][Ee]?[Aa]?[Rr]?[Ll][Yy]?)'

INC_TYPES  = ['DAILY', 'WEEKDAY', 'WEEKEND', 'WEEKLY', 'MONTHLY', 'YEARLY']
INC_MAP    = {'DAILY':'DAY', 'WEEKDAY':'WEEKDAY', 'WEEKEND':'WEEKEND',
              'WEEKLY':'WEEK', 'MONTHLY':'MONTH', 'YEARLY':'YEAR'}
INCN_TYPES = ['DAY', 'WEEKDAY', 'WEEKEND', 'WEEK', 'MONTH', 'YEAR']

# Numeric types
NUMBER = r'(?P<NUMBER>[1-9][0-9]*)'
#RANGE = r'(?P<RANGE>-)'


# Ignored values
EVERY = r'[Ee][Vv][Ee]?[Rr]?[Yy]?'
WS  = r'\s+'
IGNORE = r'(?P<IGNORE>' + '|'.join([EVERY, WS]) + r')'

# Catchall - means there was a syntax error
ERR = r'(?P<ERR>(.))'

# Put everything together
MASTER_PATTERN = re.compile('|'.join([DAILY, DAY, WEEKDAY, WEEKEND, WEEKLY,
                                      WEEK, MONTHLY, MONTH, YEARLY, YEAR,
                                      NUMBER, IGNORE, ERR]))

Token = namedtuple('Token', ['type', 'value'])
DateRepeat = namedtuple('DateRepeat', ['value', 'start', 'end'])
Date = namedtuple('Date', ['year', 'month', 'day'])
Generator = namedtuple('Generator', ['type', 'increment'])

# Tokenizer
def generate_tokens(pat, text): 
    scanner = pat.scanner(text)
    for m in iter(scanner.match, None):
        tok = Token(m.lastgroup, m.group())
        if tok.type != 'IGNORE':
            yield tok

# Parser
class DateRepeatParser:

    def parse(self, text):
        self.tokens = generate_tokens(MASTER_PATTERN, text)
        #print(list(self.tokens))
        self.tok = None
        self.nexttok = None
        self._advance()
        return self.date_repeat()

    def _advance(self):
        'Advance one token ahead'
        self.tok, self.nexttok = self.nexttok, next(self.tokens, None)

    def _accept(self, toktype):
        'Test and consume the next token if it matches toktype'
        if self.nexttok and self.nexttok.type == toktype:
            self._advance()
            return True
        else:
            return False

    def _expect(self, toktype):
        'Consume the next token if it matches toktype or raise SyntaxError'
        if not self._accept(toktype):
            raise SyntaxError('Expected ' + toktype)

    def date_repeat(self):
        value = self.generator() or self.filter()
        if not value:
            value = Generator('DAY', 1)
        return DateRepeat(value, self.start(), self.end())

    def generator(self):
        inc = 1
        type_ = None
        if self._accept('NUMBER'):
            inc = int(self.tok.value)
            type_ = self.incn_generator()
            if not type_:
                raise SyntaxError('Expected incn generator after number')
        else:
            type_ = self.inc_generator()
        if not type_:
            return None
        else:
            return Generator(type_, inc)

    def inc_generator(self):
        if any(self._accept(x) for x in INC_TYPES):
            return INC_MAP[self.tok.type]
        else:
            return None

    def incn_generator(self):
        if any(self._accept(x) for x in INCN_TYPES):
            return self.tok.type
        else:
            return None

    def start(self):
        if self._accept('START'):
            return self.date()
        else:
            return None

    def end(self):
        if self._accept('END'):
            return self.date()
        else:
            return None

    def filter(self):
        opts = []
        opt = self.item()
        while opt: 
            r = self.range(opt)
            if r:
                opts.append(r)
            else:
                opts.append(opt)
            opt = self.item()
        return Token('FILTER', tuple(opts))

    def range(self, left):
        if self._accept('RANGE'):
            if left is None:
                raise SyntaxError('Expected item before range')
            right = self.item()
            if right is None:
                raise SyntaxError('Incomplete range')
            elif left.type != right.type:
                raise SyntaxError('Expected type {} found {}'.format(
                                   left.type, right.type))
            return Token('RANGE', (left, right))

    def item(self):
        return self.weekday() or self.month()

    def weekday(self):
        if self._accept('WKDAY'):
            return Token('WKDAY', self.tok.value[:2].upper())
        else:
            return None

    def month(self):
        if self._accept('MONTH'):
            return Token('MONTH', self.tok.value[:3].upper())
        else:
            return None

def parse(parse_string):
    parser = DateRepeatParser()
    return parser.parse(parse_string)
