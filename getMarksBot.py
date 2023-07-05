import requests
import re
from config import login_url, username, password, mark_url


def extract_hidden_lt(text):
    pattern = r'<input type="hidden" name="lt" value="(.*?)" />'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    else:
        return None



def main(url, mark):
    session = requests.Session()

    request = session.get(url)
    lt = extract_hidden_lt(request.text)

    payload = {
        'username': username,
        'password': password,
        'lt': lt,
        'execution': 'e1s1',
        '_eventId': 'submit',
        'submit': 'ENTRAR'
    }

    r = session.post(url, data=payload)

    if r.status_code == 200:
        response = session.get(mark)
        print(response.status_code)

        return response.text


