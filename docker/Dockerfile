FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY apache_beam_pipeline /app

# The default command to run the scripts
 CMD ["sh", "-c", "python /app/create_index.py && python /app/pipeline.py"]