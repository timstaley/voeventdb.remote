#!/bin/sh
PYTHONPATH=$(pwd -P):$PYTHONPATH jupyter notebook docs/source/notebooks
