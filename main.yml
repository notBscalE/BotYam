import tweepy
import os
import syslog

# Secrets
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
bearer = os.getenv("BEARER")

# Syslog report
syslog.syslog(syslog.LOG_INFO, "Loading objects...")

# Twitter API
api = tweepy.Client(
    bearer_token=bearer,
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret)

def post_reply(api, tweet, words, reply_text):
    # Search for word in word bank
    if any(word in tweet.data['text'] for word in words):
        # Post reply
        res = api.create_tweet(
              text=reply_text,
              in_reply_to_tweet_id=tweet["id"]
        )
        response_data = "RESPONDING: {}".format(res.data['text'])
        syslog.syslog(syslog.LOG_INFO, response_data)

# Poster class
class BotYamPoster(tweepy.StreamingClient):
    # Define a callback function to handle tweets
    def on_tweet(self, tweet):
        # Debug
        tweet_data = "NEW TWEET from @{}: {}".format(api.get_user(id=tweet.data['author_id']).data['username'], tweet.data['text'])
        syslog.syslog(syslog.LOG_INFO, tweet_data)

        # Spare me if starts with RT
        if tweet.data['text'][:2] == "RT":
            syslog.syslog(syslog.LOG_INFO, "Skipping retweet...")
            return

        # Words bank
        bat_yam_words = ['בת ים', 'בת ימ', 'בת-ים', 'בת-ימ']
        gebels_words = ['גבלס', 'נאצי', 'היטלר', 'קורונה', 'מסמכים', 'ההסמכה']
        police_words = ['שוטר', 'מלשין', 'מלשינ', 'נלשן', 'מלשנ', 'להלשין', 'משטרה', 'משטרות', 'סירנה', 'שיטור', 'בוגדים', 'בוגד', 'בגידה', 'שמאל', '0מול', 'סמול', '👮‍♀️', '🚨', '🚔', '🚓', '👮‍♂️', 'קטטה', 'מתקוטט', 'משטרע', 'מאפיה', 'טרור', 'סירנות', '1312', '13.12', '1 3 1 2', '13 12', '1 312', '131 2', '13-12', '1-312', '131-2', '1-3-1-2', '1 3 12', '1 3 12', '13 1 2', '1-3-12', '1-3-12', '13-1-2', 'acab', 'ac ab', 'ACAB', 'AC AB', 'אגאב', 'קצין', 'קצינ', 'קצונה', 'צהוב', 'כחול']
        misadot_words = ['מסעדה', 'מסעדות']
        
        # Reply bank
        reply_text_batyam = "https://twitter.com/FromBotYam/status/1611546128524185601/video/1"
        reply_text_police = "https://twitter.com/FromBotYam/status/1611542331781529601/video/1"
        reply_text_gebels = "https://twitter.com/FromBotYam/status/1611548817853227009/video/1"
        reply_text_misadot = [reply_text_gebels, "https://twitter.com/FromBotYam/status/1612853363066175490/video/1"]
       
        # Users bank
        batyam_folks = ['134339937', '1533213104']

        post_reply(api, tweet, gebels_words, reply_text_gebels)
        post_reply(api, tweet, police_words, reply_text_police)
        if any(botyam_og in tweet.data['author_id'] for botyam_og in batyam_folks):
            post_reply(api, tweet, bat_yam_words, reply_text_batyam)
        if not any(gebels_word in tweet.data['text'] for gebels_word in gebels_words):
            post_reply(api, tweet, misadot_words, reply_text_misadot[random.randint(0,1)])

    # Define a callback function to handle errors
    def on_error(self, status_code):
        # Print the error code
        syslog.syslog(syslog.LOG_ERR, status_code)

# Set Stream rules
stream = BotYamPoster(bearer)
stream.add_rules(tweepy.StreamRule("from:LucyBscalE OR from:aviv_yashar OR from:shaulig OR from:DvirAviam OR from:YoavFried1 OR from:StevenRaz5"))
# Start listening for tweets
syslog.syslog(syslog.LOG_INFO, "Starting Twitter stream!")
stream.filter(expansions="author_id")
