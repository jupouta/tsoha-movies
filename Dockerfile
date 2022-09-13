FROM python:3.9-slim-bullseye

# For python (web)

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src .
CMD ["flask", "--app", "src/myapp.py", "run"]