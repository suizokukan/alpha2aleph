# alpha2aleph
A GPLv3/Python3/CLI project to convert something like 'mlḵ' into 'כלמ'.

* By default, symbols (list of definitions like m → מ) are stored in `symbols.txt` (see --symbolsfile).
* By default, options are stored in `config.ini` (see --cfgfile).

# installation

## pip:
`$ sudo pip3 install alpha2aleph`

→ https://pypi.org/project/alpha2aleph/

## directly from the github repository:
→ https://github.com/suizokukan/alpha2aleph

# how to use it ?
## through a pipe :
echo "“m<éléḵ:”" | alpha2aleph --source=stdin --outputformat=console

or if alpha2aleph has not been installed through pip:

echo "“m<éléḵ:”" | bin/alpha2aleph --source=stdin --outputformat=console

# where may I find default files to give a try ?
You'll need `symbols.txt` and `config.ini`; just download them :
`$ alpha2aleph --downloadbasics`

# examples

## you want to use the project inside another .py file:
`$ python3 example0.py`

## you want to create a simple (console) output:
`$ ./example1.sh` : console output

## you want to create an html output:
`$ ./example2.sh` : html output

# tests
`$ nosetests3`

or

`$ python3 -m unittest tests/tests.py`

# to go further
## input file format
* utf-8
* insert hebrew file between globalsrtl.py::RTL_SYMBOLS (e.g. '“' and '”').

## logging info.
Modify `logger.py::LOGGING_LEVEL`

## exit codes, exceptions
-1 : an error occured : can't read config file
-2 : an error occured : ill-formed input file
-3 : an error occured : can't read symbols file
-4 : an error occured : missing input file

* a runtimeerror may be raised : see raise RuntimeError in the source code.

## transformations' pipeline
### output: html

+============================================+===============================+=================================+
|transformation name                         | where is the code ?           | config.ini                      |
+============================================+===============================+=================================+
| html.1::text_delimiters                    | add_firstlast_marker()        | -                               |
+--------------------------------------------+-------------------------------+---------------------------------+
| html.2::main                               |                               |                                 |
|  * maingroup.1::improve_rtlalphatext       | transf__improve_rtlalphatext()| [pipeline.improve rtlalphatext] |
|  * maingroup.2::transf__text_alpha2alephrew| transf__text_alpha2alephrew() | - (modify symbols.txt)          |
|  * maingroup.3::transf__use_FB1D_FB4F_chars| transf__use_FB1D_FB4F_chars() | [pipeline.use FB1D-FB4F chars]  |
| html.3::br                                 | output_html()                 | -                               |
| html.4::RTL_SYMBOLS                        | output_html()                 | -                               |
| html.5::undo_text_delimiters               | output_html()                 | -                               |
+--------------------------------------------+-------------------------------+---------------------------------+

### output: console

How do I correctly display bidirectional text ?
Either by using the fribidi library (see below), either by using a console like Konsole or mlterm (https://sourceforge.net/projects/mlterm/). Do NOT mix those solutions !

+=============================================+===============================+=================================+
|transformation name                          | where is the code ?           | config.ini                      |
+=============================================+===============================+=================================+
| console.1::text_delimiters                  | add_firstlast_marker()        | -                               |
+---------------------------------------------+-------------------------------+---------------------------------+
| console.2::maingroup                        |                               |                                 |
|  * maingroup.1::improve_rtlalphatext        | transf__improve_rtlalphatext()| [pipeline.improve rtlalphatext] |
|  * maingroup.2::transf__text_alpha2alephrew | transf__text_alpha2alephrew() | - (modify symbols.txt)          |
|  * maingroup.3::transf__use_FB1D_FB4F_chars | transf__use_FB1D_FB4F_chars() | [pipeline.use FB1D-FB4F chars]  |
| console.3::rtltext                          | transf__invert_rtltext        | [output.console][invert_rtltext]|
| console.4::remove_RTL_SYMBOLS               | output_console()              | [output.console][rtl symbols]   |
| console.5::undo_text_delimiters             | remove_firstlast_marker()     | -                               |
| console.6::use fribidi                      | output_console()              | [output.console][use fribidi]   |
+---------------------------------------------+-------------------------------+---------------------------------+

#### about fribidi:
* about fribidi : http://fribidi.org/
* about python-fribidi : https://github.com/RevengeComing/python-fribidi/blob/master/test/fribidi.py

## todo
- 0.2.x : bug : un appel à bin/alpha2aleph appelle d'abord la commande alpha2aleph.

- utiliser pimydoc pour :
  - # no id number for messages given to LOGGER.pipelinetrace(), e.g. no "[I01]".
  - paramaters, args

- c'est vraiment dommage que n'existe pas --loglevel=ERROR.
- vérifier la conformité de read_cfg_file() avec ce qui est attendu dans un fichier de configuration.

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
