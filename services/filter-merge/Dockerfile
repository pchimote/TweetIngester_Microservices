FROM python:3.8-slim
WORKDIR /usr/code
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY ./utils.py .
COPY ./filter_merge.py .
ENV FM_MODE=filter
ENV FM_ARGS=/mnt/camelot-cs5604/twt/twirole.json,id,username,timestamp,hashtags,mentions,geolocation,keywords,twirole,text
CMD ["python","./filter_merge.py"]
