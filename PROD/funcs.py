import os
from dotenv import load_dotenv

load_dotenv()
CHANNEL_IDS = [str(os.getenv('PROD_SNIPING_CHANNEL_ID')),
              str(os.getenv('PROD_SNIPING_ADMIN_CHANNEL_ID')),
              str(os.getenv('PROD_BOT_TESTING_CHANNEL_ID')) ]

def accessible_channel(ctx):
    return True
    try:
        print("Accessible channel called")
        if (ctx.channel.id in CHANNEL_IDS):
            print("Accessible channel returned true")
            return True
        else:
            print("Accessible channel returned false")
            return False
    except Exception as ex:
        print(f"funcs -- accessible_channel -- {ex}")

    finally:
        return False
