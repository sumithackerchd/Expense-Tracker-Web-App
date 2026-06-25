
from flask import Flask, render_template, request
import requests, socket
from urllib.parse import urlparse

app = Flask(__name__)

SEC_HEADERS = [
    "Content-Security-Policy",
    "Strict-Transport-Security",
    "X-Frame-Options",
    "X-Content-Type-Options"
]

def scan(url):
    result = {}
    try:
        r = requests.get(url, timeout=5)
        result["status"] = r.status_code
        result["server"] = r.headers.get("Server","Unknown")
        result["headers"] = {h: r.headers.get(h,"Missing") for h in SEC_HEADERS}

        host = urlparse(url).netloc
        ports = []
        for p in [21,22,25,53,80,110,143,443,3306,8080]:
            s = socket.socket()
            s.settimeout(0.3)
            if s.connect_ex((host,p)) == 0:
                ports.append(p)
            s.close()
        result["ports"] = ports
    except Exception as e:
        result["error"] = str(e)
    return result

@app.route("/", methods=["GET","POST"])
def home():
    data = None
    if request.method == "POST":
        data = scan(request.form["url"])
    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
