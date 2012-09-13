#!/bin/bash

for f in my db db_conn xml; do
	echo "$f:"
	hotshot2calltree $f.prof > $f.out
	awk '/summary:/{print $2}' $f.out
done
