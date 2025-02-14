#  Project-api

## 📖 Project Overview

This repository contains the implementation of **Project API**, a system designed to manage and process employee hiring data efficiently using a **Medallion architecture** in **Azure SQ**L. The API supports batch data ingestion and querying transformed data for reporting in **Power BI**.

Features

Batch Data Ingestion: Supports inserting data into the Bronze layer in batches of 1 to 1000 rows.

Data Processing Pipeline: Transforms raw data from Bronze to Silver for analysis.

Power BI Integration: Queries transformed data from Silver to generate business insights.

Medallion Architecture: Implements a structured approach to data storage and transformation.

## 🏗️ Data Architecture

The API follows the Medallion architecture with three layers:

Bronze: Stores raw data. This is where new records are ingested.

Silver: Contains cleaned and transformed data. The API queries this layer for insights.

Gold: Provides aggregated and structured data views for reporting.

## 🚀 Installation & Setup

### Prerequisites

Ensure you have the following installed:

Python 3.8+

FastAPI

SQLAlchemy

Azure SQL Database

Power BI for visualization

### Installation Steps

Clone the repository:

git clone https://github.com/stezele/project-api.git
cd project-api

Create a virtual environment and install dependencies:

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt

Configure the database connection in config.py.

Start the API server:

uvicorn main:app --reload

API Endpoints

Method

Endpoint

Description

POST

/insert

Inserts batch data into Bronze (1-1000 rows).

GET

/query

Retrieves processed data from Silver.

GET

/report

Fetches aggregated insights from Gold.

Usage

Insert Data: Send a batch of up to 1000 records using the /insert endpoint.

Query Transformed Data: Fetch cleaned and structured data via /query.

Generate Reports: Access aggregated data for reporting through /report.

Deployment

For deployment on Azure:

Set up an Azure SQL Database.

Deploy the API using Azure App Services.

Connect Power BI to the Gold layer for reporting.

Contributing

Contributions are welcome! Please follow these steps:

Fork the repository.

Create a new branch: git checkout -b feature-branch.

Commit your changes: git commit -m 'Add new feature'.

Push to your branch: git push origin feature-branch.

Submit a Pull Request.

License

This project is licensed under the MIT License. See LICENSE for details.
