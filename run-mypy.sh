#!/bin/bash

set -ex

mypy --strict orderedsets/ test/ examples/
