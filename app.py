from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# app.config['SQLALCHEMY_RECORD_QUERIES'] = True

debug = DebugToolbarExtension(app)

@app.get("/")
def display_home():
    """ Display opening page of the survey """

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
    """ Redirect to the first question and clear out responses """
    session["responses"] = [] # <--- side effect

    return redirect("/questions/0")


@app.get("/questions/<int:q_id>")
def display_question(q_id):
    """ Display question """
    # I do not not need int(q_id), this is what the decorator does for me with int:
    resps = session["responses"]

    if len(resps) != q_id:
        flash("Cannot access invalid question")
        return redirect(f"/questions/{len(resps)}")

    return render_template(
        "question.jinja",
        question=survey.questions[len(resps)],
        id=len(resps)
    )


@app.post("/answer")
def handle_answer():
    """ Redirect to next question or show completion if no questions remain"""

    answer = request.form["answer"]

    resps = session["responses"]
    resps.append(answer)
    session["responses"] = resps

    # If no more questions remain
    if len(resps) >= len(survey.questions):
        return redirect("/thank-you")

    # Else redirect to the next question
    return redirect(f"/questions/{len(resps)}")


@app.get("/thank-you")
def completetion_page():
    """ Display thank you page with filled in answers"""

    # questions_and_answers = dict(zip(responses, survey.questions) this didn't work because the responses are not unique keys

    prompts = [q.prompt for q in survey.questions]
    responses = session["responses"]
    return render_template(
            "completion.jinja",
            questions=prompts,
            answers=responses
        )
