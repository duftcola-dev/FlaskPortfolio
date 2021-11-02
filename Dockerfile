FROM python:3.9.1

ADD . /home
WORKDIR /home
COPY . /home

RUN pip install -r requirements.txt
RUN python3 -m pip install --upgrade pip

ENTRYPOINT [ "python" ]

CMD [ "App.py" ]