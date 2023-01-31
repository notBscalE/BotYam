import tweepy
import random
from connector import Connector

def init_streamobject(conn):
    print("Loading Stream object...")
    return BotYamPoster(conn.get_bearer())

def post_reply(conn, victim_bank, tweet, words, reply_text_bank, postcounter):
    # Search for word in word bank
    if any(word in tweet.data['text'] for word in words):
        reply_text = reply_text_bank[random.randint(0, (len(reply_text_bank)-1))]
        # Post reply
        if tweet.data['author_id'] in victim_bank['author_id'] and not "@FromBotYam" in tweet.data['text']:
            reply_text = victim_bank['reply'][random.randint(0,2)] + "\nו" + reply_text
        res = conn.api.create_tweet(
              text=reply_text,
              in_reply_to_tweet_id=tweet["id"]
        )
        postcounter = postcounter + 1
        response_data = f"RESPONDING: {res.data['text']}"
        print(response_data)
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

        if (postcounter == 0):
            print("Post counter for this tweet: 0! Posting tilt.")

        if any(tilter in tweet.data['text'] for tilter in reply_bank['special_gags']['tilt']['keywords']) or (postcounter == 0 and "@FromBotYam" in tweet.data['text']):
            postcounter = post_reply(
                conn,
                reply_bank['victims'],
                tweet, reply_bank['special_gags']['tilt']['keywords'],
                reply_bank['special_gags']['tilt']['reply'],
                postcounter)

    # Define a callback function to handle errors
    def on_error(self, status_code):
        # Print the error code
        print("ERROR: " + status_code)
