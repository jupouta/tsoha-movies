FROM python:3.9-slim-bullseye

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY webapp /opt/myapp/webapp
COPY config.py /opt/myapp
COPY main.py /opt/myapp

CMD ["python", "/opt/myapp/main.py"]