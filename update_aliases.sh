#!/bin/bash

BASEDIR=/home/mramad3us

# UPLOAD NEW VERSION OF ALIAS FILE TO GIT #

cp $BASEDIR/.aliases $BASEDIR/misc_lab
cd $BASEDIR/misc_lab && git commit -m updating && git push

