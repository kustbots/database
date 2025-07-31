from flask import Flask, request, jsonify

app = Flask(__name__)

URLS = []

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
        return jsonify({"message": f"Deleted: {url}"})
    except ValueError:
        return jsonify({"error": "URL not found"}), 404

@app.route("/clear", methods=["DELETE"])
def clear_all():
    URLS.clear()
    return jsonify({"message": "All URLs cleared."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

