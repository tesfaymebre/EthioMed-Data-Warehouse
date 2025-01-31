import pandas as pd
import logging
import re
import os
import emoji

class DataCleaner:
    def __init__(self, input_path="data/raw/scraped_data.csv", output_path="data/preprocessed/cleaned_data.csv"):
        self.input_path = input_path
        self.output_path = output_path

        # Ensure logs directory exists
        os.makedirs("logs", exist_ok=True)

        # Configure logging
        logging.basicConfig(
            filename="logs/data_cleaning.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def load_csv(self):
        """ Load CSV file into a Pandas DataFrame. """
        try:
            df = pd.read_csv(self.input_path)
            logging.info(f"✅ CSV file '{self.input_path}' loaded successfully.")
            return df
        except Exception as e:
            logging.error(f"❌ Error loading CSV file: {e}")
            raise

    @staticmethod
    def clean_text(text):
        """ Standardize text by removing newline characters and unnecessary spaces. """
        if pd.isna(text):
            return "No Message"
        return re.sub(r'\n+', ' ', text).strip()

    @staticmethod
    def extract_emojis(text):
        """ Extract emojis from text. """
        emojis = ''.join(c for c in text if c in emoji.EMOJI_DATA)
        return emojis if emojis else "No emoji"

    @staticmethod
    def remove_emojis(text):
        """ Remove emojis from text. """
        return ''.join(c for c in text if c not in emoji.EMOJI_DATA)

    def clean_dataframe(self, df):
        """ Perform all cleaning and standardization steps. """
        try:
            # Remove duplicates
            df = df.drop_duplicates(subset=["ID"]).copy()
            logging.info("✅ Duplicates removed from dataset.")

            # Format Date column
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            logging.info("✅ Date column formatted to datetime.")

            # Handle missing values
            df['Message'] = df['Message'].fillna("No Message")
            df['Media Path'] = df['Media Path'].fillna("No Media")
            logging.info("✅ Missing values filled.")

            # Standardize text columns
            df['Channel Title'] = df['Channel Title'].str.strip()
            df['Channel Username'] = df['Channel Username'].str.strip()
            df['Message'] = df['Message'].apply(self.clean_text)
            logging.info("✅ Text columns standardized.")

            # Extract and remove emojis
            df['emoji_used'] = df['Message'].apply(self.extract_emojis)
            df['Message'] = df['Message'].apply(self.remove_emojis)
            logging.info("✅ Emojis processed.")

            # Rename columns for consistency
            df.rename(columns={
                "Channel Title": "channel_title",
                "Channel Username": "channel_username",
                "ID": "message_id",
                "Message": "message",
                "Date": "message_date",
                "Media Path": "media_path",
                "emoji_used": "emoji_used"
            }, inplace=True)
            logging.info("✅ Column renaming completed.")

            return df
        except Exception as e:
            logging.error(f"❌ Data cleaning error: {e}")
            raise

    def save_cleaned_data(self, df):
        """ Save cleaned data to a new CSV file. """
        try:
            os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
            df.to_csv(self.output_path, index=False)
            logging.info(f"✅ Cleaned data saved successfully to '{self.output_path}'.")
        except Exception as e:
            logging.error(f"❌ Error saving cleaned data: {e}")
            raise

    def run(self):
        """ Execute the data cleaning pipeline. """
        df = self.load_csv()
        cleaned_df = self.clean_dataframe(df)
        self.save_cleaned_data(cleaned_df)

# Main execution
if __name__ == "__main__":
    cleaner = DataCleaner()
    cleaner.run()
