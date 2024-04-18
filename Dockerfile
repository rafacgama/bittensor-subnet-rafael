FROM ubuntu:22.04
LABEL authors="Rafael Gama"

# Environment setup
ARG DEBIAN_FRONTEND=noninteractive
ENV RUST_BACKTRACE=1

# Install necessary packages and cleanup in one step
RUN apt update && \
    apt install -y make build-essential git clang curl libssl-dev llvm libudev-dev protobuf-compiler python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir -r ./requirements.txt

# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

WORKDIR /app

RUN git clone https://github.com/opentensor/subtensor.git && cd subtensor && git checkout main

WORKDIR /app

RUN ./subtensor/scripts/init.sh

WORKDIR /app/subtensor

RUN cargo build --release --features pow-faucet

CMD BUILD_BINARY=0 ./scripts/localnet.sh

