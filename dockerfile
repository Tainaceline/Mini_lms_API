FROM python:3.12

WORKDIR /projeto

COPY . .

RUN pip install -r requeriments.txt
EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]