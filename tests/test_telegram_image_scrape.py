import unittest
from unittest.mock import patch, MagicMock, mock_open
import os
import json
import logging
from telethon import TelegramClient
from telegram_image_scrape import get_last_processed_id, save_last_processed_id, scrape_images, main

class TestTelegramImageScraper(unittest.TestCase):

    @patch('telegram_image_scrape.open', new_callable=mock_open, read_data='{"last_id": 123}')
    def test_get_last_processed_id(self, mock_file):
        channel_username = '@test_channel'
        last_id = get_last_processed_id(channel_username)
        self.assertEqual(last_id, 123)
        mock_file.assert_called_once_with(f"../src/data/last_id/{channel_username}_lastid_images.json", 'r')

    @patch('telegram_image_scrape.open', new_callable=mock_open)
    def test_save_last_processed_id(self, mock_file):
        channel_username = '@test_channel'
        last_id = 123
        save_last_processed_id(channel_username, last_id)
        mock_file.assert_called_once_with(f"../src/data/last_id/{channel_username}_lastid_images.json", 'w')
        mock_file().write.assert_called_once_with(json.dumps({'last_id': last_id}))

    @patch('telegram_image_scrape.TelegramClient')
    @patch('telegram_image_scrape.get_last_processed_id', return_value=0)
    @patch('telegram_image_scrape.save_last_processed_id')
    @patch('telegram_image_scrape.os.path.join', return_value='test_path')
    @patch('telegram_image_scrape.os.makedirs')
    @patch('telegram_image_scrape.client.download_media')
    async def test_scrape_images(self, mock_download_media, mock_makedirs, mock_path_join, mock_save_last_id, mock_get_last_id, mock_telegram_client):
        client = MagicMock()
        channel_username = '@test_channel'
        image_dir = 'test_image_dir'
        entity = MagicMock()
        client.get_entity.return_value = entity
        message = MagicMock()
        message.id = 1
        message.media = MagicMock(spec=MessageMediaPhoto)
        client.iter_messages.return_value = [message]

        await scrape_images(client, channel_username, image_dir)

        mock_download_media.assert_called_once_with(message.media.photo, 'test_path')
        mock_save_last_id.assert_called_once_with(channel_username, 1)

    @patch('telegram_image_scrape.TelegramClient')
    @patch('telegram_image_scrape.os.makedirs')
    @patch('telegram_image_scrape.scrape_images')
    @patch('telegram_image_scrape.load_dotenv')
    @patch('telegram_image_scrape.os.getenv', side_effect=['api_id', 'api_hash', 'phone_number'])
    async def test_main(self, mock_getenv, mock_load_dotenv, mock_scrape_images, mock_makedirs, mock_telegram_client):
        client = MagicMock()
        mock_telegram_client.return_value = client

        await main()

        client.start.assert_called_once_with('phone_number')
        mock_makedirs.assert_any_call('../src/data/images/CheMed123_images', exist_ok=True)
        mock_makedirs.assert_any_call('../src/data/images/lobelia4cosmetics_images', exist_ok=True)
        self.assertEqual(mock_scrape_images.call_count, 2)

if __name__ == "__main__":
    unittest.main()