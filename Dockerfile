FROM python:3.9.1-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY wsgi.py wsgi.py
COPY blog ./blog
COPY migrations ./migrations
EXPOSE 5000
CMD ["python", "wsgi.py"]