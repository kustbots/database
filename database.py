from flask import Flask, request, jsonify

app = Flask(__name__)

URLS = []
UPTIME_STATS = {} 

@app.route("/")
def index():
    return "🟢 Uptime Memory API is running."

@app.route("/set", methods=["POST"])
def add_url():
    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({"error": "Missing 'url'"}), 400
    if url not in URLS:
        URLS.append(url)
        return jsonify({"message": f"URL added: {url}"})
    else:
        return jsonify({"message": f"URL already exists: {url}"}), 200

@app.route("/get", methods=["GET"])
def get_url():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing 'url' param"}), 400
    exists = url in URLS
    return jsonify({"exists": exists, "url": url})

@app.route("/all", methods=["GET"])
def list_all():
    return jsonify(URLS)

@app.route("/delete", methods=["DELETE"])
def delete_url():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing 'url' param"}), 400
    try:
        URLS.remove(url)
        UPTIME_STATS.pop(url, None)
        return jsonify({"message": f"Deleted: {url}"})
    except ValueError:
        return jsonify({"error": "URL not found"}), 404

@app.route("/clear", methods=["DELETE"])
def clear_all():
    URLS.clear()
    UPTIME_STATS.clear()
    return jsonify({"message": "All URLs and stats cleared."})

@app.route("/uptime", methods=["POST", "GET"])
def handle_uptime():
    if request.method == "POST":
        data = request.get_json()
        url = data.get("url")
        success = data.get("success")  # Boolean: True or False

        if not url or success is None:
            return jsonify({"error": "Missing 'url' or 'success'"}), 400

        stats = UPTIME_STATS.get(url, {"total": 0, "success": 0})
        stats["total"] += 1
        if success:
            stats["success"] += 1
        UPTIME_STATS[url] = stats

        return jsonify({"message": "Uptime updated", "stats": stats})

    elif request.method == "GET":
        url = request.args.get("url")
        if url:
            stats = UPTIME_STATS.get(url)
            if not stats:
                return jsonify({"error": "No stats found for this URL"}), 404
            uptime_percent = (stats["success"] / stats["total"] * 100) if stats["total"] else 0
            return jsonify({url: {**stats, "uptime_percent": round(uptime_percent, 2)}})
        else:
            result = {}
            for url, stats in UPTIME_STATS.items():
                uptime_percent = (stats["success"] / stats["total"] * 100) if stats["total"] else 0
                result[url] = {**stats, "uptime_percent": round(uptime_percent, 2)}
            return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)


