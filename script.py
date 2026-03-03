import requests
import json

TEAM_ID = "royalracer-fans"
OUTPUT_FILE = "qualified_players.txt"

HEADERS = {
    "Accept": "application/x-ndjson",
    "User-Agent": "github-action-bot"
}

def main():
    team_url = f"https://lichess.org/api/team/{TEAM_ID}/users"
    
    response = requests.get(team_url, headers=HEADERS, timeout=30)
    response.raise_for_status()

    qualified = []

    for line in response.iter_lines():
        if not line:
            continue

        user = json.loads(line)
        username = user.get("id")

        blitz = user.get("perfs", {}).get("blitz", {}).get("rating", 0)
        rapid = user.get("perfs", {}).get("rapid", {}).get("rating", 0)

        if blitz >= 2000 and rapid >= 2000:
            qualified.append(f"{username} | Blitz: {blitz} | Rapid: {rapid}")

    with open(OUTPUT_FILE, "w") as f:
        f.write("\n".join(qualified))

if __name__ == "__main__":
    main()
