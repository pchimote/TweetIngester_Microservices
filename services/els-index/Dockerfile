FROM python:3.8-slim
WORKDIR /usr/code
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY ./utils.py .
COPY ./index.py .
CMD ["python","./index.py"]
