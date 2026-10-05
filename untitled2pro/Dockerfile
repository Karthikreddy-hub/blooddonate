FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
RUN useradd --create-home appuser \
    && chown -R appuser:appuser /app 

USER appuser

EXPOSE 5000
CMD ["python" "apps.py"]
