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


RUN pip3 install airflow-python-sdk

RUN groupadd eallprod
RUN useradd eallprod
RUN usermod -aG root eallprod

USER eallprod

WORKDIR /eallprod
ARG WORKDIR=/eallprod

COPY airflow_main.py ${WORKDIR}

USER root

#These airflow_api files are on my (ecrlsmn) local machine

#RUN rm -rf /usr/lib/python3.6/site-packages/airflow_python_sdk/rest.py && rm -rf /usr/lib/python3.6/site-packages/airflow_python_sdk/model/dag_run.py && rm -rf /usr/lib/python3.6/site-packages/airflow_python_sdk/model_utils.py && rm -rf /usr/lib/python3.6/site-packages/airflow_python_sdk/api/dag_run_api.py && rm -rf /usr/lib/python3.6/site-packages/airflow_python_sdk/model/dag_state.py

#ADD --chown=eallprod:eallprod ./airflow_api_sdk_stuff/rest.py /usr/lib/python3.6/site-packages/airflow_python_sdk/rest.py
#ADD --chown=eallprod:eallprod ./airflow_api_sdk_stuff/dag_run.py /usr/lib/python3.6/site-packages/airflow_python_sdk/model/dag_run.py
#ADD --chown=eallprod:eallprod ./airflow_api_sdk_stuff/model_utils.py /usr/lib/python3.6/site-packages/airflow_python_sdk/model_utils.py
#ADD --chown=eallprod:eallprod ./airflow_api_sdk_stuff/dag_run_api.py /usr/lib/python3.6/site-packages/airflow_python_sdk/api/dag_run_api.py
#ADD --chown=eallprod:eallprod ./airflow_api_sdk_stuff/dag_state.py /usr/lib/python3.6/site-packages/airflow_python_sdk/model/dag_state.py
USER eallprod

WORKDIR /eallprod
ARG WORKDIR=/eallprod

COPY airflow_main.py ${WORKDIR}

CMD ["python3", "airflow_main.py", "https://des-alliance-airflow.corey005.rnd.gic.ericsson.se/api/v1", "ealener", "ealener", "anomalies_benchmarking_test", "commit_id"]

ENV PYTHONWARNINGS="ignore:Unverified HTTPS request"