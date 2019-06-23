#!/bin/bash

set -e

COMMON_VERSIONS=(3.5 3.6 3.7)

build(){
    docker build . -t cpdb:${1} --build-arg PYTHON_VERSION=${1}
}

run(){
    docker run --rm cpdb:${1}
}

for version in ${@-${COMMON_VERSIONS[@]}}
do
    echo "building image for version $version"
    build ${version}
    echo "running tests for version $version"
    run ${version}
done

