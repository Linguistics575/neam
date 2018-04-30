import os
import sys
import platform

clear_code = 'cls' if platform.system() == 'Windows' else 'clear'

with open(sys.argv[1]) as input_file:
    lines = [line.strip() for line in input_file.readlines()]

tags = []

for i in range(len(lines)):
    unused_variable = os.system(clear_code)

    if i > 1:
        print(lines[i-1])
    print('>> ' + lines[i])
    if i < len(lines) - 1:
        print(lines[i+1])

    tags.append(input())

with open(sys.argv[2], 'w') as output_file:
    output_file.write('\n'.join("{}%%%{}".format(tag, line) for [line, tag] in zip(lines, tags)))

