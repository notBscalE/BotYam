import sys
import tweepy
import time
from BotYamPoster import BotYamPoster
from BotYamPoster import init_streamobject
from connector import Connector
from connector import printlog

def main():
    printlog("BOT-YAM - VERSION 3.0.2 >>>>")
    conn = Connector()
    stream = init_streamobject(conn)
    printlog("Adding stream rules...")
    stream.add_rules(tweepy.StreamRule(conn.get_victims()['stream_filter']))
    stream.add_rules(tweepy.StreamRule("@FromBotYam"))
    # Start listening for tweets
    printlog("Starting Twitter stream!")
    stream.filter(expansions="author_id")

if __name__ == "__main__":
    main()
