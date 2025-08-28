FROM python:3.12-alpine

COPY /app/ /app/
COPY requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
