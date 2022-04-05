# syntax=docker/dockerfile:1

FROM python:3.9.11-slim-bullseye

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .
CMD ["sh", "run.sh"]
