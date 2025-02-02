import unittest
from unittest.mock import patch, MagicMock, mock_open
import pandas as pd
import os
import logging
from merge_medical_data import load_csv, save_merged_data, main

class TestMergeMedicalData(unittest.TestCase):

    @patch('merge_medical_data.pd.read_csv')
    def test_load_csv(self, mock_read_csv):
        mock_read_csv.return_value = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
        file_path = 'test.csv'
        df = load_csv(file_path)
        mock_read_csv.assert_called_once_with(file_path)
        self.assertEqual(df.shape, (2, 2))
        self.assertIn('col1', df.columns)
        self.assertIn('col2', df.columns)

    @patch('merge_medical_data.pd.DataFrame.to_csv')
    def test_save_merged_data(self, mock_to_csv):
        df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
        output_path = 'merged.csv'
        save_merged_data(df, output_path)
        mock_to_csv.assert_called_once_with(output_path, index=False)

    @patch('merge_medical_data.load_csv')
    @patch('merge_medical_data.save_merged_data')
    @patch('merge_medical_data.pd.concat')
    @patch('merge_medical_data.os.path.join', side_effect=lambda *args: '/'.join(args))
    @patch('merge_medical_data.os.makedirs')
    def test_main(self, mock_makedirs, mock_path_join, mock_concat, mock_save_merged_data, mock_load_csv):
        mock_load_csv.return_value = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
        mock_concat.return_value = pd.DataFrame({'col1': [1, 2, 1, 2], 'col2': [3, 4, 3, 4]})
        
        main()
        
        self.assertEqual(mock_load_csv.call_count, 5)
        mock_concat.assert_called_once()
        mock_save_merged_data.assert_called_once()
        mock_makedirs.assert_called_once_with('../logs', exist_ok=True)

if __name__ == "__main__":
    unittest.main()