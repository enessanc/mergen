FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install --yes --no-install-recommends \
        build-essential \
        ca-certificates \
        cmake \
        git \
        ninja-build \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd --gid 10001 mergen \
    && useradd --uid 10001 --gid mergen --create-home --shell /usr/sbin/nologin mergen

COPY entrypoint.sh /usr/local/bin/mergen-cpp-cmake-validate
RUN chmod 0555 /usr/local/bin/mergen-cpp-cmake-validate

USER 10001:10001
WORKDIR /workspace

ENTRYPOINT ["/usr/local/bin/mergen-cpp-cmake-validate"]
