from flask import Flask
from flask_assistant import Assistant, ask, tell

app = Flask(__name__)
assist = Assistant(app)


@assist.prompt_for('ubuntu_release', intent_name='find_latest_serial')
def prompt_ubuntu_release(ubuntu_release):
    speech = "I'm sorry, which Ubuntu release?"
    return ask(speech)


@assist.action('find_latest_serial')
def find_latest_serial(ubuntu_release):
    speech = "You asked about {}".format(ubuntu_release)
    return tell(speech)

if __name__ == '__main__':
    app.run(debug=True)
