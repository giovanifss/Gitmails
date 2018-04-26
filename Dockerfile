FROM bitnami/minideb:stretch

ENV PYTHONIOENCODING utf8
RUN install_packages python3 python3-pip libgit2-dev gcc cmake make wget openssl libssl-dev libffi-dev python3-setuptools python3-dev
ADD . /
RUN echo "pygit2" >> /requirements.txt
RUN wget https://github.com/libgit2/libgit2/archive/v0.27.0.tar.gz && \
      tar xzf v0.27.0.tar.gz && \
      cd libgit2-0.27.0/ && \
      cmake . && \
      make && \
      make install
RUN pip3 install -r requirements.txt
RUN ldconfig
RUN apt-get purge gcc cmake make wget -y && apt-get autoremove -y
ENTRYPOINT ["python3", "gitmails.py"]
