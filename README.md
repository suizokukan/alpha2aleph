# alpha2heb

# input file format
* utf-8
* insert hebrew file between '◆' and '■'.

# todo
* il manque shin avec daghesh
* TODO en pagaille + "..." dans argparse.
* tester la cohérence de symbols.txt
* implémenter la norme ISO-machin; renommer symbols.txt en xf_symbols.txt
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
$ echo "◆m<éléḵ:■" | python3 alpha2heb.py --source=stdin
$ echo "“m<éléḵ:”" | python3 alpha2heb.py --source=stdin