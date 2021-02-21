# Green Belt Tracker Telegram Bot
This is a [Telegram Bot](https://core.telegram.org/bots) that will tell me how far away I am from the [German Green Belt](https://en.wikipedia.org/wiki/German_Green_Belt) and how much of it i've already completed on my hike alongside it.

## Setup
1. Create a new Telegram Bot using [BotFather](https://t.me/botfather).
1. Copy the `config.example.py` into `config.py` and adapt at least the values for `bot_token` and `user_id_list` (use the [IDBot](https://telegram.me/myidbot) to get your own user ID)
1. Install the project's requirements using
```
$ pip install -r requirements.txt
```

## Run
Run the bot using
```
$ python3 green-belt-tracker.py
```

## To Do
* Make the bot capable of using arbitrary GPX tracks