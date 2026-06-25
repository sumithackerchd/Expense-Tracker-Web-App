import requests

def scan_target(url):
    try:
        r = requests.get(url, timeout=5)
        return {
            "status_code": r.status_code,
            "server": r.headers.get("Server","Unknown"),
            "headers": dict(r.headers)
        }
    except Exception as e:
        return {"error": str(e)}
