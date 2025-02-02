import pandas as pd
import logging
import re
import os
import emoji

# Ensure logs folder exists
os.makedirs("../logs", exist_ok=True)

# Configure logging to write to file & display in Jupyter Notebook
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("../logs/data_cleaning.log", encoding='utf-8'),  # Log to file with UTF-8 encoding
        logging.StreamHandler()  # Log to Jupyter Notebook output
    ]
)

class MedicalDataCleaner:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = self.load_csv()

    def load_csv(self):
        """ Load CSV file into a Pandas DataFrame. """
        try:
            df = pd.read_csv(self.file_path)
            logging.info(f"✅ CSV file '{self.file_path}' loaded successfully.")
            return df
        except Exception as e:
            logging.error(f"❌ Error loading CSV file: {e}")
            raise

    def extract_emojis(self, text):
        """ Extract emojis from text, return 'No emoji' if none found. """
        emojis = ''.join(c for c in text if c in emoji.EMOJI_DATA)
        return emojis if emojis else "No emoji"

    def remove_emojis(self, text):
        """ Remove emojis from the message text. """
        return ''.join(c for c in text if c not in emoji.EMOJI_DATA)

    def extract_youtube_links(self, text):
        """ Extract YouTube links from text, return 'No YouTube link' if none found. """
        youtube_pattern = r"(https?://(?:www\.)?(?:youtube\.com|youtu\.be)/[^\s]+)"
        links = re.findall(youtube_pattern, text)
        return ', '.join(links) if links else "No YouTube link"

    def remove_youtube_links(self, text):
        """ Remove YouTube links from the message text. """
        youtube_pattern = r"https?://(?:www\.)?(?:youtube\.com|youtu\.be)/[^\s]+"
        return re.sub(youtube_pattern, '', text).strip()

    def clean_text(self, text):
        """ Standardize text by removing newline characters and unnecessary spaces. """
        if pd.isna(text):
            return "No Message"
        return re.sub(r'\n+', ' ', text).strip()

    def clean_dataframe(self):
        """ Perform all cleaning and standardization steps while avoiding SettingWithCopyWarning. """
        try:
            df = self.df.drop_duplicates(subset=["ID"]).copy()  # Ensure a new copy
            logging.info("✅ Duplicates removed from dataset.")

            # ✅ Convert Date to datetime format, replacing NaT with None
            df.loc[:, 'Date'] = pd.to_datetime(df['Date'], errors='coerce')
            df.loc[:, 'Date'] = df['Date'].where(df['Date'].notna(), None)
            logging.info("✅ Date column formatted to datetime.")

            # ✅ Convert 'ID' to integer for PostgreSQL BIGINT compatibility
            df.loc[:, 'ID'] = pd.to_numeric(df['ID'], errors="coerce").fillna(0).astype(int)

            # ✅ Fill missing values
            df.loc[:, 'Message'] = df['Message'].fillna("No Message")
            logging.info("✅ Missing values filled.")

            # ✅ Standardize text columns
            df.loc[:, 'Channel Title'] = df['Channel Title'].str.strip()
            df.loc[:, 'Channel Username'] = df['Channel Username'].str.strip()
            df.loc[:, 'Message'] = df['Message'].apply(self.clean_text)
            logging.info("✅ Text columns standardized.")

            # ✅ Extract emojis and store them in a new column
            df.loc[:, 'emoji_used'] = df['Message'].apply(self.extract_emojis)
            logging.info("✅ Emojis extracted and stored in 'emoji_used' column.")
            
            # ✅ Remove emojis from message text
            df.loc[:, 'Message'] = df['Message'].apply(self.remove_emojis)

            # ✅ Extract YouTube links into a separate column
            df.loc[:, 'youtube_links'] = df['Message'].apply(self.extract_youtube_links)
            logging.info("✅ YouTube links extracted and stored in 'youtube_links' column.")

            # ✅ Remove YouTube links from message text
            df.loc[:, 'Message'] = df['Message'].apply(self.remove_youtube_links)

            # ✅ Rename columns to match PostgreSQL schema
            df = df.rename(columns={
                "Channel Title": "channel_title",
                "Channel Username": "channel_username",
                "ID": "message_id",
                "Message": "message",
                "Date": "message_date",
                "emoji_used": "emoji_used",
                "youtube_links": "youtube_links"
            })

            logging.info("✅ Data cleaning completed successfully.")
            self.df = df
        except Exception as e:
            logging.error(f"❌ Data cleaning error: {e}")
            raise

    def save_cleaned_data(self, output_path):
        """ Save cleaned data to a new CSV file. """
        try:
            self.df.to_csv(output_path, index=False)
            logging.info(f"✅ Cleaned data saved successfully to '{output_path}'.")
            print(f"✅ Cleaned data saved successfully to '{output_path}'.")
        except Exception as e:
            logging.error(f"❌ Error saving cleaned data: {e}")
            raise