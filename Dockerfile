FROM python:3.8.3-slim-buster
RUN python -m pip install --upgrade pip
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
