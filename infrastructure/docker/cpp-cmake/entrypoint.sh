#!/usr/bin/env bash
set -euo pipefail

workspace="${MERGEN_WORKSPACE:-/workspace}"
build_dir="${MERGEN_BUILD_DIR:-/tmp/mergen-build}"

if [[ ! -f "$workspace/CMakeLists.txt" ]]; then
  printf 'Mergen runtime error: CMakeLists.txt was not found in %s\n' "$workspace" >&2
  exit 64
fi

cmake -S "$workspace" -B "$build_dir" -G Ninja
cmake --build "$build_dir" --parallel
ctest --test-dir "$build_dir" --output-on-failure
