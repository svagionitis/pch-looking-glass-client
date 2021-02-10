# See https://www.docker.com/blog/containerized-python-development-part-1/

FROM python:3.8

WORKDIR /pch_looking_glass_cli

# Copy dependencies and install them
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ .

CMD [ "python", "./pch_looking_glass_cli.py" ]
