##################################################################
# Dockerfile to build container images for ngsfetch (v0.1.1)
# Based on python 3.9-bullseye
##################################################################

FROM python:3.9-bullseye

# File Author / Maintainer
LABEL maintainer="Naoto Kubota <naotok@ucr.edu>"

ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies first
RUN apt-get -qq update && \
	apt-get -qq -y install \
    wget less vim curl

# Upgrade pip
RUN pip install --upgrade pip

# Install ngsfetch
RUN git clone https://github.com/NaotoKubota/ngsfetch.git -b v0.1.1 && \
    cd ngsfetch && \
    pip install .

# Set working directory
WORKDIR /home

# bash
CMD ["bash"]
