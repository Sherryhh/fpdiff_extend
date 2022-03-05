#!/bin/bash
threshold=0.0001

infile=$1
outfile=$2
NEWLINE=$'\n'
outputstream=''

while read line; do
	if [[ $line == *"==== S3FP arguments and settings ===="* ]]; then
		if [[ $status == "T" ]]; then
			outputstream="$outputstream$NEWLINE$field"
		fi
		field=$line
		status='F'
	else
		field="$field$NEWLINE$line"
	fi

	if [[ $line == *"Best Relative Error"* ]]; then
		rel=$(echo $line | cut -d ' ' -f 4)
		weight=$(awk -v n1="$rel" -v n2="$threshold" 'BEGIN {printf "" (n1<n2?"<":">=") "\n"}')
		if [[ $weight == ">=" ]]; then
			status="T"
		fi
	fi
done < $infile

if [[ $status == "T" ]]; then
	outputstream="$outputstream$NEWLINE$field"
fi

echo "$outputstream" | tail -n +2 | head -n -1 > "$outfile"