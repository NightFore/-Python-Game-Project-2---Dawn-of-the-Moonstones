import cx_Freeze
import os.path
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

executables = [cx_Freeze.Executable("[Game Project 2] Dawn of the Moonstones v6-2b.py")]

cx_Freeze.setup(
    name="Dawn of the Moonstones v6.2b",
    options={"build_exe": {"packages": ["pygame"],
                           "include_files": ["pygame_textinput.py",
                                             "Data",
                                             "readme.txt"]}},
    executables = executables

    )
