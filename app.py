"""ACEest Fitness & Gym - simple Flask service."""
from flask import Flask, jsonify, request


def create_app():
    app = Flask(__name__)

    # In-memory "database" (fine for this assignment)
    app.config["MEMBERS"] = {}
    app.config["NEXT_ID"] = 1

    @app.route("/")
    def index():
        return jsonify(message="Welcome to ACEest Fitness & Gym"), 200

    @app.route("/health")
    def health():
        return jsonify(status="ok"), 200

    @app.route("/members", methods=["GET"])
    def list_members():
        return jsonify(list(app.config["MEMBERS"].values())), 200

    @app.route("/members", methods=["POST"])
    def add_member():
        data = request.get_json(silent=True) or {}
        name = data.get("name")
        plan = data.get("plan", "basic")
        if not name or not isinstance(name, str):
            return jsonify(error="'name' is required"), 400
        if plan not in ("basic", "premium", "elite"):
            return jsonify(error="invalid plan"), 400

        member_id = app.config["NEXT_ID"]
        app.config["NEXT_ID"] += 1
        member = {"id": member_id, "name": name, "plan": plan}
        app.config["MEMBERS"][member_id] = member
        return jsonify(member), 201

    @app.route("/members/<int:member_id>", methods=["GET"])
    def get_member(member_id):
        member = app.config["MEMBERS"].get(member_id)
        if member is None:
            return jsonify(error="member not found"), 404
        return jsonify(member), 200

    @app.route("/members/<int:member_id>", methods=["DELETE"])
    def delete_member(member_id):
        if app.config["MEMBERS"].pop(member_id, None) is None:
            return jsonify(error="member not found"), 404
        return jsonify(message="deleted"), 200

    @app.route("/bmi")
    def bmi():
        try:
            weight = float(request.args["weight"])
            height = float(request.args["height"])
            if weight <= 0 or height <= 0:
                raise ValueError
        except (KeyError, ValueError):
            return jsonify(error="provide positive 'weight' (kg) and 'height' (m)"), 400
        value = round(weight / (height ** 2), 2)
        return jsonify(bmi=value), 200

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
