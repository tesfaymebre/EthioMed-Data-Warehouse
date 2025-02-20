import os
import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import pandas as pd

class DatabaseManager:
    def __init__(self, log_dir="logs", env_file=".env"):
        # Ensure logs folder exists
        os.makedirs(log_dir, exist_ok=True)

        # Configure logging
        logging.basicConfig(
            filename=os.path.join(log_dir, "database_setup.log"),
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

        # Load environment variables
        load_dotenv(env_file)

        self.db_host = os.getenv("DB_HOST")
        self.db_name = os.getenv("DB_NAME")
        self.db_user = os.getenv("DB_USER")
        self.db_password = os.getenv("DB_PASSWORD")
        self.db_port = os.getenv("DB_PORT")
        self.engine = None

    def connect_to_database(self):
        """Create and return the database engine."""
        try:
            database_url = f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
            logging.debug(f"Connecting to database with URL: {database_url}")  # Debug log
            self.engine = create_engine(database_url)
            
            # Test connection
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))

            logging.info("✅ Successfully connected to the PostgreSQL database.")
        except Exception as e:
            logging.error(f"❌ Database connection failed: {e}")
            raise

    def create_table(self):
        """Create the telegram_messages table if it does not exist."""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS telegram_messages (
            id SERIAL PRIMARY KEY,
            channel_title TEXT,
            channel_username TEXT,
            message_id BIGINT UNIQUE,
            message TEXT,
            message_date TIMESTAMP,
            media_path TEXT,
            emoji_used TEXT,
            youtube_links TEXT
        );
        """
        try:
            with self.engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
                connection.execute(text(create_table_query))

            logging.info("✅ Table 'telegram_messages' created successfully.")
        except Exception as e:
            logging.error(f"❌ Error creating table: {e}")
            raise

    def insert_data(self, cleaned_df):
        """Insert cleaned Telegram data into the database."""
        try:
            # Convert NaT timestamps to None (NULL in SQL)
            cleaned_df["message_date"] = cleaned_df["message_date"].apply(lambda x: None if pd.isna(x) else str(x))

            insert_query = """
            INSERT INTO telegram_messages 
            (channel_title, channel_username, message_id, message, message_date, media_path, emoji_used, youtube_links) 
            VALUES (:channel_title, :channel_username, :message_id, :message, :message_date, :media_path, :emoji_used, :youtube_links)
            ON CONFLICT (message_id) DO NOTHING;
            """

            with self.engine.begin() as connection:
                for _, row in cleaned_df.iterrows():
                    logging.info(f"Inserting: {row['message_id']} - {row['message_date']}")

                    connection.execute(
                        text(insert_query),
                        {
                            "channel_title": row["channel_title"],
                            "channel_username": row["channel_username"],
                            "message_id": row["message_id"],
                            "message": row["message"],
                            "message_date": row["message_date"],
                            "media_path": row["media_path"],
                            "emoji_used": row["emoji_used"],
                            "youtube_links": row["youtube_links"]
                        }
                    )

            logging.info(f"✅ {len(cleaned_df)} records inserted into PostgreSQL database.")
        except Exception as e:
            logging.error(f"❌ Error inserting data: {e}")
            raise

    def create_detected_objects_table(self):
        """Create the detected_objects table if it does not exist."""
        create_table_query = """
        CREATE TABLE detected_objects (
            id SERIAL PRIMARY KEY,
            image_name TEXT NOT NULL,
            class_id INTEGER NOT NULL,
            x_center FLOAT NOT NULL,
            y_center FLOAT NOT NULL,
            width FLOAT NOT NULL,
            height FLOAT NOT NULL,
            confidence FLOAT NOT NULL,
            detection_timestamp TIMESTAMP DEFAULT NOW()
        );
        """
        try:
            with self.engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
                connection.execute(text(create_table_query))

            logging.info("✅ Table 'detected_objects' created successfully.")
        except Exception as e:
            logging.error(f"❌ Error creating table: {e}")

    def insert_detection_results(self, detection_results_df):
        """Insert YOLOv5 detection results into the detected_objects table."""
        try:
            insert_query = """
            INSERT INTO detected_objects (
                image_name, class_id, x_center, y_center, width, height, confidence
            ) VALUES (
                :image_name, :class_id, :x_center, :y_center, :width, :height, :confidence
            );
            """
            with self.engine.begin() as connection:
                for _, row in detection_results_df.iterrows():
                    connection.execute(
                        text(insert_query),
                        {
                            "image_name": row["image_name"],
                            "class_id": row["class_id"],
                            "x_center": row["x_center"],
                            "y_center": row["y_center"],
                            "width": row["width"],
                            "height": row["height"],
                            "confidence": row["confidence"]
                        }
                    )
            logging.info(f"✅ {len(detection_results_df)} detection results inserted into database.")
        except Exception as e:
            logging.error(f"❌ Error inserting detection results: {e}")
            raise


# Example Usage
if __name__ == "__main__":
    db_manager = DatabaseManager()
    db_manager.connect_to_database()
    db_manager.create_table()

    # Example: Load cleaned data and insert into database
    cleaned_data_path = "data/preprocessed/cleaned_telegram_data.csv"
    cleaned_df = pd.read_csv(cleaned_data_path)
    db_manager.insert_data(cleaned_df)
