import requests
import json
import time

TEAM_ID = "royalracer-fans"
OUTPUT_FILE = "qualified_players.txt"

HEADERS = {
    "Accept": "application/x-ndjson",
    "User-Agent": "github-action-bot"
}

def main():
    team_url = f"https://lichess.org/api/team/{TEAM_ID}/users"

    response = requests.get(team_url, headers=HEADERS)
    response.raise_for_status()

    qualified = []

    for line in response.iter_lines():
        if not line:
            continue

        user_data = json.loads(line)
        username = user_data.get("id")

        # Safety delay to avoid rate limit
        time.sleep(0.2)

        user_resp = requests.get(
            f"https://lichess.org/api/user/{username}",
            headers={"Accept": "application/json", "User-Agent": "github-action-bot"}
        )

        if user_resp.status_code != 200:
            continue

        try:
            user = user_resp.json()
        except:
            continue

        blitz = user.get("perfs", {}).get("blitz", {}).get("rating", 0)
        rapid = user.get("perfs", {}).get("rapid", {}).get("rating", 0)

        if blitz >= 2000 and rapid >= 2000:
            qualified.append(f"{username} | Blitz: {blitz} | Rapid: {rapid}")

    with open(OUTPUT_FILE, "w") as f:
        f.write("\n".join(qualified))

if __name__ == "__main__":
    main()
