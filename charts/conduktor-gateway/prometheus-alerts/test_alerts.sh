#!/usr/bin/env bash

set -Eeuo pipefail

origin=$(pwd)
script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd -P)

DOCKER=1
CMD=""


setup_colors() {
  if [[ -t 2 ]] && [[ -z "${NO_COLOR-}" ]] && [[ "${TERM-}" != "dumb" ]]; then
    NOFORMAT='\033[0m' RED='\033[0;31m' GREEN='\033[0;32m' ORANGE='\033[0;33m' BLUE='\033[0;34m' PURPLE='\033[0;35m' CYAN='\033[0;36m' YELLOW='\033[1;33m'
  else
    NOFORMAT='' RED='' GREEN='' ORANGE='' BLUE='' PURPLE='' CYAN='' YELLOW=''
  fi
}

msg() {
  echo >&2 -e "${1-}"
}

die() {
  local msg=$1
  local code=${2-1} # default exit status 1
  msg "$msg"
  exit "$code"
}


native_or_docker() {
    if command -v promtool &> /dev/null
    then
        DOCKER=0
        CMD="promtool"
        msg "${BLUE}promtool detected, running in local mode${NOFORMAT}"
        return
    fi

    if [ "${DOCKER}" -eq "1" ] && [ -n $(command -v docker &> /dev/null) ]
    then
        msg "${BLUE}docker detected, pull prometheus image ...${NOFORMAT}"
        docker pull prom/prometheus
        CMD="docker container run --rm -v ${script_dir}:/workdir -w /workdir --entrypoint /bin/promtool prom/prometheus"
    else
        die "${RED}Neither docker or promtool detected\nPlease check your configuration or install Prometheus promtool or docker to run this script${NOFORMAT}" 128
    fi
}

setup_colors

native_or_docker

cd ${script_dir}
TEST_FILES=""
for f in $(ls tests/*_tests.yaml)
do
  msg "${BLUE}Detected test file ${f}${NOFORMAT}"
  TEST_FILES="${TEST_FILES} ${f}"
done

$CMD test rules $TEST_FILES

if [ $? -eq 0 ]
then
    msg "${GREEN}Tests succeeded${NOFORMAT}"
fi

cd $origin
