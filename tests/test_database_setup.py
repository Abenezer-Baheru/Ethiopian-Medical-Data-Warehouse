import unittest
from unittest.mock import patch, MagicMock, mock_open
from sqlalchemy import create_engine, text
import pandas as pd
import os
import logging
from database_setup import get_db_connection, create_table, insert_data

class TestDatabaseSetup(unittest.TestCase):

    @patch('database_setup.create_engine')
    @patch('database_setup.os.getenv', side_effect=['localhost', 'test_db', 'user', 'password', '5432'])
    def test_get_db_connection(self, mock_getenv, mock_create_engine):
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine
        connection = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = connection

        engine = get_db_connection()
        mock_create_engine.assert_called_once_with('postgresql://user:password@localhost:5432/test_db')
        connection.execute.assert_called_once_with(text("SELECT 1"))
        self.assertEqual(engine, mock_engine)

    @patch('database_setup.create_engine')
    @patch('database_setup.text')
    def test_create_table(self, mock_text, mock_create_engine):
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine
        connection = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = connection

        create_table(mock_engine)
        connection.execute.assert_called_once_with(mock_text("""
            CREATE TABLE IF NOT EXISTS telegram_medical_messages (
                id SERIAL PRIMARY KEY,
                channel_title TEXT,
                channel_username TEXT,
                message_id BIGINT UNIQUE,
                message TEXT,
                message_date TIMESTAMP,
                emoji_used TEXT,
                youtube_links TEXT
            );
        """))

    @patch('database_setup.create_engine')
    @patch('database_setup.text')
    def test_insert_data(self, mock_text, mock_create_engine):
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine
        connection = MagicMock()
        mock_engine.begin.return_value.__enter__.return_value = connection

        cleaned_df = pd.DataFrame({
            'channel_title': ['Channel 1'],
            'channel_username': ['@channel1'],
            'message_id': [1],
            'message': ['Test message'],
            'message_date': ['2025-02-02'],
            'emoji_used': ['😊'],
            'youtube_links': ['https://youtu.be/dQw4w9WgXcQ']
        })

        insert_data(mock_engine, cleaned_df)
        connection.execute.assert_called_once_with(mock_text("""
            INSERT INTO telegram_medical_messages 
            (channel_title, channel_username, message_id, message, message_date, emoji_used, youtube_links) 
            VALUES (:channel_title, :channel_username, :message_id, :message, :message_date, :emoji_used, :youtube_links)
            ON CONFLICT (message_id) DO NOTHING;
        """), {
            'channel_title': 'Channel 1',
            'channel_username': '@channel1',
            'message_id': 1,
            'message': 'Test message',
            'message_date': '2025-02-02',
            'emoji_used': '😊',
            'youtube_links': 'https://youtu.be/dQw4w9WgXcQ'
        })

if __name__ == "__main__":
    unittest.main()
