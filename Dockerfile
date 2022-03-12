FROM tiangolo/meinheld-gunicorn-flask:python3.7

COPY ./setup.py setup.py
RUN pip install .
RUN python -m spacy download en

COPY . /app

