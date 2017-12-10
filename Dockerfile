FROM ubuntu:trusty
# COPY . /app

RUN apt-get update
RUN apt-get install -y wget software-properties-common
RUN wget -O - http://sgjp.pl/apt/sgjp.gpg.key | apt-key add -
RUN add-apt-repository 'deb http://sgjp.pl/apt/ubuntu trusty main'
RUN apt-get update
RUN apt-get install -y morfeusz2 python-morfeusz2

RUN set -ex && mkdir /app
WORKDIR /app

COPY morfeusz-test.py morfeusz-test.py
CMD python morfeusz-test.py

# RUN useradd -m botytucja
# USER botytucja
# CMD python clock.py --access-logfile - --error-logfile - --log-file - --log-level info
