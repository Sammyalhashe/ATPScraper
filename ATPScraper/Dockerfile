FROM python:3.7.3-alpine

WORKDIR /usr/src/app
ENV DEV=production

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "./app.py"]
