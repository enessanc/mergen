cmake_minimum_required(VERSION 3.22)

project(mergen_runtime_proof LANGUAGES CXX)

enable_testing()

add_executable(runtime_proof src/main.cpp)
target_compile_features(runtime_proof PRIVATE cxx_std_20)

add_test(NAME runtime_proof COMMAND runtime_proof)
