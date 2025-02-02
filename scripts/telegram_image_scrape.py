import logging
from telethon import TelegramClient
import os
import json
from dotenv import load_dotenv
from telethon.tl.types import MessageMediaPhoto

# Ensure logs folder exists
os.makedirs("../logs", exist_ok=True)

# Set up logging
logging.basicConfig(
    filename='../logs/scraping_images.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Load environment variables once
load_dotenv('.env')
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone_number = os.getenv('PHONE_NUMBER')

# Function to get last processed message ID
def get_last_processed_id(channel_username):
    try:
        with open(f"../src/data/last_id/{channel_username}_lastid_images.json", 'r') as f:
            return json.load(f).get('last_id', 0)
    except FileNotFoundError:
        logging.warning(f"No last ID file found for {channel_username}. Starting from 0.")
        return 0

# Function to save last processed message ID
def save_last_processed_id(channel_username, last_id):
    os.makedirs('../src/data/last_id', exist_ok=True)
    with open(f"../src/data/last_id/{channel_username}_lastid_images.json", 'w') as f:
        json.dump({'last_id': last_id}, f)
        logging.info(f"Saved last processed ID {last_id} for {channel_username}.")

# Function to scrape images from a single channel
async def scrape_images(client, channel_username, image_dir):
    try:
        entity = await client.get_entity(channel_username)
        last_id = get_last_processed_id(channel_username)
        
        # Limit to scraping only 100 messages
        async for message in client.iter_messages(entity, limit=100, reverse=True):
            if message.id <= last_id:
                continue
            
            if isinstance(message.media, MessageMediaPhoto):
                photo = message.media.photo
                file_path = os.path.join(image_dir, f"{message.id}.jpg")
                await client.download_media(photo, file_path)
                logging.info(f"Downloaded image {file_path} from {channel_username}.")
            
            last_id = message.id

        save_last_processed_id(channel_username, last_id)

    except Exception as e:
        logging.error(f"Error while scraping images from {channel_username}: {e}")

# Initialize the client once with a session file
client = TelegramClient('scraping_session', api_id, api_hash)

async def main():
    try:
        await client.start(phone_number)
        logging.info("Client started successfully.")
        
        # Directories to save images
        chemed123_dir = '../src/data/images/CheMed123_images'
        lobelia4cosmetics_dir = '../src/data/images/lobelia4cosmetics_images'
        os.makedirs(chemed123_dir, exist_ok=True)
        os.makedirs(lobelia4cosmetics_dir, exist_ok=True)

        # Channels to scrape images from
        channels = {
            '@CheMed123': chemed123_dir,
            '@lobelia4cosmetics': lobelia4cosmetics_dir
        }
        
        for channel, image_dir in channels.items():
            await scrape_images(client, channel, image_dir)
            logging.info(f"Scraped images from {channel}.")

    except Exception as e:
        logging.error(f"Error in main function: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())