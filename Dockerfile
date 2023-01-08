FROM python:3.8

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose the port the app will run on
EXPOSE 8000

# Set the default command to run when starting the container
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]