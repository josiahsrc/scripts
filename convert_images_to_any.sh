#!/bin/bash

(
  CWD=$(pwd)
  cd "$(dirname "$0")" || true
  .venv/bin/python3 -m util.convert_images_to_any --input-dir $CWD --output-dir $CWD "$@"
);
