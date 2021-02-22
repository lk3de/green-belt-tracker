#!/usr/bin/env python3
import logging

# Paste your bot secret here
bot_token = 'my-super-secret-token'

# Only the users in this list can use the bot
user_id_list = [
    123456789,      # User A
    987654321       # User B
]

# GPX configuration
gpx_file = 'green-belt-germany.gpx'
max_distance_meter = 10000

# Logging configuration
log_level = logging.DEBUG