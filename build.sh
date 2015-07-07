#/bin/bash
if [ ! -f /tmp/lame.tar.gz ]; then
    echo "Downloading LAME";
    wget -O /tmp/lame.tar.gz http://downloads.sourceforge.net/project/lame/lame/3.98.4/lame-3.98.4.tar.gz;
else
    echo "Found LAME";
fi


tar xvfz /tmp/lame.tar.gz;
./lame-3.98.4/configure --prefix=${PREFIX};
make;
make install;
make clean;
python setup.py install