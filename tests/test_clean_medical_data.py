import unittest
from unittest.mock import patch, MagicMock, mock_open
import pandas as pd
import os
import logging
from clean_medical_data import MedicalDataCleaner

class TestMedicalDataCleaner(unittest.TestCase):

    @patch('clean_medical_data.pd.read_csv')
    def test_load_csv(self, mock_read_csv):
        mock_read_csv.return_value = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
        file_path = 'test.csv'
        cleaner = MedicalDataCleaner(file_path)
        df = cleaner.load_csv()
        mock_read_csv.assert_called_once_with(file_path)
        self.assertEqual(df.shape, (2, 2))
        self.assertIn('col1', df.columns)
        self.assertIn('col2', df.columns)

    def test_extract_emojis(self):
        cleaner = MedicalDataCleaner('test.csv')
        text_with_emojis = "Hello 😊"
        text_without_emojis = "Hello"
        self.assertEqual(cleaner.extract_emojis(text_with_emojis), "😊")
        self.assertEqual(cleaner.extract_emojis(text_without_emojis), "No emoji")

    def test_remove_emojis(self):
        cleaner = MedicalDataCleaner('test.csv')
        text_with_emojis = "Hello 😊"
        text_without_emojis = "Hello"
        self.assertEqual(cleaner.remove_emojis(text_with_emojis), "Hello ")
        self.assertEqual(cleaner.remove_emojis(text_without_emojis), "Hello")

    def test_extract_youtube_links(self):
        cleaner = MedicalDataCleaner('test.csv')
        text_with_links = "Check this out: https://youtu.be/dQw4w9WgXcQ"
        text_without_links = "No links here"
        self.assertEqual(cleaner.extract_youtube_links(text_with_links), "https://youtu.be/dQw4w9WgXcQ")
        self.assertEqual(cleaner.extract_youtube_links(text_without_links), "No YouTube link")

    def test_remove_youtube_links(self):
        cleaner = MedicalDataCleaner('test.csv')
        text_with_links = "Check this out: https://youtu.be/dQw4w9WgXcQ"
        text_without_links = "No links here"
        self.assertEqual(cleaner.remove_youtube_links(text_with_links), "Check this out:")
        self.assertEqual(cleaner.remove_youtube_links(text_without_links), "No links here")

    def test_clean_text(self):
        cleaner = MedicalDataCleaner('test.csv')
        text_with_newlines = "Hello\nWorld"
        text_without_newlines = "Hello World"
        self.assertEqual(cleaner.clean_text(text_with_newlines), "Hello World")
        self.assertEqual(cleaner.clean_text(text_without_newlines), "Hello World")
        self.assertEqual(cleaner.clean_text(None), "No Message")

    @patch('clean_medical_data.pd.DataFrame.to_csv')
    def test_save_cleaned_data(self, mock_to_csv):
        cleaner = MedicalDataCleaner('test.csv')
        cleaner.df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
        output_path = 'cleaned.csv'
        cleaner.save_cleaned_data(output_path)
        mock_to_csv.assert_called_once_with(output_path, index=False)

    @patch('clean_medical_data.MedicalDataCleaner.load_csv')
    @patch('clean_medical_data.MedicalDataCleaner.clean_dataframe')
    @patch('clean_medical_data.MedicalDataCleaner.save_cleaned_data')
    def test_main(self, mock_save_cleaned_data, mock_clean_dataframe, mock_load_csv):
        file_path = 'test.csv'
        output_path = 'cleaned.csv'
        cleaner = MedicalDataCleaner(file_path)
        cleaner.clean_dataframe()
        cleaner.save_cleaned_data(output_path)
        mock_load_csv.assert_called_once()
        mock_clean_dataframe.assert_called_once()
        mock_save_cleaned_data.assert_called_once_with(output_path)

if __name__ == "__main__":
    unittest.main()
