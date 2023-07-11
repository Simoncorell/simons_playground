# This is a inspiration Dockerfile how to build a cbo based image such as:
# armdocker.rnd.ericsson.se/proj-dsi-portal/daas-ut/cbo-pytest-pylint:1.0.0

ARG CBO_IMAGE_URL=armdocker.rnd.ericsson.se/proj-ldc/common_base_os_full/sles
ARG CBO_VERSION=3.39.0-7
FROM ${CBO_IMAGE_URL}:${CBO_VERSION}

RUN zypper rm -y java-11-openjdk
RUN zypper rm -y java-11-openjdk-headless

# Installing some packages
ARG CBO_REPO=arm.sero.gic.ericsson.se/artifactory/proj-ldc-repo-rpm-local/common_base_os/sles/
ARG CBO_VERSION

RUN zypper addrepo --gpgcheck-strict -f https://${CBO_REPO}${CBO_VERSION} \
    COMMON_BASE_OS_SLES_REPO \
    && zypper --gpg-auto-import-keys refresh \
    && zypper install java-1_8_0-openjdk \
    && zypper install java-1_8_0-openjdk-headless \
    && zypper refresh \
    && zypper clean --all

RUN useradd eallprod
RUN groupadd eallprod
RUN usermod -aG eallprod eallprod

# Copy over the prod.yml file from ria-configuration
COPY prod.yml /tmp/
WORKDIR /tmp

# Install condaenv
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    sh Miniconda3-latest-Linux-x86_64.sh -b -p miniconda3 && \
    rm -rf Miniconda3-latest-Linux-x86_64.sh && \
    . /tmp/miniconda3/etc/profile.d/conda.sh && \
# Create a condaenv instance. Will take minimum 1-2 hours.
    conda env create -n conda_environment -f prod.yml && \
    conda clean -yptfi \
    && . /tmp/miniconda3/etc/profile.d/conda.sh \
    && conda activate conda_environment \
    && pip install sklearn \
    && conda deactivate

ENV JAVA_HOME "/usr"

USER eallprod
ENV HOME /home/eallprod

# Perhaps need to copy over users's ssh keys and/or known_host file for cdacommon.


