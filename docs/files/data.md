# Data for nerds

!!! note
    Before contributing, read the [license](license.md).

Here you have something to get, if you want to participate in the coding and somehow you got included - congrats! You are in.
Here are the basic knowledge stuff.

## Where is the data coming from?

In the `connector.py` file, you'll find that we use Redis as our DB of choice.

The DB is used for storing everything in stores, as its credentials are currently stored inside the machine itself - with a certain hope to bring it up as a k8s secret, when the chance is given.

## API Tokens
The API tokens are stored in the API hash, used to communicate with Twitter API.

!!! warning "Twitter API License Changes"
    Currently, the bot is operating under the Twitter API Elevated Access.<br>On February 9th, new changes for the API access that has been announced will come into effect, and currently there isn't a guarantee that the bot will be up after the changes will be applied.<br>
    Please follow `@FromBotYam` for updates.

## The Data Structure

The current data structure is going as follows:
```json
{
    "id": "gag_name",
    "keywords": ["1", "2"],
    "reply": ["https://www.twitter.com/FromBotYam/status/{{status_id}}/video/1"]
}
```

Special gags (as being described in the "Specia Gags" section in `BotYamPoster.py`) have different kind of treatment, although the data structure is pretty much the same.<br>
Unlike the special gags, all the gags are stored in the reply_bank json key under `gags`.

## Victims

The victims list is built as follows:
```json
{
    "stream_filter": "from:Victim1 OR from:Victim2 OR from:Victim3",
    "author_id": ["id1", "id2", "id3"],
    "reply": ["added text 1", "added text 2", "added text 3"]
}
```
`stream_filter` is the actual filter used for the Twitter API Stream, to follow the victims as they post.<br>
`author_id` is the list of Twitter IDs, representing the victims' users.<br>
`reply` is the list of the possible added text.

The list of the users affected, and the possible replies, are all described in the [User Guide](usage.md).
