FROM python:3.6-alpine
RUN pip3 install soundcloud-lib
RUN mkdir /app

WORKDIR /app

COPY main.py /app/
#ENTRYPOINT ["tail", "-f", "/dev/null"]
ENTRYPOINT [ "python3" ,"main.py" ]