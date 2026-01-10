FROM python:3.13-slim

WORKDIR /core

COPY ./app /core/app
COPY ./requirements.txt /core/requirements.txt

RUN pip install --no-cache-dir -r /core/requirements.txt

EXPOSE 8000

CMD ["python", "/core/app/main.py"]
