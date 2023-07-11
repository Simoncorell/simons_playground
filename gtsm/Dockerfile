# This is daas-integration-test-anomalies:1.0.0
FROM armdocker.rnd.ericsson.se/proj-dsi-portal/ecrlsmn/airflow_restapi:1.0.7

USER root

RUN pip3 install urllib3 requests dicttoxml

ADD --chown=eallprod:eallprod ./gtsm_update_test.py ${WORKDIR}
ADD --chown=eallprod:eallprod ./login_get_token.sh ${WORKDIR}
RUN chown eallprod:eallprod /eallprod/airflow_main.py && chmod 755 /eallprod/airflow_main.py

USER eallprod
