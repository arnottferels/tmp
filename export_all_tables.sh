#!/bin/bash
set -e

mkdir -p "$REPO_DIR/$REMOTE_TABLE_DIR"

echo "Exporting all data from $TABLE_NAME..."

psql "$DB_URL" -c "\COPY (
  SELECT * FROM ${TABLE_NAME}
) TO 'all_data.csv' WITH CSV HEADER"

header=$(head -n 1 all_data.csv)

timestamp_col=$(echo "$header" | tr ',' '\n' | awk '
{
  if ($0 ~ /^"?timestamp"?$/) {
    print NR
    exit
  }
}')

if [ -z "$timestamp_col" ]; then
  echo "timestamp column not found."
  exit 1
fi

tail -n +2 all_data.csv | awk -F',' -v header="$header" -v col="$timestamp_col" '
{
  ts = $col
  gsub(/^"|"$/, "", ts)
  split(ts, parts, "T")
  day = parts[1]

  file = "'"$REPO_DIR"'/'"$REMOTE_TABLE_DIR"'/" day ".csv"
  if (!(day in seen)) {
    print header > file
    seen[day] = 1
  }
  print $0 >> file
}'
