#!/bin/bash

# UPLOAD NEW VERSION OF ALIAS FILE TO GIT #
# NEEDS TO BE RUN BY MAIN(NOT ROOT) USER WITH VERY SPECIFIC FS ORGANIZATION #

BASEDIR=$HOME


cp $BASEDIR/.aliases $BASEDIR/misc_lab/custom_conf
cp $BASEDIR/.bashrc $BASEDIR/misc_lab/custom_conf
cd $BASEDIR/misc_lab && git add custom_conf && git commit -m updating && git push

