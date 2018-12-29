#!/usr/bin/env bash
echo "the word 'king' (“m<éléḵ:”) in Hebrew..." | bin/alpha2aleph_bin --log=ERROR --cfgfile=examples/config.ini --symbolsfile=examples/symbols.txt --source=stdin --outputformat=console
