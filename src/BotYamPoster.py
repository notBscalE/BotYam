import tweepy
import random
import re
import requests
from connector import Connector

def init_streamobject(conn):
    print("Loading Stream object...")
    return BotYamPoster(conn.get_bearer())

def expand_tco_url(url):
    response = requests.head(url, allow_redirects=False)
    if 'location' in response.headers:
        return response.headers['location']
    else:
        return url

def post_reply(conn, victim_bank, tweet, words, reply_text_bank, postcounter):
    # Search for word in word bank
    if any(word in tweet.data['text'] for word in words):
        reply_text = reply_text_bank[random.randint(0, (len(reply_text_bank)-1))]
        # Post reply
        try:
            if tweet.data['author_id'] in victim_bank['author_id'] and not "@FromBotYam" in tweet.data['text']:
                reply_text = victim_bank['reply'][random.randint(0,2)] + "\nו" + reply_text
                res = conn.api.create_tweet(
                    text=reply_text,
                    in_reply_to_tweet_id=tweet["id"]
                )
        except tweepy.errors.TwitterServerError as e:
            print("ERROR: An error occured, we'll try again in a few minutes. The error: " + str(e))
            try:
                if tweet.data['author_id'] in victim_bank['author_id'] and not "@FromBotYam" in tweet.data['text']:
                    reply_text = victim_bank['reply'][random.randint(0,2)] + "\nו" + reply_text
                    res = conn.api.create_tweet(
                        text=reply_text,
                        in_reply_to_tweet_id=tweet["id"]
                    )
                
                response_data = f"RESPONDING: {res.data['text']}"
                print(response_data)
            except Exception as e:
                print("ERROR: An exception occured. The error: " + str(e))
        except Exception as e:
            print("ERROR: An exception occured. The error: " + str(e))
        postcounter = postcounter + 1
    return postcounter

class BotYamPoster(tweepy.StreamingClient):
    # Define a callback function to handle tweets
    def on_tweet(self, tweet):
        # Make it easy on Yashar

        postcounter = int(0)

        if (not "@FromBotYam" in tweet.data['text'] and random.randint(0,3) != 0):
            return
        
        # Don't use bot for own replies
        if tweet.data['author_id'] == "1604848395805401092":
            return
        
        conn = Connector()
        reply_bank = conn.get_reply_bank()

        # Debug
        tweet_data = f"NEW TWEET from @{conn.api.get_user(id=tweet.data['author_id']).data['username']}: {tweet.data['text']}"
        print(tweet_data)

        # Spare me if starts with RT
        if tweet.data['text'][:2] == "RT":
            print("Skipping retweet...")
            return
        
        # Run on all gags
        for gag in reply_bank['gags']:
            postcounter = post_reply(conn, reply_bank['victims'], tweet, gag['keywords'], gag['reply'], postcounter)
        
        # Special gags
        if reply_bank['special_gags']['haikar_misadot']['keywords'][0] in tweet.data["text"]:
            postcounter = post_reply(
                conn,
                reply_bank['victims'],
                tweet,
                reply_bank['special_gags']['haikar_misadot']['keywords'],
                reply_bank['special_gags']['haikar_misadot']['reply'],
                postcounter)
        elif not any(gebol in tweet.data['text'] for gebol in reply_bank['gags'][1]['keywords']) and any(misada in tweet.data['text'] for misada in reply_bank['special_gags']['misadot']['keywords']):
            postcounter = post_reply(
                conn,
                reply_bank['victims'],
                tweet,
                reply_bank['special_gags']['misadot']['keywords'],
                reply_bank['special_gags']['misadot']['reply'],
                postcounter)

        if (postcounter == 0 and "@FromBotYam" in tweet.data['text']):
            print("Post counter for this tweet: 0! Posting tilt.")

        if any(tilter in tweet.data['text'] for tilter in reply_bank['special_gags']['tilt']['keywords']):
            postcounter = post_reply(
                conn,
                reply_bank['victims'],
                tweet,
                reply_bank['special_gags']['tilt']['keywords'],
                reply_bank['special_gags']['tilt']['reply'],
                postcounter)
        
        if (postcounter == 0 and "@FromBotYam" in tweet.data['text']):
            postcounter = post_reply(
                conn,
                reply_bank['victims'],
                tweet,
                ['@FromBotYam'],
                reply_bank['special_gags']['tilt']['reply'],
                postcounter)

    # Define a callback function to handle errors
    def on_error(self, status_code):
        # Print the error code
        print("ERROR: " + status_code)
    
    def on_direct_message(self, message):
        # Check if the message is from the authenticated user
        if message['sender_id'] == self.user_id:
            return

        conn = Connector()

        # Get the text of the message
        text = message['text']

        # Find the URL of the tweet in the message
        tweet_url_regex = r'https?://twitter.com/\w+/status/(\d+)(?:\?.*)?$'
        tweet_url_match = re.search(tweet_url_regex, text)

        if not tweet_url_match:
            try:
                conn.api.send_direct_message(recipient_id=message['sender_id'], text="אין לי את הפונקציה הזאת עדיין סורי נשמה")
                print("Sent a message back - command unsupported.")
            except:
                print("Couldn't even send the message. Eef.")
            return

        tweet_id = tweet_url_match.group(1)

        # Get the tweet using the API
        tweet = conn.api.get_tweet(tweet_id)
        
        tco_regex = r'https?://t.co/\w+'
        tco_url = re.findall(tco_regex, tweet.data["text"])

        if not tco_url:
            try:
                conn.api.send_direct_message(recipient_id=message['sender_id'], text="אין פה סרטון או משהו שאפשר לפרש, זיבי ביי.")
                print("Sent a message back - command unsupported.")
            except:
                print("Couldn't even send the message, and no video in this tweet. Eef.")
            return

        videon_url = expand_tco_url(tco_url[0])

        # Create a response message with the tweet's text
        try:
            conn.api.send_direct_message(recipient_id=message['sender_id'], text="טוב ליסן, מצאתי פה קישור משהו לוקסוס. רק צריך להעתיק לפוסט, לדאוג שזה אחרון בפוסט, ויצא לך אמבד מושלם.")
            conn.api.send_direct_message(recipient_id=message['sender_id'], text=videon_url)
            print(f"SENT URL: {videon_url}")
        except:
            print(f"Sorry, couldn't send url {videon_url}")