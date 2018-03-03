#!/usr/bin/env bash
# check if python3 is installed
[[ "$(which python3 2>/dev/null)" != "" ]] && HAS_PYTHON3=1 || HAS_PYTHON3=0
if [ $HAS_PYTHON3 == 0 ]; then
    echo "python3 is required to run this app, please install it (v3.3+) and try again"
    echo && exit
fi
# ok, found so run app bootstrap
APP_ROOT_PATH=$(python3 -c "import os; print(os.path.realpath('$(dirname $0)'))")
cd "${APP_ROOT_PATH}/app/"
python3 __main__.py
