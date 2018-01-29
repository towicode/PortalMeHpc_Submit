FROM alpine:latest
MAINTAINER bcf_staff
RUN apk update
RUN apk add --update make cmake gcc g++ gfortran
RUN apk add --update python python-dev
RUN apk add --update openssh
RUN apk add --update py-pip

RUN pip install pexpect

ADD main.py /usr/bin
ADD wisconsin.py /usr/bin
ADD generics.py /usr/bin
RUN chmod +x /usr/bin/main.py
ENTRYPOINT ["main.py"]