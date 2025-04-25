FROM python:3.10-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /src

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY app .

COPY .env .env

# RUN chmod +x prestart.sh

# ENTRYPOINT [ "./prestart.sh" ]


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]