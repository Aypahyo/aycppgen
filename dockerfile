FROM python:latest
WORKDIR /app
RUN python -m pip install --upgrade pip
ADD . /app
RUN pip install -r requirements.txt
ENTRYPOINT [ "python", "-m", "unittest", "discover" ]
