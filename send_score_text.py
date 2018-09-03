from twilio.rest import Client

numbers_to_text = [
    '+13016534336'
    # ,'+12404296800'
    # ,'+12408390994'
    # ,'+13478615875'
    # ,'+13015805831'
]

stats = ['WIN', '4', 'WAS', '5', 'A1550']
home_team = stats[2]
home_score = stats[3]
away_team = stats[0]
away_score = stats[1]
id = stats[4]

if home_score > away_score:
    result = 'lost to'
elif home_score < away_score:
    result = 'beat'
else:
    result = 'tied with'

body = away_team + " just " + result + " " + home_team + ". The final score was " + away_score + " to " + home_score + ". " \
                                                                                                                       "The game id is " + id + ". Who was playing?\n\nPlease respond in the following format: *PLAYER* was *TEAM*." \
                                                                                                                                                "\n\nPlease send one text that tell me who was playing as each team."

account_sid = 'AC989cb3b03b930c5cf683f5e0e6d9c645'
auth_token = '25e2e56499efc7c427f8cb524184274b'
client = Client(account_sid, auth_token)

for number in numbers_to_text:
    message = client.messages.create(
        body=body,
        from_='+13013272522',
        to=number
    )
