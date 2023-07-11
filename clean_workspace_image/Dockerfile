ARG CBO_IMAGE_URL=armdocker.rnd.ericsson.se/proj-ldc/common_base_os_full/sles
ARG CBO_VERSION=3.60.0-32
FROM ${CBO_IMAGE_URL}:${CBO_VERSION}

ARG CBO_VERSION
ARG CBO_REPO=arm.sero.gic.ericsson.se/artifactory/proj-ldc-repo-rpm-local/common_base_os/sles/

RUN zypper addrepo --gpgcheck-strict -f https://${CBO_REPO}${CBO_VERSION} \
    COMMON_BASE_OS_SLES_REPO \
    && zypper --gpg-auto-import-keys refresh \
    && zypper clean --all
