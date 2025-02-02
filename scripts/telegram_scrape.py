import logging
from telethon import TelegramClient
import csv
import os
import json
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(
    filename='scraping.log',
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
        with open(f"{channel_username}_last_id.json", 'r') as f:
            return json.load(f).get('last_id', 0)
    except FileNotFoundError:
        logging.warning(f"No last ID file found for {channel_username}. Starting from 0.")
        return 0

# Function to save last processed message ID
def save_last_processed_id(channel_username, last_id):
    with open(f"{channel_username}_last_id.json", 'w') as f:
        json.dump({'last_id': last_id}, f)
        logging.info(f"Saved last processed ID {last_id} for {channel_username}.")

# Function to scrape data from a single channel
async def scrape_channel(client, channel_username, data_dir):
    try:
        entity = await client.get_entity(channel_username)
        channel_title = entity.title
        
        last_id = get_last_processed_id(channel_username)
        
        # Limit to scraping only 1000 messages
        messages = []
        async for message in client.iter_messages(entity, limit=1000, reverse=True):
            if message.id <= last_id:
                continue
            messages.append(message)
        
        filename = os.path.join(data_dir, f"{channel_username[1:]}_data.csv")
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Channel Title', 'Channel Username', 'ID', 'Message', 'Date'])
            for message in reversed(messages):
                writer.writerow([channel_title, channel_username, message.id, message.message, message.date])
                logging.info(f"Processed message ID {message.id} from {channel_username}.")
                last_id = message.id

        save_last_processed_id(channel_username, last_id)

        if not messages:
            logging.info(f"No new messages found for {channel_username}.")

    except Exception as e:
        logging.error(f"Error while scraping {channel_username}: {e}")

# Initialize the client once with a session file
client = TelegramClient('scraping_session', api_id, api_hash)

async def main():
    try:
        await client.start(phone_number)
        logging.info("Client started successfully.")
        
        data_dir = '../src/data/raw_data'
        os.makedirs(data_dir, exist_ok=True)

        channels = [
            '@DoctorsET',
            '@CheMed123',
            '@lobelia4cosmetics',
            '@yetenaweg',
            '@EAHCI'
        ]
        
        for channel in channels:
            await scrape_channel(client, channel, data_dir)
            logging.info(f"Scraped data from {channel}.")

    except Exception as e:
        logging.error(f"Error in main function: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())