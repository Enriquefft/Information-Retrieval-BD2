#!/bin/bash
#
source ./read_env.sh DB_NAME


# run create_index.sql
psql -d $DB_NAME -f create_index.sql
