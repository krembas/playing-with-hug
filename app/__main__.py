"""
Package bootstrap/runner (prepares runtime environment, runs tests, starts webserver that serves API and opens
webbrowser with application landing page).
"""
# Copyright (C) 2017 Krystian Rembas
# -----------------------------------------------------------------------------------------------------------------------
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
# to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
# -----------------------------------------------------------------------------------------------------------------------

import venv

import subprocess


def bootstrap(project_path, app_path, test_path, venv_path):
    """
    Bootstrap python app (checking compatibility issues, prepares dedicated virtualnenv, runs tests starts webserver,
    opens webbrowser with landing page)
    """

    print("\n+-------------------------------------------------------------------------+"
          "\n| -=((( The Ultimate PythonApp Bootstrap ;)))=-  (C) 2017 Krystian Rembas |"
          "\n+----------------------------<  HINT: Press CTRL-C to exit anytime... >---+\n")
    time.sleep(1)
    print("...Brace yourselves! Awesome is coming! ;)\n")
    time.sleep(2)
    PYTHON_EXE_PATH = join(venv_path, 'bin', 'python3')
    PIP_EXE_PATH = join(venv_path, 'bin', 'pip3')

    print("\n--> Examining your system for compatibility issues...\n")
    if os.name == 'nt':
        print(" (!) Sorry, Windows in not supported by this bootstrap, exiting now ;p")
        return -1

    print("\n--> Preparing runtime environment...\n")
    env_builder = venv.EnvBuilder(system_site_packages=False, clear=False, symlinks=True)
    env_builder.create(venv_path)
    getpip_path = join(venv_path, 'bin', 'get-pip.py')
    urlretrieve('https://bootstrap.pypa.io/get-pip.py', getpip_path)  # download pip bootstrap
    os.system(PYTHON_EXE_PATH + ' {}'.format(getpip_path))
    os.unlink(getpip_path)  # clean up, no longer needed
    os.system(PIP_EXE_PATH + ' install -r {}'.format(join(project_path, 'requirements.txt'))),

    print("\n--> Running the tests and source code syntax/style validator...\n")
    os.system(PYTHON_EXE_PATH + ' -m flake8 ' + app_path)
    os.system(PYTHON_EXE_PATH + ' -c "import pytest; pytest.main([\'-v\', \'{}\'])"'.format(test_path))
    print("\n--> Starting webserwer that serves app (@localhost:8000)...\n")
    try:
        sp = subprocess.Popen([PYTHON_EXE_PATH, '-c', 'import app; app.serve()'], cwd=app_path, stdout=subprocess.PIPE)
    except Exception:
        raise
    print("  [IN PROGRESS] Webserver's PID is {}".format(str(sp.pid)))
    time.sleep(3)  # give sometime to fully run server
    rc = sp.poll()
    if rc is not None:
        print("oops.. webserver terminated - sth gone wrong, exiting\n")
        sys.exit(rc)

    print("\n--> Opening web browser with app's landing page...\n")
    try:
        webbrowser.open('http://localhost:8000/', new=1)
    except Exception:
        raise
    print("\n--> ALL DONE! Stop the server at any time and exit by pressing CTRL-C...\n")
    sp.wait()


if __name__ == '__main__':
    import sys
    import time
    import os
    import webbrowser
    from os.path import dirname, abspath, join
    from urllib.request import urlretrieve

    PROJECT_ROOT_PATH = dirname(dirname(abspath(__file__)))
    APP_ROOT_PATH = join(PROJECT_ROOT_PATH, 'app')
    VENV_PATH = join(PROJECT_ROOT_PATH, '.venv')
    TEST_FILE_PATH = join(APP_ROOT_PATH, 'tests.py')

    sys.exit(bootstrap(project_path=PROJECT_ROOT_PATH, app_path=APP_ROOT_PATH,
                       test_path=TEST_FILE_PATH, venv_path=VENV_PATH))
