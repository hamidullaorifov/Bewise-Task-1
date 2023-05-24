# Use the official Python base image
FROM python:3.10.1

# Set the working directory inside the container
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Copy the requirements file
COPY requirements.txt .

# Install the Python dependencies
RUN pip install -r requirements.txt

COPY . .




ENV POSTGRES_USER=your_username
ENV POSTGRES_PASSWORD=your_password
ENV POSTGRES_DB=your_db

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
