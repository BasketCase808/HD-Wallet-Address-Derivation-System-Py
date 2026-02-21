FROM python:3.10-slim
WORKDIR /app

# Copy the pre-downloaded packages
COPY ./packages /app/packages
COPY main.py .

# Install from the local folder without hitting the internet
RUN pip install --no-index --find-links=/app/packages fastapi uvicorn bitcoinlib python-dotenv

EXPOSE 8000

#CMD ["python", "main.py"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
