import requests

url_ = "https://AC989cb3b03b930c5cf683f5e0e6d9c645:948b542ba4e995ce4ff9c68877a49c24@api.twilio.com/2010-04-01/Accounts/AC989cb3b03b930c5cf683f5e0e6d9c645/IncomingPhoneNumbers/PN2b7a6e9d7089edf4ce7197893d1e3432"

r = requests.post(url_, data={'SmsUrl': 'https://376680e8.ngrok.io'})
r
