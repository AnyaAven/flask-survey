from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# app.config['SQLALCHEMY_RECORD_QUERIES'] = True

debug = DebugToolbarExtension(app)

responses = []

@app.get("/")
def display_home():
    """ Display surveys title in the homepage """

    return render_template(
        "survey_start.jinja",
        title=survey.title,
        instructions=survey.instructions
        )

# Posts can never be cached %100 your browser will send a request, with get
# with get methods your browsers will decide if it needs to make a request.
# As a dev I have no control over the get

@app.post("/begin")
def redirect_questions():
    """ Redirect to questions """
    q_id = 0

    return redirect(f"/questions/{q_id}")


@app.get("/questions/<q_id>")
def display_question(q_id):
    """ Display question"""

    q_id = int(q_id)

    return render_template(
        "question.jinja",
        question=survey.questions[q_id]
    )
