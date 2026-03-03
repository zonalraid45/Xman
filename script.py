import requests

TEAM_ID = "royalracer-fans"
OUTPUT_FILE = "qualified_players.txt"

def main():
    headers = {"Accept": "application/x-ndjson"}
    team_url = f"https://lichess.org/api/team/{TEAM_ID}/users"

    response = requests.get(team_url, headers=headers)
    response.raise_for_status()

    qualified = []

    for line in response.text.strip().split("\n"):
        username = line.strip()
        if not username:
            continue

        user = requests.get(
            f"https://lichess.org/api/user/{username}",
            headers={"Accept": "application/json"}
        ).json()

        blitz = user.get("perfs", {}).get("blitz", {}).get("rating", 0)
        rapid = user.get("perfs", {}).get("rapid", {}).get("rating", 0)

        if blitz >= 2000 and rapid >= 2000:
            qualified.append(f"{username} | Blitz: {blitz} | Rapid: {rapid}")

    with open(OUTPUT_FILE, "w") as f:
        f.write("\n".join(qualified))

if __name__ == "__main__":
    main()
