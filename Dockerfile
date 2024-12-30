# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container
COPY ./app .

# Set environment variables (optional)
ENV FLASK_APP=application.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080

# Expose port 8501 for Flask app
EXPOSE 8080

# Run the app
# CMD ["python", "application.py"]
CMD ["gunicorn", "-b", "0.0.0.0:8080", "application:application"]
