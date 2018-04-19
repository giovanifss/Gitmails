FROM debian:latest
#RUN apk update && apk upgrade && apk add python3 libgit2-dev libgit2 gcc git libffi libffi-dev python3-dev linux-headers musl-dev
#RUN apt-get update && apt-get install python3-pygit2 python3 python3-pip libffi-dev pkg-config libgit2-dev libssl-dev openssl inetutils-inetd git -y
RUN apt-get update && apt-get install python3 python3-pip libgit2-dev cmake make wget openssl libssl-dev libffi-dev -y
#RUN apt-get install python-dev libffi-dev libssl-dev libxml2-dev libxslt1-dev libssh2-1 libgit2-dev python-pip libgit2-24 -y  
ADD . /
RUN wget https://github.com/libgit2/libgit2/archive/v0.27.0.tar.gz && \
      tar xzf v0.27.0.tar.gz && \
      cd libgit2-0.27.0/ && \
      cmake . && \
      make && \
      make install

RUN pip3 install -r requirements.txt
RUN ldconfig
ENTRYPOINT ["python3", "gitmails.py"]
