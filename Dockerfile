FROM kennethreitz/pipenv
COPY . /app

RUN useradd -m botytucja
USER botytucja
CMD python clock.py --access-logfile - --error-logfile - --log-file - --log-level info
