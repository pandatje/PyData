FROM ubuntu:trusty
# COPY . /app

RUN set -ex && apt-get update
RUN set -ex && apt-get install -y wget software-properties-common python-pip
RUN set -ex && wget -O - http://sgjp.pl/apt/sgjp.gpg.key | apt-key add -
RUN set -ex && add-apt-repository 'deb http://sgjp.pl/apt/ubuntu trusty main'
RUN set -ex && apt-get update
RUN set -ex && apt-get install -y python-morfeusz2
RUN set -ex && pip install -U pip setuptools pipenv

RUN set -ex && mkdir /app
WORKDIR /app

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
RUN set -ex && pipenv install --deploy --system
RUN set -ex && python -c "import nltk; nltk.download('punkt')"

COPY . /app
CMD python botytucja/language.py

# RUN useradd -m botytucja
# USER botytucja
# CMD python clock.py --access-logfile - --error-logfile - --log-file - --log-level info
