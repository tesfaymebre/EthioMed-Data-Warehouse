# EthioMed-Data-Warehouse

# Telegram Scraping with Telethon

This module enables scraping data (messages and media) from public Telegram channels using the Telethon library. It is designed to store scraped data and media efficiently while maintaining logs and tracking progress.

## Features
- Scrapes messages from public Telegram channels.
- Downloads and saves media (images, documents, etc.) from messages.
- Tracks the last processed message ID to avoid re-scraping.
- Logs all activities for monitoring and debugging.
- Stores scraped data in a CSV file.
- Modular and extensible with Object-Oriented Programming (OOP).

---

## Directory Structure
```plaintext
├── data/
│   ├── raw/
│   │   ├── photos/             # Media files scraped from Telegram
│   │   ├── scraped_data.csv    # CSV file containing scraped messages
│   │   ├── [channel]_last_id.json  # JSON file tracking last processed message for each channel
├── logs/
│   ├── scraping.log            # Log file for tracking the scraping process
├── scripts/
│   ├── telegram_scraper.py     # Main scraping script
├── channels.json               # JSON file containing list of Telegram channels
```

---

## Requirements
Add the following dependencies to your `requirements.txt`:
```plaintext
telethon
python-dotenv
```

Install the dependencies:
```bash
pip install -r requirements.txt
```

---

## Setup

### 1. Environment Variables
Create a `.env` file in the root directory to store your Telegram API credentials:
```env
TG_API_ID=your_api_id
TG_API_HASH=your_api_hash
phone=your_phone_number
```
- Replace `your_api_id` and `your_api_hash` with your Telegram API credentials.
- Replace `your_phone_number` with the phone number linked to your Telegram account.

### 2. Add Channels
Create a `channels.json` file in the root directory to store the list of Telegram channels to scrape:
```json
{
  "channels": [
    "@DoctorsET",
    "@CheMed123",
    "@lobelia4cosmetics"
  ]
}
```
- Add channel usernames (with `@`) to the `channels` array.

---

## Usage

### Running the Scraper
Run the `telegram_scraper.py` script to scrape data:
```bash
python scripts/telegram_scraper.py
```

### Outputs
1. **Scraped Data**:
   - Saved in `data/raw/scraped_data.csv`.
   - Includes columns: `Channel Title`, `Channel Username`, `ID`, `Message`, `Date`, `Media Path`.

2. **Media Files**:
   - Saved in the `data/raw/photos/` directory.

3. **Progress Tracking**:
   - Last processed message ID for each channel is stored in `data/raw/[channel]_last_id.json`.

4. **Logs**:
   - Detailed logs are saved in `logs/scraping.log`.

---

## Key Features in the Script

### Class: `TelegramScraper`
Encapsulates all functionality for scraping Telegram data.

#### Methods:
1. `load_channels()`: Loads channels from `channels.json`.
2. `get_last_processed_id(channel_username)`: Retrieves the last processed message ID.
3. `save_last_processed_id(channel_username, last_id)`: Saves the last processed message ID.
4. `scrape_channel(channel_username, writer)`: Scrapes messages and media from a single channel.
5. `run()`: Main entry point for scraping multiple channels.

---

## Customization
### Adjust the Message Limit
To scrape more or fewer messages per channel, update the `message_count` limit in the `scrape_channel` method:
```python
if message_count >= 100:
    break
```

---

## Troubleshooting

### Common Errors
1. **Missing Channels File**:
   - Error: `Channels file channels.json not found.`
   - Solution: Ensure `channels.json` exists in the root directory.

2. **Authentication Error**:
   - Error: `Telegram client failed to start.`
   - Solution: Verify API credentials in the `.env` file.

3. **Permission Denied**:
   - Error: Unable to write files.
   - Solution: Check write permissions for `data/raw/` and `logs/` directories.

---

## Next Steps
- Add unit tests for scraper methods.
- Extend functionality to scrape private channels (requires admin permissions).
- Add options for real-time monitoring and reporting.

---

## Credits
Developed using the Telethon library: [https://github.com/LonamiWebs/Telethon](https://github.com/LonamiWebs/Telethon)

