
import os
import logging

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-me")

# Gmail SMTP configuration
app.config.update(
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME="sooryas851@gmail.com",
    MAIL_PASSWORD=os.environ.get("MAIL_PASSWORD", "sdhw ztys ogap egdb"),
    MAIL_DEFAULT_SENDER="sooryas851@gmail.com",
)

mail = Mail(app)
logging.basicConfig(level=logging.INFO)

SKILLS = [
    "Python", "Java", "C", "C++", "HTML5", "CSS3", "Bootstrap",
    "JS", "Flask", "MySQL", "SQLite", "Git", "GitHub", "VS Code"," Anti-Gravity"
]

CERTS = [
    ("🌐", "Web Development", "DigiDARA"),
    ("🗃️", "Oracle Database", "Naan Mudhalvan"),
    ("☕", "Java Spring", "Naan Mudhalvan"),
    ("🐍", "Python Foundations", "Naan Mudhalvan"),
]

G = "https://github.com/sooya08/"

PROJECTS = [
    ("🌫️", "AirGuardian",
     "ML app that predicts the Air Quality Index with Linear Regression and Random Forest. Deployed on Hugging Face Spaces.",
     "Python", G + "AirGuardian"),
    ("₿", "Bitcoin Prediction",
     "Forecasting algorithms with live data to predict Bitcoin price trends.",
     "Python", G + "Bitcoin_prediction"),
    ("📚", "Faculty Publication Tracker",
     "Flask and MySQL web app to manage faculty research publications with full CRUD.",
     "Flask", G + "Faculty_publication_Tracker"),
    ("🌐", "Personal Portfolio",
     "Responsive portfolio with 3D animation, built with Flask.",
     "Flask", G + "Personal_portfolio"),
    ("🏦", "Secure Banking",
     "Backend app with structured banking workflows, focused on security and data.",
     "Python", G + "securebanking"),
    ("📈", "Demand Prediction",
     "Predicts future product demand from historical data using statistics and ML.",
     "Python", G + "demand_prediction"),
    ("🏟️", "Sports Hub Management",
     "Web app module for managing a sports hub, scheduling and users.",
     "HTML", G + "sports-hub-management"),
    ("🗂️", "Resource Management",
     "Template and asset repository for faster project setup.",
     "HTML", G + "new_resource"),
]


@app.route("/")
def home():
    return render_template("index.html", skills=SKILLS)


@app.route("/work")
def work():
    return render_template("work.html", certs=CERTS)


@app.route("/projects")
def projects():
    return render_template("projects.html", projects=PROJECTS)


@app.route("/resume")
def resume():
    return render_template("resume.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if not all([name, email, message]):
            flash("Please fill in all fields.", "danger")
            return redirect(url_for("contact"))

        if not app.config["MAIL_PASSWORD"]:
            app.logger.error("MAIL_PASSWORD environment variable is missing.")
            flash("Email service is not configured. Please try again later.", "danger")
            return redirect(url_for("contact"))

        try:
            # Send the contact message to Soorya
            msg_to_me = Message(
                subject=f"New message from {name}",
                recipients=["sooryas851@gmail.com"],
                body=(
                    f"From: {name}\n"
                    f"Email: {email}\n\n"
                    f"Message:\n{message}"
                ),
            )
            mail.send(msg_to_me)

            # Send an automatic reply to the visitor
            msg_to_user = Message(
                subject="Thanks for contacting Soorya!",
                recipients=[email],
                body=(
                    f"Hi {name},\n\n"
                    "Thanks for reaching out! I have received your message:\n\n"
                    f'"{message}"\n\n'
                    "I will get back to you soon.\n\n"
                    "Regards,\nSoorya J"
                ),
            )
            mail.send(msg_to_user)

            flash(
                "Your message has been sent. "
                "A confirmation was also sent to your email.",
                "success",
            )

        except Exception:
            app.logger.exception("Failed to send contact email.")
            flash(
                "Could not send your message. Please try again later.",
                "danger",
            )

        return redirect(url_for("contact"))

    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)