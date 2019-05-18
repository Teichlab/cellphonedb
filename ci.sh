#!/bin/bash

for version in 3.5 3.6 3.7
do
    docker build . -t cpdb:${version} --build-arg PYTHON_VERSION=${version}
done

for version in 3.5 3.6 3.7
do
    docker run --rm cpdb:${version}
done
