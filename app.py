from flask import Flask, render_template, request
# from models import db, Feedback
# from config import Config
# # from models import db, Feedback
# from llm import generate_user_response, generate_admin_summary_and_action
# # from config import Config
from task_2.models import db, Feedback
from task_2.llm import generate_user_response, generate_admin_summary_and_action
from task_2.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Bind DB
    db.init_app(app)

    # Auto-create DB + tables
    with app.app_context():
        db.create_all()

    @app.route("/", methods=["GET", "POST"])
    def user_page():
        if request.method == "POST":
            user_msg = request.form.get("message")

            ai_response = generate_user_response(user_msg)

            fb = Feedback(
                user_message=user_msg,
                ai_response=ai_response
            )
            db.session.add(fb)
            db.session.commit()

            return render_template("user.html", response=ai_response)

        return render_template("user.html")

    @app.route("/admin")
    def admin():
        all_feedback = Feedback.query.all()
        return render_template("admin.html", feedback=all_feedback)

    return app
