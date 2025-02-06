FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Define environment variable for Google API key
# (You can also pass this via docker-compose or at runtime)
ENV GOOGLE_API_KEY="AIzaSyAZWhdsbFlcCkguMhF39TBrAXdaisb39JY"

# Run the FastAPI app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
