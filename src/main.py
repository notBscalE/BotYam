import tweepy
import os
import syslog
import json
import redis
from BotYamPoster import BotYamPoster
from BotYamPoster import init_streamobject


class Connector():
    def __init__(self):
        syslog.syslog(syslog.LOG_INFO, "Loading Consul connector...")
        # TODO: Add token
        self.dbconn = redis.Redis(
            host=os.getenv("REDIS_HOST"),
            port=os.getenv("REDIS_PORT"),
            password=os.getenv("REDIS_CREDENTIALS")
        )

        self.api = Connector.init_api(self.dbconn)

    def init_api(dbconn):
        # Syslog report
        syslog.syslog(syslog.LOG_INFO, "Loading Twitter API connector...")

        return tweepy.Client(
            bearer_token=str(dbconn.hget("api", "bearer")),
            consumer_key=str(dbconn.hget("api", "consumer_key")),
            consumer_secret=str(dbconn.hget("api", "consumer_secret"))
            access_token=str(dbconn.hget("api", "access_token")),
            access_token_secret=str(dbconn.hget("api","access_token_secret"))
        )
    
    def get_reply_bank(self):
        return json.loads(self.dbconn.get('reply_bank'))
    
    def get_victims(self):
        return json.loads(self.dbconn.get('reply_bank')).victims
    
    def get_bearer(self):
        return str(self.dbconn.hget("api", "bearer"))

def main():
    syslog.syslog(syslog.LOG_INFO, "BOT-YAM - VERSION 2.1.2 >>>>")
    conn = Connector()
    stream = init_streamobject(conn)
    syslog.syslog(syslog.LOG_INFO, "Adding stream rules...")
    stream.add_rules(tweepy.StreamRule(conn.get_victims().stream_filter))
    stream.add_rules(tweepy.StreamRule("@FromBotYam"))
    # Start listening for tweets
    syslog.syslog(syslog.LOG_INFO, "Starting Twitter stream!")
    stream.filter(expansions="author_id")

if __name__ == "__main__":
    main()
