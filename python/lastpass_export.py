# Command line utility to format the CSV file from LastPass export into
# something printable

import csv
import sys

from collections import defaultdict

fieldnames = 'url,username,password,extra,name,grouping,fav'.split(',')

def main(args):
    try:
        export(args[1], args[2] if len(args) > 2 else 'passwords.txt')
    except Exception as e:
        sys.stderr.write('ERROR:\n')
        sys.stderr.write(str(e) + '\n\n')
        sys.stdout.write(usage(args[0]))

def usage(executable_name):
    return 'Usage: {} <lastpass_export.csv> [<output.txt>]'

def export(path_in, path_out):
    ''' Export data from a CSV in path_in to the text file path_out '''
    passwords = read_records(path_in)
    passwords.next()  # Discard header row
    groups = group(passwords)
    formatter = get_format_writer(section_writer, entry_writer)
    write_formatted(path_out, groups, formatter)

def read_records(path_in):
    ''' Read records as a dictionary from the CSV file '''
    with open(path_in, 'rb') as fin:
        reader = csv.DictReader(fin, fieldnames)
        for record in reader:
            yield record

def group(iterable, key='grouping'):
    ''' Collect items in a dictionary by a specified key '''
    groups = defaultdict(list)
    for item in iterable:
        groups[item[key]].append(item)
    return groups

def write_formatted(path_out, groups, format_writer):
    with open(path_out, 'wt') as fout:
        format_writer(fout, groups)

def get_format_writer(group_writer, item_writer):
    ''' 
    Returns a closure for formatting 'groups' and writing the output to
    fout
    '''
    def format_writer(fout, groups):
        sortedgroups = iter(sorted(groups.items()))
        for group in sortedgroups:
            group_writer(fout, group[0], group[1], item_writer)
    return format_writer

def section_writer(fout, name, entries, item_writer):
    sep = '=' * len(name) + '\n'
    fout.write(sep)
    fout.write(name + '\n')
    fout.write(sep)
    fout.write('\n')
    for entry in entries:
        item_writer(fout, entry)

def entry_writer(fout, entry):
    sep = '-' * len(entry['name']) + '\n'
    fout.write(entry['name'] + '\n')
    fout.write(sep)
    fout.write('URL: ' + entry['url'] + '\n')
    fout.write('Username: ' + entry['username'] + '\n')
    fout.write('Password: ' + entry['password'] + '\n\n')

if __name__ == '__main__':
    main(sys.argv)
