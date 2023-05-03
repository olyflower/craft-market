FROM python:3.10-slim

RUN apt update && mkdir /craft

WORKDIR /craft

COPY ./src ./src

COPY ./commands ./commands

COPY ./requirements.txt ./requirements.txt

RUN python -m pip install --upgrade pip && pip install -r ./requirements.txt

EXPOSE 8010

CMD ["bash"]
