FROM python:3.10

WORKDIR /usr/src/my_mock_server
COPY requirements.txt .

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

WORKDIR /usr/src/my_mock_server

EXPOSE 8000