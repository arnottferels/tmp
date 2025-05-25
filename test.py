import sys

api_key = sys.argv[1] if len(sys.argv) > 1 else None
print(f"API Key: {api_key}")
