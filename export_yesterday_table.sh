#!/bin/bash
set -e

mkdir -p "$REPO_DIR/$REMOTE_TABLE_DIR"

echo "Exporting $YESTERDAY to $CSV_PATH"

psql "$DB_URL" -c "\COPY (
  SELECT * FROM ${TABLE_NAME}
  WHERE timestamp::date = DATE '$YESTERDAY'
) TO '$CSV_PATH' WITH CSV HEADER"