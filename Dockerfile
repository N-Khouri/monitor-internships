FROM python:3.11

ENV HOME /root
WORKDIR /root

COPY . .
RUN pip install -r requirements.txt

ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

CMD python -u main.py