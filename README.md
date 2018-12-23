**[[1] alpha2aleph](#1-alpha2aleph)**<br/>
**[[2] installation](#2-installation)**<br/>
**[[3] how to use it](#3-how-to-use-it)**<br/>
**[[4] how to write input text, symbols file and config file ?](#4-how-to-write)**<br/>
**[[5] tests & checks](#5-tests-and-checks)**<br/>
**[[6] to go further](#6-to-go-further)**<br/>
**[[7] todo & roadmap](#7-todo-and-roadmap)**<br/>

# [1] alpha2aleph
A GPLv3/Python3/CLI project to convert a string like '... the word king (“mlḵ”).' into '... the word king (‏מלכ‎).'.

* By default, symbols (list of definitions like m → מ) are stored in `symbols.txt` (see --symbolsfile command line option).
* By default, options are stored in `config.ini` (see --cfgfile command line option).

# [2] installation

## [2.1] pip:
`$ sudo pip3 install alpha2aleph`

→ https://pypi.org/project/alpha2aleph/

## [2.2] directly from the github repository:
→ https://github.com/suizokukan/alpha2aleph

# [3] how to use it ?

You'll need `symbols.txt` and `config.ini`; just download them :
`$ alpha2aleph --downloadbasics`

## [3.1] through a pipe :
`$ echo "“m<éléḵ:”" | alpha2aleph --source=stdin --outputformat=console`

or if `alpha2aleph` has not been installed through `pip` but if you downloaded the repository:

`$ echo "“m<éléḵ:”" | bin/alpha2aleph_bin --source=stdin --outputformat=console`

## [3.2] examples

### [3.2.1] you want to use the project inside another .py file:

see example0.py:

    from alpha2aleph.main import entrypoint
    print(entrypoint((os.path.join("examples", "config.ini"),
                  os.path.join("examples", "symbols.txt"),
                  "“m<éléḵ:”",
                  "console")))

### [3.2.2] you want to create a simple (console) output:

see example1.sh:

    echo "“m<éléḵ:”" | alpha2aleph --log=ERROR --cfgfile=examples/config.ini --symbolsfile=examples/symbols.txt --source=stdin --outputformat=console

### [3.2.2] you want to create an html output:

see example2.sh:

    alpha2aleph --log=ERROR --cfgfile=examples/config.ini --symbolsfile=examples/symbols.txt --source=inputfile --outputformat=html --inputfile=examples/input.txt

# [4] how to write input text, symbols file and config file ?

## [4.1] input file format
* utf-8
* insert hebrew text between globalsrtl.py::RTL_SYMBOLS (e.g. '“' and '”').

If you write something like:
`I know the Hebrew word for 'king', it's "“mlḵ”".`

The expected output is `I know the Hebrew word for 'king', it's "כלמ".`

## [4.2] symbols file
* utf-8
* comments begin after `#`.
* alphabetic symbol → hebrew symbol like in `ʔ → א`
  different alphabetic symbols may be used for the same hebrew symbol

## [4.3] configuration file
* utf-8
* INI file
* do not use upper case symbols in keys; not `Ḥe + holam + shin > Ḥe + shin : True` but `ḥe + holam + shin > ḥe + shin : True`

# [5] tests & checks

## [5.1] unit tests
`$ nosetests3`

or

`$ python3 -m unittest tests/tests.py`

## [5.2] test one symbol file:
`$ alpha2aleph --checksymbols --symbolsfile=examples/symbols.txt`

# [6] to go further

## [6.1] logging info.
see `--log` command line option.
Modify `logger.py::LOGGING_LEVEL`

## [6.2] exit codes, exceptions
-1 : an error occured : can't read config file
-2 : an error occured : ill-formed input file
-3 : an error occured : can't read symbols file
-4 : an error occured : missing input file

* a runtimeerror may be raised : see raise RuntimeError in the source code.

## [6.3] transformations' pipeline
### [6.3.1] output: html

|transformation name                         | where is the code ?           | config.ini                      |
|--------------------------------------------|-------------------------------|---------------------------------|
| html.1::text_delimiters                    | add_firstlast_marker()        | -                               |
| html.2::main                               |                               |                                 |
|  * maingroup.1::improve_rtlalphatext       | transf__improve_rtlalphatext()| [pipeline.improve rtlalphatext] |
|  * maingroup.2::transf__text_alpha2alephrew| transf__text_alpha2alephrew() | - (modify symbols.txt)          |
|  * maingroup.3::transf__use_FB1D_FB4F_chars| transf__use_FB1D_FB4F_chars() | [pipeline.use FB1D-FB4F chars]  |
| html.3::br                                 | output_html()                 | -                               |
| html.4::RTL_SYMBOLS                        | output_html()                 | -                               |
| html.5::undo_text_delimiters               | output_html()                 | -                               |

### [6.3.2] output: console

How do I correctly display bidirectional text ?
Either by using the fribidi library (see below), either by using a console like Konsole or mlterm (https://sourceforge.net/projects/mlterm/). Do NOT mix those solutions !

| transformation name                         | where is the code ?           | config.ini                      |
|---------------------------------------------|-------------------------------|---------------------------------|
| console.1::text_delimiters                  | add_firstlast_marker()        |                                 |
| console.2::maingroup                        |                               |                                 |
|  * maingroup.1::improve_rtlalphatext        | transf__improve_rtlalphatext()| [pipeline.improve rtlalphatext] |
|  * maingroup.2::transf__text_alpha2alephrew | transf__text_alpha2alephrew() | - (modify symbols.txt)          |
|  * maingroup.3::transf__use_FB1D_FB4F_chars | transf__use_FB1D_FB4F_chars() | [pipeline.use FB1D-FB4F chars]  |
| console.4::remove_RTL_SYMBOLS               | output_console()              | [output.console][rtl symbols]   |
| console.5::undo_text_delimiters             | remove_firstlast_marker()     | -                               |
| console.6::use fribidi                      | output_console()              | [output.console][use fribidi]   |

#### [6.3.2.1] about fribidi:
* about fribidi : http://fribidi.org/
* about python-fribidi : https://github.com/RevengeComing/python-fribidi/blob/master/test/fribidi.py

# [7] todo & roadmap

## [7.1] todo
> 0.2.9 : incohérence dans symbols.txt: g → גּ mais pas gg → גּ
- 0.3 : tests unitaires

- vérifier la conformité de read_cfg_file() avec ce qui est attendu dans un fichier de configuration.
- implémenter la norme ISO-machin; renommer symbols.txt en xf_symbols.txt; https://en.wikipedia.org/wiki/ISO_259
- dans les tests, bien vérifier source={file,stdin} + RTLSYMB ==/!= .
- incorporer les caractères de U0590...
- export vers .odt

## [7.2] roadmap
- v. 0.2.9 : completed examples/symbols.txt
- v. 0.2.8 : table of content in README.md
- v. 0.2.7 : use pimydoc to control some part of documentation
- v. 0.2.6 : improved README.md
- v. 0.2.5
     - improved README.md
     - fixed a typo in main.py : 'paramaters' > 'forcedparameters'
- v 0.2.4
     - improved README.md
     - renamed functions in main.py called to execute command line options:
       cmdline__*
- 0.2.3 : --checksymbols
