FROM python:3.8.13-bullseye

WORKDIR /usr/src/app

ENV VIRTUAL_ENV=/code/venv
RUN python3 -m venv $VIRTUAL_ENV
RUN /code/venv/bin/python3 -m pip install --upgrade pip

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies:
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
VOLUME ./output /usr/src/app/output

# Default to linting (using CMD, so it can be overridden).
CMD pylint features/**/*.py
