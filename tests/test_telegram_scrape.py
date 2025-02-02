import unittest
from unittest.mock import patch, MagicMock, mock_open
import os
import json
import logging
from telethon import TelegramClient
from telegram_scrape import get_last_processed_id, save_last_processed_id, scrape_channel, main

class TestTelegramScraper(unittest.TestCase):

    @patch('telegram_scrape.open', new_callable=mock_open, read_data='{"last_id": 123}')
    def test_get_last_processed_id(self, mock_file):
        channel_username = '@test_channel'
        last_id = get_last_processed_id(channel_username)
        self.assertEqual(last_id, 123)
        mock_file.assert_called_once_with(f"{channel_username}_last_id.json", 'r')

    @patch('telegram_scrape.open', new_callable=mock_open)
    def test_save_last_processed_id(self, mock_file):
        channel_username = '@test_channel'
        last_id = 123
        save_last_processed_id(channel_username, last_id)
        mock_file.assert_called_once_with(f"{channel_username}_last_id.json", 'w')
        mock_file().write.assert_called_once_with(json.dumps({'last_id': last_id}))

    @patch('telegram_scrape.TelegramClient')
    @patch('telegram_scrape.get_last_processed_id', return_value=0)
    @patch('telegram_scrape.save_last_processed_id')
    @patch('telegram_scrape.csv.writer')
    @patch('telegram_scrape.open', new_callable=mock_open)
    async def test_scrape_channel(self, mock_file, mock_csv_writer, mock_save_last_id, mock_get_last_id, mock_telegram_client):
        client = MagicMock()
        channel_username = '@test_channel'
        data_dir = 'test_data_dir'
        entity = MagicMock()
        entity.title = 'Test Channel'
        client.get_entity.return_value = entity
        message = MagicMock()
        message.id = 1
        message.message = 'Test message'
        message.date = '2025-02-02'
        client.iter_messages.return_value = [message]

        await scrape_channel(client, channel_username, data_dir)

        mock_file.assert_called_once_with(os.path.join(data_dir, f"{channel_username[1:]}_data.csv"), 'w', newline='', encoding='utf-8')
        mock_csv_writer().writerow.assert_any_call(['Channel Title', 'Channel Username', 'ID', 'Message', 'Date'])
        mock_csv_writer().writerow.assert_any_call(['Test Channel', '@test_channel', 1, 'Test message', '2025-02-02'])
        mock_save_last_id.assert_called_once_with(channel_username, 1)

    @patch('telegram_scrape.TelegramClient')
    @patch('telegram_scrape.os.makedirs')
    @patch('telegram_scrape.scrape_channel')
    @patch('telegram_scrape.load_dotenv')
    @patch('telegram_scrape.os.getenv', side_effect=['api_id', 'api_hash', 'phone_number'])
    async def test_main(self, mock_getenv, mock_load_dotenv, mock_scrape_channel, mock_makedirs, mock_telegram_client):
        client = MagicMock()
        mock_telegram_client.return_value = client

        await main()

        client.start.assert_called_once_with('phone_number')
        mock_makedirs.assert_called_once_with('../src/data/raw_data', exist_ok=True)
        self.assertEqual(mock_scrape_channel.call_count, 5)

if __name__ == "__main__":
    unittest.main()