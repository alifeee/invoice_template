#!/bin/bash

# this script generates a unique invoice number for a date (e.g., "2024-01-01") and index (e.g., "1" or "2")
# it is an alternative of using the date and index directly,
#  for example, "2024010101", which run through the hash becomes "3199"
# the hash consists simply of two parts
#  1. number of days since 2023-12-01
#  2. 
# it therefore supports unique invoice numbers for
#  1. any date after 2023-12-01
#  2. up to 99 invoices per day
# to invoke, use this example call
#  $ ./id_gen.sh 2024-01-01 1
#  > 3130

DATE=$1
INDEX=$2
if [ -z "$DATE" ]; then
  echo "date is required"
  exit 1
fi
if [ -z "$INDEX" ]; then
  echo "index is required"
  exit 1
fi
if [ $INDEX -lt 1 ] || [ $INDEX -gt 100 ]; then
  echo "index must be between 1 and 100"
  exit 1
fi

date_diff=$(( ($(date -d "${DATE} UTC" +%s) - $(date -d "2023-12-01 UTC" +%s)) / (60*60*24) ))

offset=$(($date_diff % 100))

index_hash=$((($INDEX + $offset) % 100))

echo "${date_diff}$(printf "%02d" $index_hash)"
