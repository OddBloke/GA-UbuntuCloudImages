import requests
from flask import Flask
from flask_assistant import Assistant, ask, tell
from num2words import num2words


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


def _speechify_serial(serial):
    year, month, dayish = serial[2:4], serial[4:6], serial[6:]
    if '.' in dayish:
        day, after_dot = dayish.split('.')
        parts = [
            num2words(int(part)) for part in [year, month, day, after_dot]]
        parts.insert(2, ',')
        parts.insert(1, ',')
        parts.insert(-1, 'dot')
        speech_serial = ' '.join(parts)
    else:
        speech_serial = ', '.join(
            num2words(int(part)) for part in [year, month, dayish])
    return 'twenty ' + speech_serial


@assist.action('find_latest_serial')
def find_latest_serial(ubuntu_release):
    serial = _find_latest_serial(ubuntu_release)
    if serial is None:
        text = speech = (
            "Sorry, I couldn't find any release serials for {}".format(
                ubuntu_release))
    else:
        template = "The latest {release} release serial on {site} is {serial}"
        text = template.format(release=ubuntu_release,
                               site='cloud-images.ubuntu.com',
                               serial=serial)
        speech_serial = _speechify_serial(serial)
        speech = template.format(release=ubuntu_release,
                                 site='cloud images.ubuntu.com',
                                 serial=speech_serial)
    return tell(speech, display_text=text)

if __name__ == '__main__':
    app.run(debug=True)
