import os
import slack
from dotenv import load_dotenv
from pathlib import Path
from flask import Flask
from slackeventsapi import SlackEventAdapter
import re
import tweepy

env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'], '/slack/events', app)
SLACK_TOKEN = os.environ['SLACK_BOT_TOKEN']

client = slack.WebClient(token=os.environ['SLACK_BOT_TOKEN'])

BOT_ID = client.api_call("auth.test")['user_id']

@slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    z = client.conversations_info(token=SLACK_TOKEN, channel=channel_id)
    print(z)
    channel_name = z['channel']['name_normalized']
    user_id = event.get('user')
    x = client.users_info(token=SLACK_TOKEN, user=user_id)
    username = x['user']['name']
    text=event.get('text')
    msg=re.findall('.*-tweet.*', text)
    if BOT_ID != user_id and msg:
        client.chat_postMessage(channel=channel_id, text="You have posted a tweet :)")
        msg_string = text
        print(text)
        tweet(msg_string)


twitter_client =  tweepy.Client(os.environ['TWITTER_BEARER_TOKEN'], os.environ['TWITTER_API_KEY'], os.environ['TWITTER_API_SECRET'], os.environ['TWITTER_ACCESS_TOKEN'], os.environ['TWITTER_ACCESS_TOKEN_SECRET'])
def tweet(msg):
   twitter_client.create_tweet(text=msg)

if __name__ == "__main__":
    app.run(debug=True)