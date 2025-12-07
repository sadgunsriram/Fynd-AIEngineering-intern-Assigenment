from flask import Flask, render_template, request, jsonify
from task_2.models import db, Feedback
from task_2.llm import generate_user_response, generate_admin_summary_and_action
from task_2.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route("/", methods=["GET"])
    def user_page():
        return render_template("user.html")

    @app.route("/submit_feedback", methods=["POST"])
    def submit_feedback():
        rating = int(request.form.get("rating"))
        review = request.form.get("review")

        ai_user_response = generate_user_response(rating, review)
        admin_summary, admin_action = generate_admin_summary_and_action(rating, review)

        fb = Feedback(
            rating=rating,
            review_text=review,
            ai_user_response=ai_user_response,
            ai_admin_summary=admin_summary,
            ai_recommended_action=admin_action
        )

        db.session.add(fb)
        db.session.commit()

        return jsonify({"ai_user_response": ai_user_response})

    @app.route("/admin")
    def admin():
        feedbacks = Feedback.query.order_by(Feedback.created_at.desc()).all()

        total = len(feedbacks)
        avg_rating = round(sum(f.rating for f in feedbacks) / total, 2) if total else 0

        rating_counts = {i: 0 for i in range(1, 6)}
        for f in feedbacks:
            rating_counts[f.rating] += 1

        return render_template(
            "admin.html",
            feedbacks=feedbacks,
            total=total,
            avg_rating=avg_rating,
            rating_counts=rating_counts
        )

    return app
