import logging
from telethon import TelegramClient
import csv
import os
import json
from dotenv import load_dotenv

class TelegramScraper:
    def __init__(self, raw_data_dir="data/raw/", log_dir="logs/", channels_file="channels.json"):
        # Directories for raw data and logs
        self.raw_data_dir = raw_data_dir
        self.media_dir = os.path.join(self.raw_data_dir, "photos")
        os.makedirs(self.raw_data_dir, exist_ok=True)
        os.makedirs(self.media_dir, exist_ok=True)
        os.makedirs(log_dir, exist_ok=True)

        # Set up logging
        logging.basicConfig(
            filename=os.path.join(log_dir, "scraping.log"),
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )

        # Load environment variables
        load_dotenv()
        self.api_id = os.getenv("TG_API_ID")
        self.api_hash = os.getenv("TG_API_HASH")
        self.phone = os.getenv("phone")
        self.session_name = os.getenv("SESSION_NAME")

        # Initialize Telegram client
        self.client = TelegramClient(self.session_name, self.api_id, self.api_hash)

        # Load channels from JSON file
        self.channels_file = channels_file
        self.channels = self.load_channels()

    def load_channels(self):
        """Load channels from a JSON file."""
        try:
            with open(self.channels_file, "r") as f:
                data = json.load(f)
                return data.get("channels", [])
        except FileNotFoundError:
            logging.error(f"Channels file {self.channels_file} not found.")
            return []
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON file {self.channels_file}: {e}")
            return []

    def get_last_processed_id(self, channel_username):
        """Retrieve the last processed message ID for a channel."""
        try:
            file_path = os.path.join(self.raw_data_dir, f"{channel_username}_last_id.json")
            with open(file_path, "r") as f:
                return json.load(f).get("last_id", 0)
        except FileNotFoundError:
            logging.warning(f"No last ID file found for {channel_username}. Starting from 0.")
            return 0

    def save_last_processed_id(self, channel_username, last_id):
        """Save the last processed message ID for a channel."""
        file_path = os.path.join(self.raw_data_dir, f"{channel_username}_last_id.json")
        with open(file_path, "w") as f:
            json.dump({"last_id": last_id}, f)
            logging.info(f"Saved last processed ID {last_id} for {channel_username}.")

    async def scrape_channel(self, channel_username, writer):
        """Scrape messages from a single Telegram channel."""
        try:
            entity = await self.client.get_entity(channel_username)
            channel_title = entity.title

            last_id = self.get_last_processed_id(channel_username)
            is_first_run = (last_id == 0)  # Check if this is the first run
            message_count = 0

            async for message in self.client.iter_messages(entity):
                # Skip previously processed messages unless it's the first run
                if not is_first_run and message.id <= last_id:
                    continue

                media_path = None
                if message.media:
                    filename = (
                        f"{channel_username}_{message.id}.jpg"
                        if not hasattr(message.media, "document")
                        else f"{channel_username}_{message.id}.{message.media.document.mime_type.split('/')[-1]}"
                    )
                    media_path = os.path.join(self.media_dir, filename)
                    await self.client.download_media(message.media, media_path)
                    logging.info(f"Downloaded media for message ID {message.id}.")

                writer.writerow(
                    [
                        channel_title,
                        channel_username,
                        message.id,
                        message.message,
                        message.date,
                        media_path,
                    ]
                )
                logging.info(f"Processed message ID {message.id} from {channel_username}.")

                last_id = message.id
                message_count += 1

                # Stop after scraping 100 messages
                if message_count >= 100:
                    break

            self.save_last_processed_id(channel_username, last_id)

            if message_count == 0:
                logging.info(f"No new messages found for {channel_username}.")

        except Exception as e:
            logging.error(f"Error while scraping {channel_username}: {e}")


    async def run(self):
        """Run the scraper for multiple channels."""
        try:
            await self.client.start(self.phone)
            logging.info("Telegram client started successfully.")

            csv_file = os.path.join(self.raw_data_dir, "scraped_data.csv")
            with open(csv_file, "a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                if os.stat(csv_file).st_size == 0:  # Write headers only if the file is empty
                    writer.writerow(
                        ["Channel Title", "Channel Username", "ID", "Message", "Date", "Media Path"]
                    )

                for channel in self.channels:
                    await self.scrape_channel(channel, writer)
                    logging.info(f"Scraped data from {channel}.")

        except Exception as e:
            logging.error(f"Error in run function: {e}")

# Main function
if __name__ == "__main__":
    import asyncio

    scraper = TelegramScraper()
    asyncio.run(scraper.run())
