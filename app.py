#to change route for the input
from flask import Flask, render_template, request, redirect, flash, jsonify , url_for
app = Flask(__name__)
app.config["SECRET_KEY"] = "SHHHHHHHHHHH SEEKRIT"


class Question:
    """Question on a questionnaire."""

    def __init__(self, question, choices=None, allow_text=False):
        """Create question (assume Yes/No for choices."""

        if not choices:
            choices = ["Yes", "No"]

        self.question = question
        self.choices = choices
        self.allow_text = allow_text


class Survey:
    """Questionnaire."""

    def __init__(self, title, instructions, questions):
        """Create questionnaire."""

        self.title = title
        self.instructions = instructions
        self.questions = questions


satisfaction_survey = Survey(
    "Customer Satisfaction Survey",
    "Please fill out a survey about your experience with us.",
    [
        Question("Have you shopped here before?"),
        Question("Did someone else shop with you today?"),
        Question("On average, how much do you spend a month on frisbees?",
                 ["Less than $10,000", "$10,000 or more"]),
        Question("Are you likely to shop here again?"),
    ])

personality_quiz = Survey(
    "Rithm Personality Test",
    "Learn more about yourself with our personality quiz!",
    [
        Question("Do you ever dream about code?"),
        Question("Do you ever have nightmares about code?"),
        Question("Do you prefer porcupines or hedgehogs?",
                 ["Porcupines", "Hedgehogs"]),
        Question("Which is the worst function name, and why?",
                 ["do_stuff()", "run_me()", "wtf()"],
                 allow_text=True),
    ]
)

surveys = {
    "satisfaction": satisfaction_survey,
    "personality": personality_quiz,
}



responses = []

@app.route('/')
def get_home():
    return render_template('home.html',surveys=surveys)    

@app.route('/survey/<survey_name>')
def get_q(survey_name):
    # get which url and form
    if survey_name == 'satisfaction':
        return render_template('satisfaction.html',survey=satisfaction_survey)
    elif survey_name == 'personality':
        return render_template('personality.html',survey=personality_quiz)
    else: 
        return "no"


@app.route('/submit_survey', methods=['POST'])
def submit_survey():
    survey_name = request.form.get('question.question')
    survey = surveys.get(survey_name)
    answers = [request.form.get(question.question) for question in survey.questions]
    responses.append(answers)
    return render_template('show.html', responses=responses)


if __name__ == '__main__':
    app.run(debug=True)
#
#