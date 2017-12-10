FROM python:3.6.3

# -- Install Pipenv:
RUN set -ex && pip install pipenv --upgrade

# -- Install Application into container:
RUN set -ex && mkdir /app

WORKDIR /app

# -- Adding Pipfiles
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

# -- Install dependencies:
RUN set -ex && pipenv install --deploy --system

COPY . /app

RUN useradd -m botytucja
USER botytucja
CMD python3 clock.py --access-logfile - --error-logfile - --log-file - --log-level info
