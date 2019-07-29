#!/bin/bash

echo "input filepath: $1"
echo "output filepath: $2"

python prediction.py $1 $2
