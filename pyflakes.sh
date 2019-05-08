#!/bin/bash

echo "============================================================"
echo "== pyflakes =="
pyflakes saasbase | grep -v migration
