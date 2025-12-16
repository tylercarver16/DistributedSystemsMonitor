import requests

def get_metrics_from_url(base_url):
    base = f"{base_url}/api/v1/data?after=-60&points=10&group=average"

    def fetch(chart, key):
        url = f"{base}&chart={chart}"
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        data = r.json()
        labels = data["labels"]
        rows = data["data"]
        return {
            "timestamps": [row[labels.index("time")] for row in rows],
            "values": [row[labels.index(key)] for row in rows]
        }

    return {
        "cpu": fetch("system.cpu", "user"),
        "memory": fetch("system.ram", "used"),
        "disk": fetch("disk_space./", "used"),
        "network": fetch("system.net", "received")
    }

