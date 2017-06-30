#!/bin/bash

#CHECK ALL THE MALWARE IN BACKDOORED FOLDER AGAINST VT#

BASEDIR=/home/mramad3us/misc_lab/pe_poke
vtnotify=/home/mramad3us/sploitation/toolkit/Veil-Evasion/tools/vt-notify/vt-notify.rb

[ -f $BASEDIR/backdoored/sha1s ] && rm $BASEDIR/backdoored/sha1s

sha1sum $BASEDIR/backdoored/* > $BASEDIR/backdoored/sha1s

[ $# -gt 0 ] && [ $1 == '-v' ] && $vtnotify -f $BASEDIR/backdoored/sha1s

[ $# -eq 0 ] && $vtnotify -f $BASEDIR/backdoored/sha1s > vt-notify.out 2> vt-notify.err &


