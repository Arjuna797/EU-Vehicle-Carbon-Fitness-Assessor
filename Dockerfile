# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's source code
COPY . .

# Make port 8501 available to the world outside this container
# This is Streamlit's default port
EXPOSE 8501

# Define environment variable
ENV HEALTHCHECK_URL=http://localhost:8501/healthz

# Add a healthcheck to ensure Streamlit is running
HEALTHCHECK --interval=15s --timeout=5s --start-period=5s \
  CMD curl -f $HEALTHCHECK_URL || exit 1

# Run app.py when the container launches
# We use 0.0.0.0 to make it accessible from outside the container
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
