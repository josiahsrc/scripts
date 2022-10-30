#!/bin/bash

(
  CWD=$(pwd)
  cd "$(dirname "$0")/util/convert_youtube_to_mp3" || exit 1
  node main.js "$1" "$CWD"
);