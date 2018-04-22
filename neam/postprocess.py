#!/usr/bin/python3
import re
import sys

MONTHS = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'oct', 'nov', 'dec']
ORDINALS = ['st', 'nd', 'rd', 'th']


curYear = 1900
curMonth = 1


def main():
    text = get_text()

    text = replace_pages(text)
    text = replace_sic(text)
    text = find_titles(text)
    text = tag_bodies(text)
    text = fix_spacing(text)

    print('<body>' + text + '</p></body>')


def get_text():
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as input_file:
            lines = input_file.readlines()
    else:
        lines = sys.stdin.readlines()

    return '\n'.join(lines)


def replace_pages(text):
    return re.sub('page (\d+)', '<pb n="\g<1>"/>', text, flags=re.I)


def replace_sic(text):
    return re.sub('\[sic; (\S+)\]', '<sic>\g<1></sic>', text)


def find_titles(text):
    pattern = re.compile(r"""\n(?:[^.\n\s]+(?:\ +[^.\n\s]+){{,4}}(?:\ -|[,.])\ +)* # The preceeding sentence - the sentence must either be on the same line as the date, or on its own line
                             (?:<.*?>)?                                            # Allow the month to be surrounded in a tag 
                                 ({})(?:\.|[a-z]+)?                                # The month, optionally followed by a period or some more letters (for a full month spelling)
                             (?:</.*?>)?                                           # Allow the month to be surrounded in a tag 
                             \ +(\d+)(?:{})?\.?                                    # The day, optionally followed by an ordinal marker
                             \ *(\d+)?\.?                                          # The year
                             [^\n.]*\.?                                            # The rest of the line
                          """.format('|'.join(MONTHS), '|'.join(ORDINALS)), re.I | re.X)
    return pattern.sub(make_title, text)


def make_title(match_data):
    global curYear
    global curMonth

    title = match_data.group(0)
    month = match_data.group(1)
    day = match_data.group(2)
    year = match_data.group(3)

    if month:
        month = MONTHS.index(month.lower()) + 1

        if month < curMonth:
            curYear += 1
        curMonth = month
    else:
        month = curMonth

    if year:
        curYear = int(year)
    else:
        year = curYear

    return '<div xml:id="EBA{}{}{}" type="Entry"><p><title>{}</title></p><p>'.format(year, pad_number(month, 2), pad_number(day, 2), title)


def pad_number(n, size):
    return '0' * (size - len(str(n))) + str(n)


def tag_bodies(text):
    return re.sub('(</p><p>[\S\s]*?)(<div)', '\g<1></p></div>\g<2>', text)


def fix_spacing(text):
    text = re.sub('\n', ' ', text)
    text = re.sub('(<[^/].*?>) +', '\g<1>', text)
    text = re.sub(' +(?=</)', '', text)
    return re.sub(' {2,}', ' ', text)


if __name__ == '__main__':
    main()
