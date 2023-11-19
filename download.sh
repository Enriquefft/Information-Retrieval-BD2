#!/bin/bash

# Parameters:
# file_number: number of the file to be processed
# repeat: whether to repeat the process or not

file_number=$1

if [ -z "$1" ]
then
  echo "Error: No file number provided"
  exit 1
fi

export CSV_PATH=./CSV/spotify_songs/file_$file_number.csv

if [ -z "$2" ]
then
    repeat=0
else
    repeat=1
fi


if [ $repeat -eq 1 ]
then
  echo "Repeat"
    until python Embeddings/main.py; do echo "Try again"; done
else
  echo "No repeat"
    python Embeddings/main.py
fi
