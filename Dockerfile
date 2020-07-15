FROM python:latest

WORKDIR /

COPY requirements.txt /botname/
RUN pip install -r /botname/requirements.txt
COPY . /botname/

CMD python3 /botname/app.py
