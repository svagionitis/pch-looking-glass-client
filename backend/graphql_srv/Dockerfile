# See https://www.docker.com/blog/containerized-python-development-part-1/

FROM python:3.8

WORKDIR /graphql_srv

# Copy dependencies and install them
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ .

CMD [ "python", "./app.py" ]
