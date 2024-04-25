from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# app.config['SQLALCHEMY_RECORD_QUERIES'] = True

debug = DebugToolbarExtension(app)

responses = []
curr_question_id = 0

@app.get("/")
def display_home():
    """ Display surveys title in the homepage """

    return render_template(
        "survey_start.jinja",
        title=survey.title,
        instructions=survey.instructions
        )

# Posts can never be cached 100% your browser will send a request.
# with get methods your browsers will decide if it needs to make a request.
# As a dev I have no control over the get

@app.post("/begin")
def redirect_questions():
    """ Redirect to questions """
    q_id = str(curr_question_id)

    return redirect(f"/questions/{q_id}")


@app.get("/questions/<q_id>")
def display_question(q_id):
    """ Display question"""

    q_id = int(q_id)
    global curr_question_id
    curr_question_id += 1

    return render_template(
        "question.jinja",
        question=survey.questions[q_id],
        id=q_id
    )

@app.post("/answer")
def handle_answer():
    """ Redirect to next question or show completion if no other questions"""

    global curr_question_id

    if curr_question_id >= len(survey.questions):
        curr_question_id = 0

        return render_template(
            "completion.jinja",
            answers=responses
        )

    answer = request.form.get("answer")
    responses.append(answer)
    print("RESPONSES", answer, responses)

    q_id = str(curr_question_id)

    return redirect(f"/questions/{q_id}")
