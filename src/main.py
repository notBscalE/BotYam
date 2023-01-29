import tweepy
import os
import syslog
import consul
import json
from BotYamPoster import BotYamPoster
from BotYamPoster import init_streamobject


class Connector:
    conn_consul = set()
    api = set()

    def __init__(self):
        syslog.syslog(syslog.LOG_INFO, "Loading Consul connector...")
        # TODO: Add token
        conn_consul = consul.Consul(host='', port='')

        api = Connector.init_api(conn_consul)

    def init_api(conn_consul):
        # Syslog report
        syslog.syslog(syslog.LOG_INFO, "Loading Twitter API connector...")
        i, kv_keys = conn_consul.kv.get('botyam/api')

        return tweepy.Client(
            bearer_token=json.loads(kv_keys['Value']).bearer,
            consumer_key=json.loads(kv_keys['Value']).consumer_key,
            consumer_secret=json.loads(kv_keys['Value']).consumer_secret,
            access_token=json.loads(kv_keys['Value']).access_token,
            access_token_secret=json.loads(kv_keys['Value']).access_token_secret)

def main():
    syslog.syslog(syslog.LOG_INFO, "BOT-YAM - VERSION 2.1.2 >>>>")
    stream = init_streamobject()
    syslog.syslog(syslog.LOG_INFO, "Adding stream rules...")
    stream.add_rules(tweepy.StreamRule("from:LucyBscalE OR from:aviv_yashar OR from:shaulig OR from:DvirAviam OR from:YoavFried1 OR from:StevenRaz5 OR from:nir_hau"))
    stream.add_rules(tweepy.StreamRule("@FromBotYam"))
    # Start listening for tweets
    syslog.syslog(syslog.LOG_INFO, "Starting Twitter stream!")
    stream.filter(expansions="author_id")

if __name__ == "__main__":
    main()
