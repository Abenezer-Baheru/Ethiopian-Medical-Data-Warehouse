import pandas as pd
import logging
import os

# Ensure logs folder exists
os.makedirs("../logs", exist_ok=True)

# Configure logging to write to file & display in Jupyter Notebook
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("../logs/data_merging.log", encoding='utf-8'),  # Log to file with UTF-8 encoding
        logging.StreamHandler()  # Log to Jupyter Notebook output
    ]
)

def load_csv(file_path):
    """ Load CSV file into a Pandas DataFrame. """
    try:
        df = pd.read_csv(file_path)
        logging.info(f"✅ CSV file '{file_path}' loaded successfully.")
        return df
    except Exception as e:
        logging.error(f"❌ Error loading CSV file: {e}")
        raise

def save_merged_data(df, output_path):
    """ Save merged data to a new CSV file. """
    try:
        df.to_csv(output_path, index=False)
        logging.info(f"✅ Merged data saved successfully to '{output_path}'.")
        print(f"✅ Merged data saved successfully to '{output_path}'.")
    except Exception as e:
        logging.error(f"❌ Error saving merged data: {e}")
        raise

def main():
    try:
        data_dir = '../src/data/raw_data/'
        channels = [
            'DoctorsET_data.csv',
            'CheMed123_data.csv',
            'lobelia4cosmetics_data.csv',
            'yetenaweg_data.csv',
            'EAHCI_data.csv'
        ]

        # Load data for each channel
        dfs = []
        for channel in channels:
            file_path = os.path.join(data_dir, channel)
            df = load_csv(file_path)
            dfs.append(df)

        # Merge all data
        merged_df = pd.concat(dfs, ignore_index=True)
        logging.info("✅ All channels merged successfully.")

        # Save the merged data
        output_path = '../src/data/merged_medical_data.csv'
        save_merged_data(merged_df, output_path)

    except Exception as e:
        logging.error(f"❌ Error in main function: {e}")
        raise

if __name__ == "__main__":
    main()