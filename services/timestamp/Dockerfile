FROM python:3.8-slim
WORKDIR /usr/code
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY ./utils.py .
COPY ./extract_timestamp.py .
CMD ["python","./extract_timestamp.py"]
