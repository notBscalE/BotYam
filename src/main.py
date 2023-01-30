import sys
import tweepy
from BotYamPoster import BotYamPoster
from BotYamPoster import init_streamobject
from connector import Connector

def main():
    print("BOT-YAM - VERSION 2.1.2 >>>>")
    conn = Connector()
    stream = init_streamobject(conn)
    print("Adding stream rules...")
    stream.add_rules(tweepy.StreamRule(conn.get_victims()['stream_filter']))
    stream.add_rules(tweepy.StreamRule("@FromBotYam"))
    # Start listening for tweets
    print("Starting Twitter stream!")
    stream.filter(expansions="author_id")

if __name__ == "__main__":
    main()
