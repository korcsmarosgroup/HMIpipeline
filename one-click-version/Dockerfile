FROM python:3.6-stretch
MAINTAINER MicrobioLink project "bbazsi41@gmail.com"

RUN pip install --upgrade pip

WORKDIR /home/hmipipeline

ADD requirements.txt /home/hmipipeline/requirements.txt
RUN pip install -r /home/hmipipeline/requirements.txt

ADD /deploy/pipeline /home/hmipipeline/deploy/pipeline
ADD example_files /home/hmipipeline/example_files
ADD user_inputs /home/hmipipeline/user_inputs
ADD complete.sh /home/hmipipeline/complete.sh
ADD stepbystep.sh /home/hmipipeline/stepbystep.sh
ADD USER_complete_mode.sh /home/hmipipeline/USER_complete_mode.sh
ADD USER_stepbystep_mode.sh /home/hmipipeline/USER_stepbystep_mode.sh

CMD /bin/bash