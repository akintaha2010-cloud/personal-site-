from match import calculate_match_score
from flask import (
    Flask,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for
)

from king import auth

from database import (
    init_db,
    get_items,
    get_items_by_user,
    add_item,
    delete_item
)


app = Flask(__name__)
app.secret_key = "founddesk-development-secret-key"
app.register_blueprint(auth)

#Here are the functions for the web interface
@app.route("/users", methods=["GET"])
def list_items():
    items = get_items()
    return jsonify(items)

#Function for matching a user's item to items in the database
@app.route("/")
def index():
    items = get_items()

    possible_matches = []

    for lost_item in items:
        if lost_item[1] != "Lost":
            continue

        lost_data = {
            "id": lost_item[0],
            "name": lost_item[2],
            "location": lost_item[3],
            "category": lost_item[4] or "",
            "description": lost_item[5] or ""
        }

        for found_item in items:
            if found_item[1] != "Found":
                continue

            found_data = {
                "id": found_item[0],
                "name": found_item[2],
                "location": found_item[3],
                "category": found_item[4] or "",
                "description": found_item[5] or ""
            }

            score = calculate_match_score(
                lost_data,
                found_data
            )

            #if matching score is more than 50, then the lost item and foud item could be a match
            if score >= 50:
                possible_matches.append({
                    "lost": lost_data,
                    "found": found_data,
                    "score": score
                })

    possible_matches.sort(
        key=lambda match: match["score"],
        reverse=True
    )

    return render_template(
        "index.html",
        items=items,
        possible_matches=possible_matches
    )

#Function for displaying a user's items
@app.route("/my-items")
def my_items():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    items = get_items_by_user(
        session["user_id"]
    )

    return render_template(
        "my_items.html",
        items=items
    )

#Function for entering a user's item
@app.route("/add_user", methods=["POST"])
def add_user_route():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    report_type = request.form.get(
        "report_type",
        ""
    ).strip()

    item_name = request.form.get(
        "item_name",
        ""
    ).strip()

    location = request.form.get(
        "location",
        ""
    ).strip()

    category = request.form.get(
        "category",
        ""
    ).strip()

    description = request.form.get(
        "description",
        ""
    ).strip()

    if (
        not report_type
        or not item_name
        or not location
        or not category
    ):
        return "Please fill in all required fields.", 400

    add_item(
        report_type,
        item_name,
        location,
        category,
        description,
        session["user_id"]
    )

    return redirect(url_for("index"))

#Function for deleting a user's item
@app.route("/delete_user/<int:item_id>", methods=["GET"])
def delete_user_route(item_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    deleted_count = delete_item(
        item_id,
        session["user_id"]
    )

    if deleted_count == 0:
        return "You cannot delete another user's post.", 403

    return redirect(url_for("index"))

#Main method
if __name__ == "__main__":
    import threading
    import time
    import webview

    init_db()

    def run_flask():
        app.run(
            host="127.0.0.1",
            port=5000,
            debug=False,
            use_reloader=False
        )

    flask_thread = threading.Thread(
        target=run_flask,
        daemon=True
    )

    flask_thread.start()

    time.sleep(1)

    webview.create_window(
        "FoundDesk",
        "http://127.0.0.1:5000/register",
        width=1000,
        height=700
    )  
    
    webview.start()