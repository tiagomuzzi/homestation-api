FROM python:3

WORKDIR /usr/src/app

ENV FLASK_APP=source/app.py
ENV FLASK_RUN_HOST=0.0.0.0

ENV FLASK_ENV=development 

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["flask", "run"]