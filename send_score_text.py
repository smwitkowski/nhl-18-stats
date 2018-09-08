from twilio.rest import Client
import re
import time


def connect_to_client(account_sid, acount_token):
    client = Client(account_sid, acount_token)
    return client


def send_EoG_text(numbers, stats, client):
    print(stats)
    home_team, away_team, home_score, away_score, id = stats
    time.sleep(5)
    messages = client.messages.list()

    if home_score > away_score:
        result = 'lost to'
    elif home_score < away_score:
        result = 'beat'
    else:
        result = 'tied with'

    body = away_team + " just " + result + " " + home_team + ". The final score was " + away_score + " to " + home_score + ". " \
                                                                                                                           "The game id is " + id + ". Who was playing?\n\nPlease respond in the following format: *PLAYER* was *TEAM*." \
                                                                                                                                                    "\n\nPlease send one text that tell me who was playing as each team."

    for number in numbers:
        message = client.messages.create(
            body=body,
            from_='+13013272522',
            to=number
        )

    while body == messages[0].body:
        time.sleep(5)
        messages = client.messages.list()
    return True


def verify_response(stats, client):
    home_team, away_team, home_score, away_score, id = stats
    messages = client.messages.list()
    home_regex = r'\w{1,}(?=( was ' + home_team + '))'
    away_regex = r'\w{1,}(?=( was ' + away_team + '))'

    body = "Please responsd in the form of *PLAYER* was *TEAM*." \
           "\n\n Use the team's abbreviation instead of the full name." \
           "\n\n Include both players in one text."

    message = messages[0].body
    home_detect = re.search(home_regex, message)
    away_detect = re.search(away_regex, message)
    if messages[0].from_ == '+13013272522':
        print('Message from Twilio.')
        time.sleep(5)
        return False
    elif not all([home_detect, away_detect]):
        print("Message not correct format.")
        message = client.messages.create(
            body=body,
            from_='+13013272522',
            to=messages[0].from_
        )
        time.sleep(5)
        return False
    else:
        message = client.messages.create(
            body="Thanks!",
            from_='+13013272522',
            to=messages[0].from_
        )
        print("Success!")
        time.sleep(5)
        return True


def find_players(stats, client):
    home_team, away_team, home_score, away_score, id = stats
    messages = client.messages.list()
    home_regex = r'(?i)\w{1,}(?=( was ' + home_team + '))'
    away_regex = r'(?i)\w{1,}(?=( was ' + away_team + '))'
    message = messages[1].body
    print(message)
    p1 = re.search(home_regex, message).group()
    p2 = re.search(away_regex, message).group()
    return p1, p2
