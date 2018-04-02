import cmd
from dateexpression import SimpleGenerator, WeekdayFilter, MonthFilter
from parser import DateExpressionParser
from itertools import islice
from datetime import date

wkdayhack = {name:idx for idx,name in enumerate(['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU'])}
class ParseRepl(cmd.Cmd):

    def __init__(self):
        super().__init__()
        self.parser = DateExpressionParser()
    
    # Do nothing on empty line
    def emptyline():
        pass

    def default(self, line):
        toklist = self.parser.parse(line)
        wkdays = (wkdayhack[tok.value] for tok in toklist.value if tok.type == 'WKDAY')
        months = (tok.value for tok in toklist.value if tok.type == 'MONTH')
        chain = SimpleGenerator().filter(WeekdayFilter(*set(wkdays)))
        print(list(date.fromordinal(x) for x in islice(chain, 10)))

    def do_quit(self, line):
        print('Goodbye')
        return True


if __name__ == '__main__':
    ParseRepl().cmdloop()
