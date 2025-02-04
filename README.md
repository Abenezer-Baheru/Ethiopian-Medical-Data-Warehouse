# Ethiopian Medical Businesses Data Warehouse

## Business Need
Build a data warehouse to store data on Ethiopian medical businesses scraped from the web and Telegram channels. Integrate object detection using YOLO to enhance data analysis.

## Project Objectives
- Develop data scraping and collection pipeline.
- Develop data cleaning and transformation pipeline.
- Object detection using YOLO.
- Data warehouse design and implementation.
- Data integration and enrichment.

## Tasks and Steps:

### 1 - Data Scraping and Collection Pipeline
#### Telegram Scraping
Utilize the Telegram API to extract data from channels:
- [DoctorsET](https://t.me/DoctorsET)
- [Chemed Telegram Channel](https://t.me/CheMed123)
- [Lobelia4cosmetics](https://t.me/lobelia4cosmetics)
- [Yetenaweg](https://t.me/yetenaweg)
- [EAHCI](https://t.me/EAHCI)
- [TGStat Medicine](https://et.tgstat.com/medicine)

#### Image Scraping
Collect images from:
- [Chemed Telegram Channel](https://t.me/CheMed123)
- [Lobelia4cosmetics](https://t.me/lobelia4cosmetics)

#### Steps
1. Use `telethon` for Telegram.
2. Store raw data temporarily.
3. Implement logging.

### 2 - Data Cleaning and Transformation
#### Data Cleaning
- Remove duplicates.
- Handle missing values.
- Standardize formats.
- Validate data.
- Store cleaned data.

#### DBT for Data Transformation
1. **Setup DBT**: Install DBT and initialize the project.
2. **Defining Models**: Create DBT models for data transformation.
3. **Running DBT Models**: Perform the transformations and load the data into the data warehouse.
4. **Testing and Documentation**: Ensure data quality and provide context for the transformations.

### 3 - Object Detection Using YOLO
#### Setting Up the Environment
Ensure you have the necessary dependencies installed, including YOLO and its required libraries.

#### Downloading the YOLO Model
Clone the YOLO repository and install the required dependencies.

#### Preparing the Data
Collect images from the Chemed Telegram Channel and [Lobelia4cosmetics](https://t.me/lobelia4cosmetics). Use the pre-trained YOLO model to detect objects in the images.

#### Processing the Detection Results
Extract relevant data from the detection results, such as bounding box coordinates, confidence scores, and class labels. Store detection data in a database table. Implement logging to track the detection process, capture errors, and monitor progress.

### 4 - Expose the Collected Data Using FastAPI
#### Setting Up the Environment
Install FastAPI and Uvicorn.

#### Create a FastAPI Application
Set up a basic project structure for your FastAPI application.

#### Database Configuration
Configure the database connection using SQLAlchemy.

#### Creating Data Models
Define SQLAlchemy models for the database tables.

#### Creating Pydantic Schemas
Define Pydantic schemas for data validation and serialization.

#### CRUD Operations
Implement CRUD (Create, Read, Update, Delete) operations for the database.

#### Creating API Endpoints
Define the API endpoints using FastAPI.
