FROM python:3.6.10-slim
WORKDIR /app

RUN pip install --upgrade pip && \
apt-get update && \
apt-get install -y python3-dev default-libmysqlclient-dev build-essential && \
pip install mysqlclient && \
apt-get -y remove build-essential && \
apt-get -y autoremove && \
rm -rf /var/lib/apt/lists/*
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8888"]