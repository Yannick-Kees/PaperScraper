FROM python:3.10.10-slim

WORKDIR /python-docker
RUN apt-get update 

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt


COPY . .
EXPOSE 5000

CMD cd src && python3 -m flask run --host=0.0.0.0 -p 1405

