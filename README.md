Just a test repo

```pwsh
# keep the latest run, delete the rest
$repo = gh repo view --json nameWithOwner --jq ".nameWithOwner"
$runs = gh run list --limit 100 --json databaseId --jq ".[1:] | .[].databaseId"

foreach ($id in $runs) {
    gh api "repos/$repo/actions/runs/$id" -X DELETE
}

# delete all runs
$repo = gh repo view --json nameWithOwner --jq ".nameWithOwner"
$runIds = gh run list --json databaseId --jq ".[].databaseId"

foreach ($id in $runIds) {
    gh api "repos/$repo/actions/runs/$id" -X DELETE
}
```
