from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)


@app.route('/sms', methods=['GET', 'POST'])
def sms_ahoy_reply():
    resp = MessagingResponse()
    message = Message()

    resp.message("Thanks for your message!")
    print(message.body())
    return (str(resp))


if __name__ == ("__main__"):
    app.run(debug=True)
