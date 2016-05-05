# plexmediaplayer

* Remember you must download the new Plex release from ```https://github.com/plexinc/plex-media-player```. 
* It must go into your SOURCES directory and be called something like ```plexmediaplayer-1.1.1.293.tar.gz```
* Then you can try running ```rpmbuild -ba ./plexmediaplayer.spec```

Note: You may fail due to patches.  You will need to update the patch files to match the correct QT library locations. Since you installed them with RPM's you won't be able to use the standard build. Going with the standard build could take over 5 hours or so to do. That sucks. 

* Make sure you have the following repo's added 
```dnf install https://plex-rpm.harrycow.fr/fedora/harrycow-plex-1.0.0-2.fc23.noarch.rpm``
```dnf install http://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm http://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm```

* Once the build is complete you can install it this way. ``` rpm -Uvh plexmediaplayer-1.1.1.293-1.fc23.x86_64.rpm```
