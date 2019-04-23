FROM python:3.6

ENV WHERE_AM_I ""
ENV MAILSERVER: ""
ENV ADDR_FROM: ""
ENV ADDR_TO: ""

COPY main.py /main.py
COPY requirements.txt /requirements.txt

RUN pip install -r requirements.txt

CMD ["python", "/main.py"]
