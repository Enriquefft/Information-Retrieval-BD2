#!/bin/bash

source ./read_env.sh DB_NAME CSV_PATH CSV_TYPE



echo $CSV_TYPE
if [ "$CSV_TYPE" = "test" ]
then
  CSV_FILE="$CSV_PATH/test.csv"
elif [ "$CSV_TYPE" = "prod" ]
then
  CSV_FILE="$CSV_PATH/spotify_songs.csv"
else
  echo "Invalid data type"
  exit 1
fi


# Copy tracks from CSV file to database
psql -d $DB_NAME -c "\COPY tracks FROM '$CSV_FILE' DELIMITER ',' CSV HEADER;"


