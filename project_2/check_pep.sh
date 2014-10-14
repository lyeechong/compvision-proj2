#!/usr/bin/env bash

# Check that source code conforms to PEP8.
if pep8 --show-source *.py; then
	echo "No style errors found. Your super swaaaaggggg levels are over 9000!"
else
	echo "Some style errors detected. Construct additional swag."
fi
echo ""
