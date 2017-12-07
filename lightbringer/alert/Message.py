from slackclient import SlackClient

class Message():
    def __init__(self):
        slack_token = 'xoxp-257787694487-256522599297-271103305072-997e95878b04cf715b010d45af2abe79'
        self.slack = SlackClient(slack_token)
        
    def sendSlack(self, msg, channel, bullish = True):
        face = '\n:o:\n'
        if bullish:
            face = '\n:train:\n'
        msg = face + msg + '\n:tada:'
        self.slack.api_call(
          "chat.postMessage",
          channel=channel,
          username='ALERTBOT',
          text=msg,
          icon_emoji=':ninja:'
        )
