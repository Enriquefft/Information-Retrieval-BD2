#!/bin/bash

# Load environment variables from .env file
if [ -f .env ]
then
  export $(cat .env | sed 's/#.*//g' | xargs)
fi


mandatory_vars=()
optional_vars=()


reached_optional=false
# Populate mandatory_vars and optional_vars arrays
for var in "$@"
do
  if [ "$var" == "optional" ]
  then
    reached_optional=true
  elif [ "$reached_optional" == true ]
  then
    optional_vars+=("$var")
  else
    mandatory_vars+=("$var")
  fi
done

# Check if each mandatory variable is set
for var in "${mandatory_vars[@]}"
do
  if [ -z "${!var}" ]
  then

    # Keep asking for the value until it is set
    value=""
    while [ -z "$value" ]
    do
      read -p "Enter the value for $var: " value
      export $var=$value
    done
  fi
done

# Check if each optional variable is set
for var in "${optional_vars[@]}"
do
  if [ -z "${!var}" ]
  then
    read -p "Enter the value for $var (press enter to skip): " value
    if [ -n "$value" ]
    then
      export $var=$value
    fi
  fi
done

