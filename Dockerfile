FROM tiangolo/uwsgi-nginx-flask:python3.6

COPY ./app /app

WORKDIR /

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

