# Ethiopian Medical Businesses Data Warehouse

## Business Need
Build a data warehouse to store data on Ethiopian medical businesses scraped from the web and Telegram channels. Integrate object detection using YOLO to enhance data analysis.

## Project Objectives
- Develop data scraping and collection pipeline.
- Develop data cleaning and transformation pipeline.
- Object detection using YOLO.
- Data warehouse design and implementation.
- Data integration and enrichment.

## Tasks and Steps

### Task 1 - Data Scraping and Collection Pipeline
#### Telegram Scraping
Utilize the Telegram API to extract data from channels:
- [DoctorsET](https://t.me/DoctorsET)
- Chemed Telegram Channel
- [Lobelia4cosmetics](https://t.me/lobelia4cosmetics)
- [Yetenaweg](https://t.me/yetenaweg)
- [EAHCI](https://t.me/EAHCI)
- [TGStat Medicine](https://et.tgstat.com/medicine)

#### Image Scraping
Collect images from:
- Chemed Telegram Channel
- [Lobelia4cosmetics](https://t.me/lobelia4cosmetics)

#### Steps
1. Use `telethon` for Telegram.
2. Store raw data temporarily.
3. Implement logging.

### Task 2 - Data Cleaning and Transformation
#### Data Cleaning
- Remove duplicates.
- Handle missing values.
- Standardize formats.
- Validate data.
- Store cleaned data.

#### DBT for Data Transformation
1. **Setup DBT**:
   ```sh
   pip install dbt
   dbt init my_project
