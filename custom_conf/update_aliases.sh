#!/bin/bash

# UPLOAD NEW VERSION OF ALIAS FILE TO GIT #

BASEDIR=/home/mramad3us


cp $BASEDIR/.aliases $BASEDIR/misc_lab/custom_conf
cd $BASEDIR/misc_lab && git add custom_conf && git commit -m updating && git push

