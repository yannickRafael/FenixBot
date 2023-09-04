from datetime import datetime as dt
from config import feedback_ref

def register_feedback(feedback, number):

    data = {
        'msisdn': number,
        'date': str(dt.now().strftime("%Y-%m-%d %H:%M")),
        'description': feedback,
        'status': ''
    }

    feedback_ref.push(data)
    print(data)


