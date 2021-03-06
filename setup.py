from distutils.core import setup

import py2exe, sys, os

sys.argv.append('py2exe')

includes = [

    "encodings",

    "encodings.utf_8",

]

options = {

    "bundle_files": 1,  # create singlefile exe

    "compressed": 1,  # compress the library archive

    "optimize": 2,  # do optimize

    "includes": includes,

}

setup(

    options={"py2exe": options},

    console=[{'script': "start.py"}, {'script': "auto_start_installer.py"}],
    # console=[{'script': "auto_start_installer.py"}],

    zipfile=None,

)