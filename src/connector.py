import os
import redis
import time
import tweepy
from datetime import datetime

def printlog(text):
    print((datetime.fromtimestamp(time.time())).strftime("%d-%m-%Y, %H:%M:%S") + ": " + text)

class Connector():
    def __init__(self):
        printlog("Loading Redis connector...")
        # TODO: Add token
        self.dbconn = redis.Redis(
            host=os.getenv("REDIS_HOST"),
            port=os.getenv("REDIS_PORT"),
            password=os.getenv("REDIS_CREDENTIALS")
        )

        self.api = Connector.init_api(self.dbconn)
        printlog("Success loading connectors!")

    def init_api(dbconn):
        # Syslog report
        printlog("Loading Twitter API connector...")

        return tweepy.Client(
            bearer_token=dbconn.hget("api", "bearer").decode("utf-8"),
            consumer_key=dbconn.hget("api", "consumer_key").decode("utf-8"),
            consumer_secret=dbconn.hget("api", "consumer_secret").decode("utf-8"),
            access_token=dbconn.hget("api", "access_token").decode("utf-8"),
            access_token_secret=dbconn.hget("api","access_token_secret").decode("utf-8")
        )
    
    def get_reply_bank(self):
        return self.dbconn.json().get('reply_bank')
    
    def get_victims(self):
        return self.dbconn.json().get('reply_bank')['victims']
    
    def get_bearer(self):
        return self.dbconn.hget("api", "bearer").decode("utf-8")
