# using a specific 16.04 version (to avoid frequent updates)
FROM ubuntu:xenial-20181005
MAINTAINER MicrobioLink project "bbazsi41@gmail.com"

ADD install_base_layer.sh /
RUN /bin/bash /install_base_layer.sh

ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

ADD install_python.sh /
RUN /bin/bash /install_python.sh

EXPOSE 22

WORKDIR /home/hmipipeline

ADD /pipeline /home/hmipipeline/pipeline
ENV PYTHONPATH /home/hmipipeline/pipeline
