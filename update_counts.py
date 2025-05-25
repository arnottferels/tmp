import sys
import os
import json
import aiohttp
import asyncio
from dataclasses import dataclass
from typing import Dict, List
from dotenv import load_dotenv

load_dotenv()
API_URL_KEY = "UPDATE_COUNTS_WEB_APP_URL"
API_URL = os.getenv(API_URL_KEY) or sys.exit(f"Error: {API_URL_KEY} is missing.")

FETCH_URL = "https://arnottferels.github.io/a/data/redirect.json"


RAW_FILE = "raw.json"
OUTPUT_FILE = "counts.json"

PathnameKey = str
RedirectPath = str
IntCount = int
TotalCount = int

PathRedirectMappings = Dict[PathnameKey, List[RedirectPath]]


@dataclass
class PathCounts:
    paths_counts: Dict[RedirectPath, IntCount]
    total_count: TotalCount = 0


def transform_data_structure(
    fetch_data: PathRedirectMappings,
) -> Dict[PathnameKey, PathCounts]:
    return {
        key: PathCounts(paths_counts={path: 0 for path in paths})
        for key, paths in fetch_data.items()
    }


async def fetch_all_counts(session: aiohttp.ClientSession) -> Dict[str, int]:
    try:
        async with session.get(API_URL) as response:
            if response.status == 200:
                data = await response.json()
                return {k: int(v) for k, v in data.items()}
            else:
                print(f"Failed to fetch counts: HTTP {response.status}")
    except Exception as e:
        print(f"Exception fetching counts: {e}")
    return {}


async def fetch_and_cache_redirect_map(
    session: aiohttp.ClientSession,
) -> PathRedirectMappings:
    async with session.get(FETCH_URL) as response:
        data = await response.json()
        with open(RAW_FILE, "w") as file:
            json.dump(data, file, indent=2)
        print(f"Redirect map fetched and saved to {RAW_FILE}.")
        return data


async def process_transformed_data(
    transformed_data: Dict[PathnameKey, PathCounts],
    all_counts: Dict[str, int],
) -> None:
    for path_counts in transformed_data.values():
        total = 0
        for pathname in path_counts.paths_counts:
            count = all_counts.get(pathname, 0)
            path_counts.paths_counts[pathname] = count
            total += count
        path_counts.total_count = total


async def save_transformed_data(
    transformed_data: Dict[PathnameKey, PathCounts],
) -> None:
    filtered: Dict[str, Dict[str, int | Dict[str, int]]] = {}

    for key, path_counts in transformed_data.items():
        filtered_paths = {p: c for p, c in path_counts.paths_counts.items() if c > 0}
        if not filtered_paths:
            continue

        filtered[key] = {
            "paths_counts": filtered_paths,
            "total_count": sum(filtered_paths.values()),
        }

    with open(OUTPUT_FILE, "w") as file:
        json.dump(filtered, file, indent=2)
    print(f"Filtered data saved to {OUTPUT_FILE}.")


async def main() -> None:
    async with aiohttp.ClientSession() as session:
        redirect_map = await fetch_and_cache_redirect_map(session)
        transformed_data = transform_data_structure(redirect_map)
        all_counts = await fetch_all_counts(session)
        await process_transformed_data(transformed_data, all_counts)
        await save_transformed_data(transformed_data)


if __name__ == "__main__":
    asyncio.run(main())
