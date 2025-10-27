# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Install Java for language-tool-python
RUN apt-get update && apt-get install -y openjdk-21-jre-headless && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app
ENV PYTHONPATH=/app

# Upgrade pip
RUN pip install --upgrade pip

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Download spaCy model and language tool data
RUN python -m spacy download en_core_web_sm
RUN python -c "import language_tool_python; language_tool_python.LanguageTool('en-US')"

# Copy the rest of the application code
COPY app/ /app/app
COPY services/ /app/services
COPY proto/ /app/proto
COPY dataset/ /app/dataset

# Expose the port the app runs on
EXPOSE 50052

# Define the command to run the application
CMD ["python", "-u", "-m", "app.server"]
