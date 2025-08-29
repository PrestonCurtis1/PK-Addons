import requests, json, os, datetime

servers = json.load(open("servers.json"))
history_path = "data/server_history.json"

if os.path.exists(history_path):
    history = json.load(open(history_path))
else:
    history = {}

timestamp = datetime.datetime.utcnow().isoformat()

for srv in servers:
    ip = srv["ip"]
    try:
        resp = requests.get(f"https://api.mcsrvstat.us/2/{ip}", timeout=15).json()
        online = resp.get("online", False)
        players = resp.get("players", {}).get("online", 0) if online else 0
    except Exception:
        players = 0

    if srv["name"] not in history:
        history[srv["name"]] = []

    history[srv["name"]].append({
        "time": timestamp,
        "players": players
    })

    history[srv["name"]] = history[srv["name"]][-144:]

os.makedirs("data", exist_ok=True)
with open(history_path, "w") as f:
    json.dump(history, f, indent=2)
