import tweepy
import os
import syslog
import random
import json
from connector import Connector

def init_streamobject(conn):
    syslog.syslog(syslog.LOG_INFO, "Loading Stream object...")
    return BotYamPoster(conn.get_bearer())

def post_reply(conn, victim_bank, tweet, words, reply_text_bank, postcounter):
    # Search for word in word bank
    if any(word in tweet.data['text'] for word in words):
        reply_text = reply_text_bank[random.randint(0, (reply_text_bank.len()-1))]
        # Post reply
        if tweet.data['author_id'] in victim_bank.author_id:
            reply_text = victim_bank.text[random.randint(0,2)] + "\n" + reply_text
        res = conn.api.create_tweet(
              text=reply_text,
              in_reply_to_tweet_id=tweet["id"]
        )
        response_data = f"RESPONDING: {res.data['text']}"
        syslog.syslog(syslog.LOG_INFO, response_data)
        return (postcounter + 1)

class BotYamPoster(tweepy.StreamingClient):

    # Define a callback function to handle tweets
    def on_tweet(self, tweet):
        # Make it easy on Yashar

        postcounter = 0

        if (not "@FromBotYam" in tweet.data['text'] and random.randint(0,3) != 0):
            return
        
        # Don't use bot for own replies
        if tweet.data['author_id'] == "1604848395805401092":
            return
        
        conn = Connector()
        reply_bank = json.loads(conn.dbconn.get_reply_bank())

        # Debug
        tweet_data = f"NEW TWEET from @{conn.api.get_user(id=tweet.data['author_id']).data['username']}: {tweet.data['text']}"
        syslog.syslog(syslog.LOG_INFO, tweet_data)

        # Spare me if starts with RT
        if tweet.data['text'][:2] == "RT":
            syslog.syslog(syslog.LOG_INFO, "Skipping retweet...")
            return
        
        # Run on all gags
        for gag in reply_bank.gags:
            postcounter = post_reply(conn, reply_bank.victims, tweet, gag.keywords, gag.reply, postcounter)
        
        # Special gags
        if reply_bank.special_gags['haikar_misadot'].keywords[0] in tweet.data["text"]:
            postcounter = post_reply(
                conn,
                reply_bank.victims,
                tweet,
                reply_bank.special_gags['haikar_misadot'].keywords,
                reply_bank.special_gags['haikar_misadot'].reply,
                postcounter)
        elif not any(gebol in tweet.data['text'] for gebol in reply_bank.gags[1].keywords) and any(misada in tweet.data['text'] for misada in reply_bank.special_gags['misadot'].keywords):
            postcounter = post_reply(
                conn,
                reply_bank.victims,
                tweet,
                reply_bank.special_gags['misadot'].keywords,
                reply_bank.special_gags['misadot'].reply,
                postcounter)
        
        if any(tilter in tweet.data['text'] for tilter in reply_bank.special_gags['tilt'].keywords) or (postcounter == 0 and "@FromBotYam" in tweet.data['text']):
            postcounter = post_reply(
                conn,
                reply_bank.victims,
                tweet, reply_bank.special_gags['tilt'].keywords,
                reply_bank.special_gags['tilt'].reply,
                postcounter)

    # Define a callback function to handle errors
    def on_error(self, status_code):
        # Print the error code
        syslog.syslog(syslog.LOG_ERR, status_code)
