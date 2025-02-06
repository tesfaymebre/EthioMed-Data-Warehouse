# EthioMed-Data-Warehouse

The **EthioMed-Data-Warehouse** project enables scraping, processing, analyzing, and exposing data from Telegram channels and image-based object detection workflows. It integrates data scraping with Telethon, object detection using YOLOv5, and exposes the processed data via RESTful APIs built with FastAPI.

---

## Features
1. **Telegram Scraping**:
   - Scrapes messages and media (images, documents) from public Telegram channels.
   - Tracks progress using a JSON file to avoid duplicate processing.
   - Stores logs for monitoring and debugging.

2. **Object Detection**:
   - Runs object detection on scraped images using YOLOv5.
   - Saves detection results (bounding boxes, confidence scores, labels) as structured files and inserts them into a database.

3. **Data Exposure via APIs**:
   - RESTful APIs to access Telegram messages and object detection results.
   - Provides endpoints for querying, filtering, and analyzing the data.

---

## Directory Structure

```plaintext
├── data/
│   ├── raw/
│   │   ├── photos/                   # Media files scraped from Telegram
│   │   ├── scraped_data.csv          # CSV file containing scraped messages
│   ├── preprocessed/
│   │   ├── detection_results/        # YOLOv5 detection results
│   │       ├── detection_results.csv
├── my_project/
│   ├── main.py          # Entry point for the FastAPI application
│   ├── database.py      # Database configuration and connection
│   ├── models.py        # SQLAlchemy models for database tables
│   ├── schemas.py       # Pydantic schemas for data validation
│   └── crud.py          # CRUD operations for database interaction
├── logs/
│   ├── scraping.log                  # Log file for scraping
│   ├── object_detection.log          # Log file for YOLOv5 processing
├── scripts/
│   ├── telegram_scraper.py           # Telegram scraping script
│   ├── database_setup.py             # Database setup and connection
│   ├── api.py                        # FastAPI application entry point
│   ├── yolov5/                       # YOLOv5 cloned repository
├── notebooks/
│   ├── object_detection.ipynb        # Object detection notebook
│   ├── database_connection.ipynb     # Database integration notebook
├── channels.json                     # List of Telegram channels
├── requirements.txt                  # Project dependencies
├── README.md                         # Project documentation
```

---

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Variables
Create a `.env` file in the root directory to store your Telegram API and database credentials:

```env
TG_API_ID=your_api_id
TG_API_HASH=your_api_hash
phone=your_phone_number
DB_HOST=your_database_host
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_PORT=your_database_port
```

---

## Usage

### **Telegram Scraping**
Run the `telegram_scraper.py` script to scrape Telegram messages and media:
```bash
python scripts/telegram_scraper.py
```

**Outputs**:
1. Scraped data is saved in `data/raw/scraped_data.csv`.
2. Media files are saved in `data/raw/photos/`.
3. Logs are saved in `logs/scraping.log`.

---

### **Object Detection**
Run the YOLOv5 object detection pipeline on scraped images using the `object_detection.ipynb` notebook or the CLI:
```bash
python scripts/yolov5/detect.py \
    --weights scripts/yolov5/yolov5s.pt \
    --source data/raw/photos/ \
    --save-txt \
    --save-conf \
    --project data/preprocessed/detection_results/ \
    --name run1
```

**Outputs**:
1. Detection results are saved in `data/preprocessed/detection_results/`.
2. Results are also logged in `logs/object_detection.log`.

---

### **Exposing Data via FastAPI**
Run the FastAPI application to expose data:
```bash
uvicorn scripts.api:app --reload --host 0.0.0.0 --port 8000
```

**Endpoints**:
1. `/telegram_messages`: Retrieve Telegram messages.
2. `/detected_objects`: Retrieve detected objects.
3. `/detected_objects/stats`: Retrieve detection statistics.

**Interactive Documentation**:
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Key Features

### 1. **Telegram Scraper**
Encapsulates all functionality for scraping Telegram channels using Object-Oriented Programming (OOP).

#### Key Methods:
- `load_channels`: Loads channel list from `channels.json`.
- `scrape_channel`: Scrapes messages and media from a single channel.
- `run`: Main entry point for scraping multiple channels.

### 2. **YOLOv5 Integration**
- Detects objects in scraped images.
- Outputs structured detection results (bounding boxes, confidence scores, and labels).

### 3. **FastAPI API**
Provides endpoints to query Telegram messages and detection results.

---

## Testing

### Unit Tests
Add unit tests for:
- Telegram scraper methods.
- YOLOv5 results parsing.
- FastAPI endpoints.

Run tests:
```bash
pytest
```

---

## Troubleshooting

### Common Issues
1. **Missing Channels File**:
   - Error: `channels.json not found.`
   - Solution: Ensure `channels.json` exists in the root directory.

2. **Authentication Error**:
   - Error: `Telegram client failed to start.`
   - Solution: Verify Telegram API credentials in the `.env` file.

3. **TensorFlow Version Issues**:
   - Solution: Use Google Colab for object detection and download processed results.

4. **Database Connection Issues**:
   - Error: `Unable to connect to database.`
   - Solution: Verify database credentials in the `.env` file.

---

## Next Steps
1. Add authentication to FastAPI endpoints.
2. Automate the pipeline with CI/CD (e.g., GitHub Actions).
3. Deploy FastAPI with Docker for scalability.

---

## Credits
This project was developed using:
- **Telethon** for Telegram scraping: [https://github.com/LonamiWebs/Telethon](https://github.com/LonamiWebs/Telethon)
- **YOLOv5** for object detection: [https://github.com/ultralytics/yolov5](https://github.com/ultralytics/yolov5)
- **FastAPI** for RESTful APIs: [https://fastapi.tiangolo.com](https://fastapi.tiangolo.com)

