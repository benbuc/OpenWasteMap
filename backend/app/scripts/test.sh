#!/usr/bin/env bash

set -e
set -x

if [ $# -eq 0 ]
then
    pytest --cov=app --cov-report=term-missing app/tests
else
    pytest --cov=app --cov-report=term-missing "${@}"
fi
