#!/usr/bin/python3
import sys
from bs4 import BeautifulSoup


def open_tag(tag):
    attrs = ['{}="{}"'.format(id, value) for id, value in tag.attrs.items()]
    return '<{} {}>'.format(tag.name, ' '.join(attrs))


def close_tag(tag):
    return '</{}>'.format(tag.name)

if len(sys.argv) > 1:
    file_name = sys.argv[1]
    with open(file_name) as soup_file:
        soup = BeautifulSoup(soup_file, 'xml')
else:
    soup = BeautifulSoup(sys.stdin, 'xml')

print('<body>')
for div in soup.body.find_all('div'):
    print('\t' + open_tag(div))
    for p in div.find_all('p'):
        print('\t\t' + str(p))
    print('\t' + close_tag(div))
print('</body>')
