#!/usr/bin/env bash
set -u

# Assume this script is in the src directory and work from that location
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}" )" && pwd)"

IMAGE="docker.pkg.github.com/rainthief/robot-test-libraries/robot_testing:0.0.3"
ROBOT_CONT_NAME="robot_tests"

#local log directory relative path to project root
LOG_DIR="logs/"
LOG_LEVEL="INFO"

source "$PROJECT_ROOT/scripts/include.sh"

OPTS="--loglevel $LOG_LEVEL -l NONE -r NONE -o NONE"
DOCKER_OPTS="-it"

if [ "$CI" == "true" ]; then
    OPTS="--loglevel INFO -l $LOG_DIR/robot_log.html -r $LOG_DIR/robot_report.html -o $LOG_DIR/output.xml"
fi

mkdir -p "$LOG_DIR"

if [ "$CI" == "true" ]; then
    docker login "$DOCKER_REG" -u "$DOCKER_USER" -p "$DOCKER_PASS"
    DOCKER_OPTS="-t"
fi

docker run --rm $DOCKER_OPTS --name "$ROBOT_CONT_NAME" \
-v "$(pwd)":/usr/app \
-v /var/run/docker.sock:/var/run/docker.sock \
--network=host \
$IMAGE bash -c "robot $OPTS --debugfile $LOG_DIR/system_test.log $* ./test/tests/*.robot"
TEST_STATUS=$?

# for local development of robot support library uncomment below and comment out docker run above
# pip install -r requirements.txt
# for install via git
# pip install git+https://github.com/RainThief/robot-test-libraries.git
# for install locally
# pip install -e /media/storage/projects/PERSONAL/robot-test-libraries/
# robot $OPTS --debugfile $LOG_DIR/system_test.log $* ./test/tests/*.robot
# TEST_STATUS=$?


# make logs readable
docker run --rm \
-v "$(pwd)":/usr/app \
$IMAGE chmod 777 ./logs/*

rm -f ./alembic.ini

exitonfail $TEST_STATUS "system test"

echo_success "System test passed"
