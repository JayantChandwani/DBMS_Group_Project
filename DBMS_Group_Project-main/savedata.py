import json


def read_file():
    with open('login_state.txt') as login_file:
        data = json.load(login_file)
        return data


def update_file(login_state, otp = None):
    data = [login_state, otp]
    with open('login_state.txt', 'w') as login_file:
        json.dump(data, login_file)
        
def update_email_file(email):
    with open('email_file.txt', 'w') as email_file:
        json.dump(email, email_file)

def get_email():
    with open('email_file.txt') as email_file:
        return json.load(email_file)