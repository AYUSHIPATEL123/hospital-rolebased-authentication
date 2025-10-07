FROM python:3.11

WORKDIR /app

RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev gcc pkg-config default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt  requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY wait-for-db.sh /app/wait-for-db.sh
RUN chmod +x /app/wait-for-db.sh

COPY . .

EXPOSE 8000

# ENTRYPOINT ["python3"]
CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8000"]