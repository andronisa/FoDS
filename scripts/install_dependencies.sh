#!/usr/bin/env bash

if [[ $1 == "development" ]]; then
	echo "installing additional development dependencies..."

	env/bin/pip install --download-cache=.download_cache/ -r requirements_dev.txt
fi

env/bin/pip install --download-cache=.download_cache/ -r requirements.txt