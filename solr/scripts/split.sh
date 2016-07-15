#!/usr/bin/bash

file=dump.txt
num_files=20

total_lines=$(wc -l <${file})
((lines_per_file = (total_lines + num_files - 1) / num_files))


split --lines=${lines_per_file} ${file} dump_part.

echo "Total lines     = ${total_lines}"
echo "Lines  per file = ${lines_per_file}"
wc -l dump_part.*