FROM rust:1-bookworm

ARG GRIND_REF=main
ARG WORDCRAFT_VERSION=0.18.1
ARG GRIDCRAFT_VERSION=0.19.1
WORKDIR /build

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl git python3 \
    && curl -fsSLO "https://github.com/storytold/wordcraft/releases/download/v${WORDCRAFT_VERSION}/wordcraft-${WORDCRAFT_VERSION}-linux-x86_64.deb" \
    && curl -fsSLO "https://github.com/storytold/gridcraft/releases/download/v${GRIDCRAFT_VERSION}/gridcraft-${GRIDCRAFT_VERSION}-linux-x86_64.deb" \
    && echo "9b557161ded7b5973112c8c21f600fe0b0110c1a4d3151184485733c96f87e19  wordcraft-${WORDCRAFT_VERSION}-linux-x86_64.deb" | sha256sum --check --status \
    && echo "3e9b093ee3bed8b1f008ea56c8d60e6a96890e24317be2bbb93e431f3c9d8112  gridcraft-${GRIDCRAFT_VERSION}-linux-x86_64.deb" | sha256sum --check --status \
    && apt-get install -y --no-install-recommends "./wordcraft-${WORDCRAFT_VERSION}-linux-x86_64.deb" "./gridcraft-${GRIDCRAFT_VERSION}-linux-x86_64.deb" \
    && rm -rf /var/lib/apt/lists/* \
    && rm -f /build/*.deb \
    && git clone --depth 1 --branch "${GRIND_REF}" https://github.com/fwilhe2/grind.git \
    && cd grind \
    && cargo build --locked --release -p grind-cli \
    && install -m 0755 target/release/grind /usr/local/bin/grind \
    && rm -rf /build/grind

WORKDIR /workspace
COPY scripts /workspace/scripts
ENV GRIND_BIN=/usr/local/bin/grind

ENTRYPOINT ["python3", "/workspace/scripts/create_samples.py"]