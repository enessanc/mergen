FROM mergen/cpp-cmake:0.1

USER root
COPY --chown=10001:10001 infrastructure/docker/proof-project /opt/mergen/proof-project

USER 10001:10001
ENV MERGEN_WORKSPACE=/opt/mergen/proof-project
