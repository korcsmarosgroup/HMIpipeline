# install python environment
add-apt-repository ppa:deadsnakes/ppa
apt-get update

apt-get -y install python3.6 python3.6-dev python3-setuptools python3-pip
update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.5 1
update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 2
pip3 install --upgrade numpy
pip3 install --upgrade scipy
pip3 install --upgrade pandas
pip3 install --upgrade matplotlib
pip3 install --upgrade mlxtend
pip3 install --upgrade xgboost
pip3 install --upgrade scikit-learn
pip3 install --upgrade biopython
pip3 install --upgrade argparse
pip3 install --upgrade minio
pip3 install --upgrade python-qpid-proton
pip3 install --upgrade pyfasta
pip3 install --upgrade networkx
