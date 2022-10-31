import os
from dotenv import load_dotenv

load_dotenv()
CHANNEL_ID = os.getenv('CHANNEL_ID')

def accessible_channel(ctx):
    if ctx.channel.id is not CHANNEL_ID:
        return True
    else:
        return False
