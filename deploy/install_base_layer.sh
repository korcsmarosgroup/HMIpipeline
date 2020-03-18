#!/bin/sh
set -e

apt-get update -y --force-yes


apt-get -y install gcc g++ make sudo apt-utils software-properties-common
echo "----------------- basic packages INSTALLED ---------------------"

mkdir -p /home/hmipipeline


# UTF-8 locale settings
apt-get install -y locales
localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
echo "LC_ALL=en_US.UTF-8" >> /etc/environment
echo "LANGUAGE=en_US.UTF-8" >> /etc/environment
echo "LANG=en_US.UTF-8" >> /etc/environment

echo "---------------------- UTF-8 configured --------------------"


apt-get -y install openjdk-8-jre-headless
echo "JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64" >> /etc/environment
echo "-------------- JAVA INSTALLED ---------------"

apt-get -y install python-dev
echo "---------------------- python-dev installed --------------------"

apt-get -y install git
echo "---------------------- git installed --------------------"

apt-get -y install mc
echo "-------------- Midnight Commander INSTALLED ---------------"

apt-get -y install htop
echo "------------------- HTOP INSTALLED ------------------------"


