# NYC Taxi Trip Data Project

## Overview

This project demonstrates proficiency in SQL, Docker, and Apache Beam by processing and analyzing the NYC Taxi Trip Data. The project is divided into three parts:

1. **SQL Queries**
2. **Docker**
3. **Apache Beam**

## Data Source

We use the open-source dataset: [NYC Taxi Trip Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page). The specific file used is `yellow_tripdata_2022-01.csv`, which was converted from Parquet to CSV using the script `preprocess-data.py`. Make sure to download the Parquet file, convert it to CSV and put it under the data folder.

## Project Structure

- **SQL Queries**: `queries.sql`
- **Docker Configuration**: `Dockerfile`, `docker-compose.yml`
- **Apache Beam Pipeline**: `create_index`,`pipeline`

## Part 1: SQL

The `queries.sql` file contains the following queries:

1. **Calculate the total number of trips**
2. **Calculate the average trip distance**
3. **Find the top 5 most common pickup locations**
4. **Find the top 5 most common drop-off locations**
5. **Calculate the total amount of tips given**

## Part 2: Docker

The project includes a `Dockerfile` and `docker-compose.yml` for setting up the environment.

### Dockerfile

The `Dockerfile` sets up the necessary environment for running the Apache Beam pipeline.

### docker-compose.yml

The `docker-compose.yml` file orchestrates the services required for the project, including setting up Elasticsearch.

## Part 3: Apache Beam

Using Apache Beam, we performed the following transformations on the dataset:

1. **Filter out trips where the trip distance is less than 0.1 miles**.
2. **Calculate the total fare amount for each trip** (sum of fare amount and tip amount).
3. **Group the data by pickup location and calculate the average total fare amount**.
4. **Group the data by dropoff location and calculate the average trip distance**.

The transformed data is saved to an Elasticsearch index named `nyc_taxi_trip_data`.

## Setup and Execution

### Prerequisites

- Docker
- Docker Compose

### Steps to Run

1. **Clone the repository**:
    ```sh
    git clone https://github.com/BorchaniSalma/Taxi-Trip-Data-Engineering.git
    cd Taxi-Trip-Data-Engineering
    ```

3. **Run SQL Queries**:
   Execute the queries in `queries.sql` using a SQL client connected to the database.

4. **Run Apache Beam Pipeline**:
   Follow the instructions in `apache_beam_pipeline/README.md` to run the Apache Beam pipeline.
