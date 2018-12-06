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

# pipeline
## output: console

+============================================+================================+=====================================+
|transformation name                         | where is the code ?            | config.ini                          |
+============================================+================================+=====================================+
| console.1::text_delimiters                 | [add_firstlast_marker()]       | -                                   |
+--------------------------------------------+--------------------------------+-------------------------------------+
| console.2::main                            |                                |                                     |
|  * maingroup.1::improve_rtltext            | [transf__improve_rtltext()]    | - ???                               |
|  * maingroup.2::transf__text_alpha2hebrew  | [transf__text_alpha2hebrew()]  | - ???                               |
|  * maingroup.3::transf__use_FB1D_FB4F_chars| [transf__use_FB1D_FB4F_chars()]| ["pipeline.use FB1D-FB4F chars"]    |
| console.3::rtltext                         | [transf__invert_rtltext]       | ["output.console"]["invert_rtltext"]|
| console.4::remove_RTL_SYMBOLS              | [output_console()]             | -                                   |
| console.5::undo_text_delimiters            | [remove_firstlast_marker()]    | -                                   |
+--------------------------------------------+--------------------------------+-------------------------------------+

# todo
- 0.0.6 : sub_and_log() dans config.ini : remplir les "???"

- il manque shin avec daghesh
- implémenter la norme ISO-machin; renommer symbols.txt en xf_symbols.txt
- dans les tests, bien vérifier source={file,stdin} + RTLSYMB ==/!= .
- exportation > html (https://www.w3.org/International/articles/inline-bidi-markup/) : choisir la police pour hébreu/le reste dans config.ini
- piper : il faut donc un point d'entrée.
- pylint=10
- incorporer les caractères de U0590...
- tests unitaires
- todo : export vers .odt
- todo : si hebrew2unicode[x] n'existe pas
- todo : exemples d'utilisation
