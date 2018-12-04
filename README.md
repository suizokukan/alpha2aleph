# alpha2heb

# input file format
* utf-8
* insert hebrew file between '◆' and '■'.

# todo
* TODO en pagaille + "..." dans argparse.
* projet : alpha2heb
* header GPLv3
* dans les tests, bien vérifier source={file,stdin} + RTLSYMB ==/!= .
* exportation > html (https://www.w3.org/International/articles/inline-bidi-markup/) : choisir la police pour hébreu/le reste dans config.ini
* pylint=10
* documenter le pipeline
* incorporer les caractères de U0590...
* tests unitaires
* todo : export vers .odt
* todo : gestion des erreurs
* todo : si hebrew2unicode[x] n'existe pas
* todo : exemples d'utilisation

# exit codes
-1 : an error occured (ill-formed config file)
-2 : an error occured (ill-formed input file)

# doc
* a runtimeerror may be raised : see raise RuntimeError in the source code.

# pipe'able ? Yes !
$ echo "◆m<éléḵ:■" | python3 alpha2heb.py --source=stdin --outputformat=console
$ echo "“m<éléḵ:”" | python3 alpha2heb.py --source=stdin --outputformat=console