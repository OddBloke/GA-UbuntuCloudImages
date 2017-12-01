import requests
from flask import Flask
from flask_assistant import Assistant, ask, tell


DOWNLOAD_STREAMS = (
    'http://cloud-images.ubuntu.com'
    '/releases/streams/v1/com.ubuntu.cloud:released:download.json')

app = Flask(__name__)
assist = Assistant(app)


@assist.prompt_for('ubuntu_release', intent_name='find_latest_serial')
def prompt_ubuntu_release(ubuntu_release):
    speech = "I'm sorry, which Ubuntu release?"
    return ask(speech)


def _find_latest_serial(ubuntu_release):
    response = requests.get(DOWNLOAD_STREAMS)
    for product_dict in response.json()['products'].values():
        if product_dict['release'] == ubuntu_release:
            serials = product_dict['versions'].keys()
            latest_serial = None
            for serial in serials:
                if latest_serial is None:
                    latest_serial = serial
                    continue
                if serial > latest_serial:
                    latest_serial = serial
            return latest_serial
    return None


@assist.action('find_latest_serial')
def find_latest_serial(ubuntu_release):
    serial = _find_latest_serial(ubuntu_release)
    if serial is None:
        speech = "Sorry, I couldn't find any release serials for {}".format(
            ubuntu_release)
    else:
        speech = (
            "The latest {} release serial on cloud-images.ubuntu.com is"
            " {}".format(ubuntu_release, serial))
    return tell(speech)

    return tell(speech, display_text=text)

if __name__ == '__main__':
    app.run(debug=True)
