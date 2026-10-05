FROM python:3.12.15-alpine3.23 as dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
CMD ["python" "apps.py"]
