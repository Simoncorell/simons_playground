ARG CBO_IMAGE_URL=armdocker.rnd.ericsson.se/proj-ldc/common_base_os_full/sles
ARG CBO_VERSION=3.39.0-7
FROM ${CBO_IMAGE_URL}:${CBO_VERSION}

# Installing some packages
ARG CBO_REPO=arm.sero.gic.ericsson.se/artifactory/proj-ldc-repo-rpm-local/common_base_os/sles/
ARG CBO_VERSION

RUN zypper addrepo --gpgcheck-strict -f https://${CBO_REPO}${CBO_VERSION} \
    COMMON_BASE_OS_SLES_REPO \
    && zypper --gpg-auto-import-keys refresh \
    && zypper install -l -y curl \
    && zypper install -l -y python3 \
    && zypper install -l -y python3-pip \
    && zypper refresh \
    && zypper clean --all

RUN zypper addrepo -C -G -f https://arm.sero.gic.ericsson.se/artifactory/proj-ldc-repo-rpm-local/adp-dev/adp-build-env/1.27.0/?ssl_verify=no \
    ADP_DEV_BUILD_ENV_REPO  \
    && zypper install -l -y vim \
    && zypper refresh \
    && zypper clean --all


RUN pip3 install openapi-client argo-workflows

RUN groupadd eallprod
RUN useradd eallprod
RUN usermod -aG root eallprod

USER eallprod

WORKDIR /eallprod
ARG WORKDIR=/eallprod

USER root

#These argoworkflow_api files are on my (ecrlsmn) local machine

RUN rm -rf /usr/lib/python3.6/site-packages/argo_workflows/api/api_client.py && rm -rf /usr/lib/python3.6/site-packages/argo_workflows/api/workflow_service_api.py && rm -rf /usr/lib/python3.6/site-packages/argo_workflows/model/io_argoproj_workflow_v1alpha1_workflow.py && rm -rf /usr/lib/python3.6/site-packages/argo_workflows/model/io_argoproj_workflow_v1alpha1_workflow_status.py && rm -rf /usr/lib/python3.6/site-packages/argo_workflows/model/io_argoproj_workflow_v1alpha1_node_status.py && rm -rf /usr/lib/python3.6/site-packages/argo_workflows/model/io_argoproj_workflow_v1alpha1_log_entry.py && rm -rf /usr/lib/python3.6/site-packages/argo_workflows/model/pipeline_log_entry.py

ADD --chown=eallprod:eallprod ./argo-workflow-api-stuff/api_client.py /usr/lib/python3.6/site-packages/argo_workflows/api/api_client.py
ADD --chown=eallprod:eallprod ./argo-workflow-api-stuff/workflow_service_api.py /usr/lib/python3.6/site-packages/argo_workflows/api/workflow_service_api.py
ADD --chown=eallprod:eallprod ./argo-workflow-api-stuff/io_argoproj_workflow_v1alpha1_workflow.py /usr/lib/python3.6/site-packages/argo_workflows/model/io_argoproj_workflow_v1alpha1_workflow.py
ADD --chown=eallprod:eallprod ./argo-workflow-api-stuff/io_argoproj_workflow_v1alpha1_workflow_status.py /usr/lib/python3.6/site-packages/argo_workflows/model/io_argoproj_workflow_v1alpha1_workflow_status.py
ADD --chown=eallprod:eallprod ./argo-workflow-api-stuff/io_argoproj_workflow_v1alpha1_node_status.py /usr/lib/python3.6/site-packages/argo_workflows/model/io_argoproj_workflow_v1alpha1_node_status.py
ADD --chown=eallprod:eallprod ./argo-workflow-api-stuff/io_argoproj_workflow_v1alpha1_log_entry.py /usr/lib/python3.6/site-packages/argo_workflows/model/io_argoproj_workflow_v1alpha1_log_entry.py
ADD --chown=eallprod:eallprod ./argo-workflow-api-stuff/pipeline_log_entry.py /usr/lib/python3.6/site-packages/argo_workflows/model/pipeline_log_entry.py

USER eallprod

WORKDIR /eallprod
ARG WORKDIR=/eallprod

COPY argo_workflow_main.py ${WORKDIR}
COPY outliers_system_test_template.yaml ${WORKDIR}

CMD ["python3", "argo_workflow_main.py", "https://des-argo.ews.gic.ericsson.se", "outliers-system-tests", "outliers_system_test_template.yaml"]

ENV PYTHONWARNINGS="ignore:Unverified HTTPS request"