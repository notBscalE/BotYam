import os
import syslog
import json
import redis
import tweepy

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
            bearer_token=dbconn.hget("api", "bearer").decode("utf-8"),
            consumer_key=dbconn.hget("api", "consumer_key").decode("utf-8"),
            consumer_secret=dbconn.hget("api", "consumer_secret").decode("utf-8"),
            access_token=dbconn.hget("api", "access_token").decode("utf-8"),
            access_token_secret=dbconn.hget("api","access_token_secret").decode("utf-8")
        )
    
    def get_reply_bank(self):
        return json.loads(self.dbconn.get('reply_bank').decode("utf-8"))
    
    def get_victims(self):
        return json.loads(self.dbconn.get('reply_bank').decode("utf-8")).victims
    
    def get_bearer(self):
        return self.dbconn.hget("api", "bearer").decode("utf-8")
