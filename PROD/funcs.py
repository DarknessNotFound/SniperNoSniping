import os
from dotenv import load_dotenv

load_dotenv()
CHANNEL_IDS = [os.getenv('PROD_SNIPING_CHANNEL_ID'),
              os.getenv('PROD_SNIPING_ADMIN_CHANNEL_ID'),
              os.getenv('PROD_BOT_TESTING_CHANNEL_ID') ]

def accessible_channel(ctx):
    if ctx.channel.id in CHANNEL_ID:
        return True
    else:
        return False
