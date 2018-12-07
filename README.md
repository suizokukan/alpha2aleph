# alpha2heb

# input file format
* utf-8
* insert hebrew file between '◆' and '■'.

# logging info.
Modify logger.py::LOGGING_LEVEL

# exit codes, exceptions
-1 : an error occured (ill-formed config file)
-2 : an error occured (ill-formed input file)
-3 : an error occured (ill-formed symbol file)

* a runtimeerror may be raised : see raise RuntimeError in the source code.

# pipe'able ? Yes !
$ echo "◆m<éléḵ:■" | python3 alpha2heb.py --source=stdin
$ echo "“m<éléḵ:”" | python3 alpha2heb.py --source=stdin

# transformations' pipeline
## output: html

+============================================+===============================+=================================+
|transformation name                         | where is the code ?           | config.ini                      |
+============================================+===============================+=================================+
| html.1::text_delimiters                    | add_firstlast_marker()        | -                               |
+--------------------------------------------+-------------------------------+---------------------------------+
| html.2::main                               |                               |                                 |
|  * maingroup.1::improve_rtlalphatext       | transf__improve_rtlalphatext()| [pipeline.improve rtlalphatext] |
|  * maingroup.2::transf__text_alpha2hebrew  | transf__text_alpha2hebrew()   | - (modify symbols.txt)          |
|  * maingroup.3::transf__use_FB1D_FB4F_chars| transf__use_FB1D_FB4F_chars() | [pipeline.use FB1D-FB4F chars]  |
| html.3::br                                 | output_html()                 | -                               |
| html.4::RTL_SYMBOLS                        | output_html()                 | -                               |
| html.5::undo_text_delimiters               | output_html()                 | -                               |
+--------------------------------------------+-------------------------------+---------------------------------+

## output: console

How do I correctly display bidirectional text ?
Either by using the fribidi library (see below), either by using a console like Konsole or mlterm (https://sourceforge.net/projects/mlterm/). Do NOT mix those solutions !

+============================================+===============================+=================================+
|transformation name                         | where is the code ?           | config.ini                      |
+============================================+===============================+=================================+
| console.1::text_delimiters                 | add_firstlast_marker()        | -                               |
+--------------------------------------------+-------------------------------+---------------------------------+
| console.2::maingroup                       |                               |                                 |
|  * maingroup.1::improve_rtlalphatext       | transf__improve_rtlalphatext()| [pipeline.improve rtlalphatext] |
|  * maingroup.2::transf__text_alpha2hebrew  | transf__text_alpha2hebrew()   | - (modify symbols.txt)          |
|  * maingroup.3::transf__use_FB1D_FB4F_chars| transf__use_FB1D_FB4F_chars() | [pipeline.use FB1D-FB4F chars]  |
| console.3::rtltext                         | transf__invert_rtltext        | [output.console][invert_rtltext]|
| console.4::remove_RTL_SYMBOLS              | output_console()              | [output.console][rtl symbols]   |
| console.5::undo_text_delimiters            | remove_firstlast_marker()     | -                               |
| console.6::use fribidi                     | output_console()              | [output.console][use fribidi]   |
+--------------------------------------------+-------------------------------+---------------------------------+

### about fribidi:
* about fribidi : http://fribidi.org/
* about python-fribidi : https://github.com/RevengeComing/python-fribidi/blob/master/test/fribidi.py

# todo
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
