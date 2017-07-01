#!/bin/bash

# UPLOAD NEW VERSION OF ALIAS FILE TO GIT #

BASEDIR=/home/mramad3us


cp $BASEDIR/.aliases $BASEDIR/misc_lab
cd $BASEDIR/misc_lab && git add .aliases && git add update_aliases.sh && git commit -m updating && git push

