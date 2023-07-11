ARG CBO_IMAGE_URL=armdocker.rnd.ericsson.se/proj-ldc/common_base_os_full/sles
ARG CBO_VERSION=3.39.0-7
FROM ${CBO_IMAGE_URL}:${CBO_VERSION}

ARG NON_ROOT_USER=eallprod
ARG CI_REGISTRY_USER_ARM_TOKEN=AKCp8jRGQ4i67xFxtAkYkCDqr9WSvvca44ZGbngJTmc4bVyTCJF6bRdcrTv4fCDHnsP64Nh49
ARG CBO_REPO=arm.sero.gic.ericsson.se/artifactory/proj-ldc-repo-rpm-local/common_base_os/sles/
ARG ARM_GENERIC_PORTAL_REPO=arm.seli.gic.ericsson.se/artifactory/proj-dsi-portal-generic-local
ARG CBO_VERSION

RUN zypper addrepo --gpgcheck-strict -f https://${CBO_REPO}${CBO_VERSION} \
    COMMON_BASE_OS_SLES_REPO

RUN zypper addrepo -C -G -f https://arm.sero.gic.ericsson.se/artifactory/proj-ldc-repo-rpm-local/adp-dev/adp-build-env/1.6.0/?ssl_verify=no  ADP_DEV_BUILD_ENV_REPO \
    && zypper --gpg-auto-import-keys refresh \
    && zypper install -l -y vim \
    && zypper clean --all

RUN groupadd ${NON_ROOT_USER} \
    && useradd -m ${NON_ROOT_USER} \
    && usermod -aG ${NON_ROOT_USER} ${NON_ROOT_USER}

USER ${NON_ROOT_USER}
ENV HOME /home/${NON_ROOT_USER}

WORKDIR ${HOME}

RUN mkdir $HOME/.local/bin/ \
    && curl -sSL -H "X-JFrog-Art-Api:${CI_REGISTRY_USER_ARM_TOKEN}" https://${ARM_GENERIC_PORTAL_REPO}/external/kubernetes/kubectl -o $HOME/.local/bin/kubectl \
    && curl -sSL -H "X-JFrog-Art-Api:${CI_REGISTRY_USER_ARM_TOKEN}" https://${ARM_GENERIC_PORTAL_REPO}/external/kubernetes/helm -o $HOME/.local/bin/helm \
    && chmod +x $HOME/.local/bin/*

ENV PATH="${PATH}:${HOME}/.local/bin/"

COPY --chown=eallprod:eallprod ./mapr-spark ${HOME}/mapr-spark
COPY ./kubeconfig_corey006_eallprod.yaml ${HOME}/kubeconfig_corey006_eallprod.yaml
COPY ./deploy_check.sh ${HOME}/deploy_check.sh

ENV KUBECONFIG ${HOME}/kubeconfig_corey006_eallprod.yaml

ENTRYPOINT [ "deploy_check.sh" ]