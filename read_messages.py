from twilio.rest import Client
import re

account_sid = 'AC989cb3b03b930c5cf683f5e0e6d9c645'
auth_token = '25e2e56499efc7c427f8cb524184274b'
client = Client(account_sid, auth_token)

stats = ['WIN', '4', 'WAS', '5', 'A1550']
home_team = stats[2]
home_regex = r'\w{1,}(?=( was ' + home_team + '))'
home_score = stats[3]
away_team = stats[0]
away_regex = r'\w{1,}(?=( was ' + away_team + '))'
away_score = stats[1]
id = stats[4]

messages = client.messages.list()

idx = [idx for idx, s in enumerate(messages) if id in s.body][0]
if idx != 0:
    team_assignment_text = messages[idx - 1].body
    home_player = re.search(home_regex, team_assignment_text)
    away_player = re.search(away_regex, team_assignment_text)

    if home_player is None and away_player is None:
        print("Use the following format:")
        print("*HOME PLAYER* was *TEAM*. *AWAY PLAYER* was *TEAM*")
    elif home_player is None:
        print("Please specific a home player.")
        print("Use the following format:")
        print("*PLAYER* was *TEAM*.")
    elif away_player is None:
        print("Please specific a away player.")
        print("Use the following format:")
        print("*PLAYER* was *TEAM*.")
