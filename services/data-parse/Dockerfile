FROM python:3.8-slim
WORKDIR /usr/code
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python","./data_parser.py"]


## need to write command to copy parsed files 
## from container to semi-persistent storage 
## to avoid retriggering of service when not in need