FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY apache_beam_pipeline /app/apache_beam_pipeline

# Copy input data file
COPY data/yellow_tripdata_2022-01.csv /app/data/yellow_tripdata_2022-01.csv

# Set the entry point for the container
ENTRYPOINT ["python", "apache_beam_pipeline/pipeline.py"]
