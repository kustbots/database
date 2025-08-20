from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory JSON-like database
DB = {}

@app.route("/")
def index():
    return "🟢 JSON Memory API running."

# ---- Generic JSON storage ----

@app.route("/set", methods=["POST"])
def set_data():
    """
    Body: { "key": "user123", "data": {"recent_songs": [...], "theme": "dark"} }
    Creates or updates a record.
    """
    data = request.get_json()
    key = data.get("key")
    value = data.get("data")

    if not key or value is None:
        return jsonify({"error": "Missing 'key' or 'data'"}), 400

    # Overwrite or create
    DB[key] = value
    return jsonify({"message": f"Data set for key '{key}'", "data": value})

@app.route("/get", methods=["GET"])
def get_data():
    """
    Params: ?key=user123
    """
    key = request.args.get("key")
    if not key:
        return jsonify({"error": "Missing 'key' param"}), 400
    value = DB.get(key)
    if value is None:
        return jsonify({"error": "No data for this key"}), 404
    return jsonify({key: value})

@app.route("/update", methods=["PATCH"])
def update_data():
    """
    Body: { "key": "user123", "data": {"recent_songs": ["new_song"]} }
    Merges data instead of replacing.
    """
    data = request.get_json()
    key = data.get("key")
    updates = data.get("data")

    if not key or updates is None:
        return jsonify({"error": "Missing 'key' or 'data'"}), 400
    if key not in DB:
        return jsonify({"error": "Key not found"}), 404

    # Merge dictionaries
    if isinstance(DB[key], dict) and isinstance(updates, dict):
        DB[key].update(updates)
    else:
        DB[key] = updates  # if not dict, replace

    return jsonify({"message": f"Data updated for key '{key}'", "data": DB[key]})

@app.route("/delete", methods=["DELETE"])
def delete_data():
    """
    Params: ?key=user123
    """
    key = request.args.get("key")
    if not key:
        return jsonify({"error": "Missing 'key' param"}), 400
    if key not in DB:
        return jsonify({"error": "Key not found"}), 404
    del DB[key]
    return jsonify({"message": f"Deleted key '{key}'"})

@app.route("/all", methods=["GET"])
def list_all():
    return jsonify(DB)

@app.route("/clear", methods=["DELETE"])
def clear_all():
    DB.clear()
    return jsonify({"message": "All data cleared."})

# ---- Extra: Append to list (for songs, history, etc.) ----

@app.route("/append", methods=["POST"])
def append_data():
    """
    Body: { "key": "user123", "field": "recent_songs", "value": "songX" }
    Appends value to a list field.
    """
    data = request.get_json()
    key = data.get("key")
    field = data.get("field")
    value = data.get("value")

    if not key or not field or value is None:
        return jsonify({"error": "Missing 'key', 'field' or 'value'"}), 400
    if key not in DB:
        DB[key] = {}
    if field not in DB[key]:
        DB[key][field] = []
    if not isinstance(DB[key][field], list):
        return jsonify({"error": f"Field '{field}' is not a list"}), 400

    DB[key][field].append(value)
    return jsonify({"message": f"Value appended to '{field}' for key '{key}'", "data": DB[key]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)



