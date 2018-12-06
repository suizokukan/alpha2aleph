# alpha2heb

# input file format
* utf-8
* insert hebrew file between '◆' and '■'.

# logging info.
Modify logger.py::LOGGING_LEVEL

# exit codes
-1 : an error occured (ill-formed config file)
-2 : an error occured (ill-formed input file)
-3 : an error occured (ill-formed symbol file)

# doc
* a runtimeerror may be raised : see raise RuntimeError in the source code.

# pipe'able ? Yes !
$ echo "◆m<éléḵ:■" | python3 alpha2heb.py --source=stdin
$ echo "“m<éléḵ:”" | python3 alpha2heb.py --source=stdin

# todo
* documenter le pipeline

* il manque shin avec daghesh
* implémenter la norme ISO-machin; renommer symbols.txt en xf_symbols.txt
* dans les tests, bien vérifier source={file,stdin} + RTLSYMB ==/!= .
* exportation > html (https://www.w3.org/International/articles/inline-bidi-markup/) : choisir la police pour hébreu/le reste dans config.ini
* piper : il faut donc un point d'entrée.
* pylint=10
* incorporer les caractères de U0590...
* tests unitaires
* todo : export vers .odt
* todo : si hebrew2unicode[x] n'existe pas
* todo : exemples d'utilisation
