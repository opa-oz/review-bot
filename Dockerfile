FROM python:3.9

WORKDIR /code

EXPOSE 9091

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./main.py /code/main.py
COPY ./review_bot /code/review_bot


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9091"]