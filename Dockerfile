FROM python:3.6-alpine

 

RUN apk add tzdata
RUN cp -r -f /usr/share/zoneinfo/$TZ /etc/localtime  
 
 
WORKDIR /micro_schedule
COPY requirements.txt requirements.txt
RUN pip3.6 install -r requirements.txt
CMD python3.6 app.py