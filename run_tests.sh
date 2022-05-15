#!/bin/sh
# A simple entrypoint for controlling the test run (using the most
# compatible shell).

behavex \
  --logging-level ${LOGGING_LEVEL:-'INFO'} \
  --parallel-processes ${PARALLEL_PROCESSES:-3} \
  --parallel-scheme ${PARALLEL_SCHEME:-'scenario'} \
  --tags ${TAGS:-'~@wip'}
