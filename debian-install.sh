#!/bin/bash
set -x

cd /tmp
sudo apt-get update && \
  sudo apt-get install python3 python3-pip libgit2-dev cmake make wget openssl libssl-dev libffi-dev -y

wget https://github.com/libgit2/libgit2/archive/v0.27.0.tar.gz && \
  tar xzf v0.27.0.tar.gz && \
  cd libgit2-0.27.0/ && \
  cmake . && \
  make && \
  sudo make install

ldconfig
pip3 install pygit2
