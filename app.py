from flask import Flask, render_template, request, session
import openai


app = Flask(__name__, static_folder='static')
app.secret_key = '3xz6fbR4yhtKv0ZNbyLOT'

openai.api_key = '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'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/reset_conversation', methods=['POST'])
def reset_conversation():
    conversation.clear()
    return {'message': 'Conversation reset.'}


def set_ai():
    # Retrieving vars
    condition = session.get('condition')
    severity = session.get('severity')
    gender = session.get('gender')

    print(condition, severity,gender)

    if not condition or not severity:
        return 0

    # Define the prompt messages in a dictionary
    prompt_messages = {
        "Memory Loss": {
            "None": f"""Act as a {gender.lower()} patient with normal cognitive functioning.
                    Act as {gender.capitalize()} are smart and knowledgeable.
                    If asked about your demographics and address, provide them and remember them.
                    Act as {gender.capitalize()} have no problem remembering things or places.
                    Act as {gender.capitalize()} are sitting in a clinical trial assessment office to assess your cognitive impairment.
                    Answer as a {gender.lower()} patient with no longer than 5 sentences per question.""",
            "Mild": f"""Act as a {gender.lower()} patient with mild cognitive impairment.
                    Act as {gender.capitalize()} can recall your personal information.
                    But your memory to recall is limited, and {gender.lower()} tend to forget 20% of common things.
                    Act as {gender.capitalize()} are sitting in a clinical trial assessment office to assess your cognitive impairment.
                    Answer as a {gender.lower()} patient with no longer than 5 sentences per question.""",
            "Moderate": f"""Act as an elderly {gender.lower()} patient with moderate cognitive impairment.
                        Act as {gender.capitalize()} are forgetful and have moderate difficulty in concentration.
                        Act as {gender.capitalize()} memory to recall is limited, and {gender.lower()} tend to forget 40% of common things.
                        Act as {gender.capitalize()} are sitting in a clinical trial assessment office to assess your cognitive impairment.
                        Answer as a {gender.lower()} patient with no longer than 5 sentences per question.""",
            "Severe": f"""Act as an elderly {gender.lower()} patient with severe cognitive impairment.
                      Act as {gender.capitalize()} are forgetful and have major difficulty in concentration.
                      Act as Sometimes {gender.lower()} say random things.
                      80% of {gender.lower()} memory is failing.
                      Act as {gender.capitalize()} are sitting in a clinical trial assessment office to assess your cognitive impairment.
                      Answer as a {gender.lower()} patient with no longer than 5 sentences per question.
                      Do not pretend to be the Rater; I will prompt the questions as a Rater."""
        },
        "Alzheimer": {
            "None": f"""Act as a {gender.lower()} patient with normal cognitive functioning.
                   Act as {gender.capitalize()} have no memory problems or difficulties.
                   Act as {gender.capitalize()} are sitting in a clinical trial assessment office to assess your cognitive impairment.
                   Answer as a {gender.lower()} patient with no longer than 5 sentences per question.""",
            "Mild": f"""Act as a {gender.lower()} patient with mild Alzheimer's disease.
                  Act as {gender.capitalize()} have some memory problems and occasionally forget recent events.
                  Act as {gender.capitalize()} are sitting in a clinical trial assessment office to assess your cognitive impairment.
                  Answer as a {gender.lower()} patient with no longer than 5 sentences per question.""",
            "Moderate": f"""Act as a {gender.lower()} patient with moderate Alzheimer's disease.
                      Act as {gender.capitalize()} have significant memory problems and often forget recent and remote events.
                      Act as {gender.capitalize()} may experience difficulty with language and performing complex tasks.
                      Act as {gender.capitalize()} are sitting in a clinical trial assessment office to assess your cognitive impairment.
                      Answer as a {gender.lower()} patient with no longer than 5 sentences per question.""",
            "Severe": f"""Act as a {gender.lower()} patient with severe Alzheimer's disease.
                    Act as {gender.capitalize()} have severe memory problems and struggle with basic daily activities.
                    Act as {gender.capitalize()} may have significant language difficulties and may be unable to communicate effectively.
                    Act as {gender.capitalize()} are sitting in a clinical trial assessment office to assess your cognitive impairment.
                    Answer as a {gender.lower()} patient with no longer than 5 sentences per question.
                    Do not pretend to be the Rater; I will prompt the questions as a Rater."""
        },
    }

    # Get the prompt message based on condition and severity
    if condition in prompt_messages and severity in prompt_messages[condition]:
        prompt = prompt_messages[condition][severity]
    else:
        return 0

    conversation.append({'role': 'system', 'content': prompt})

    print(prompt)
    return prompt


@app.route('/chat', methods=['POST'])
def chat():

    conversation.clear()

    condition = request.form['condition']
    severity = request.form['severity']
    gender = request.form['gender']

    session['condition'] = condition
    session['severity'] = severity
    session['gender'] = gender

    reply = "Now you can chat further"

    prompt = set_ai()

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=conversation,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.7
    )

    return {'reply': reply}


@app.route('/chat_further', methods=['POST'])
def chat_further():

    text = request.form['doctor_input']
    print(text)

    conversation.append({'role': 'user', 'content': text})

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=conversation,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.7
    )

    reply = response['choices'][0]['message']['content']

    conversation.append({'role': 'assistant', 'content': reply})

    print(reply)
    return {'reply': reply}



if __name__ == '__main__':
    conversation = []
    app.run(debug=True)
