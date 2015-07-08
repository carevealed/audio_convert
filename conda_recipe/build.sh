#/bin/bash
if [ ! -f lame-3.98.4.tar.gz ]; then
    echo "Downloading LAME";
    wget http://downloads.sourceforge.net/project/lame/lame/3.98.4/lame-3.98.4.tar.gz;
else
    echo "Found LAME";
fi


tar xvfz ${SRC_DIR}/lame-3.98.4.tar.gz;
(cd ${SRC_DIR}/lame-3.98.4/; ./configure --prefix=${PREFIX};
make;
make install;
make clean;)
python setup.py install