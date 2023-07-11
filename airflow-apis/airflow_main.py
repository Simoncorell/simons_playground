#!/usr/bin/python3

"""
Python Script for sending API calls to an Airflow instance.
Used for starting, checking and getting logs for/from Airflow DAGs.
"""

from operator import ge
import time
import sys
import random
from pprint import pprint

import airflow_python_sdk
from airflow_python_sdk.api import task_instance_api
from airflow_python_sdk.api import monitoring_api
from airflow_python_sdk.model.dag_run import DAGRun
from airflow_python_sdk.api import dag_run_api

def get_dag_run_logs(api_client, dag_id, dag_run_id):
    """
    Function for getting the logs from the finsished DAG.
    """
    api_instance = task_instance_api.TaskInstanceApi(api_client)
    task_id = dag_id
    task_try_number = 1  # int | The task try number.
    try:
        # Get logs
        api_response = api_instance.get_log(
            dag_id, dag_run_id, task_id, task_try_number)
        pprint(api_response)
    except airflow_python_sdk.ApiException as airflow_exception:
        print("Exception when calling TaskInstanceApi->get_log: %s\n" % airflow_exception)

def check_airflow_health(api_client):
    """
    Function for getting the health of the Airflow Scheduler and
    Metadatabase.
    """
    # Create an instance of the API class Monitoring
    api_instance = monitoring_api.MonitoringApi(api_client)
    try:
        print("Beginning checking health of Airflow MetaDatabase & Scheduler")
        # Get instance status
        api_response = api_instance.get_health()
        if str(api_response.metadatabase.status) == "healthy" \
           and str(api_response.scheduler.status) == "healthy":
            print("Both Airflow Metadatabase & Scheduler are healthy! \nContinuing....")
        else:
            print("Airflow is not healthy! \nExiting...")
            sys.exit(1)

    except airflow_python_sdk.ApiException as airflow_exception:
        print("Exception when calling MonitoringApi->get_health: %s\n" % airflow_exception)
        sys.exit(1)

def get_dag_run(api_client, dag_id, dag_run_id):
    """
    Function handling the logic of checking the status of the DAG previous started.
    """
    api_instance = dag_run_api.DAGRunApi(api_client)

    start_getting_dag = time.time()

    while True:
        try:
            # Get a DAG run
            api_response = api_instance.get_dag_run(dag_id, dag_run_id)

            now = time.time()
            time_elapsed = now - start_getting_dag

            if str(api_response.state) == "queued":
                print(f"{dag_run_id} is queued!\nSleeping for 10 secs...")
                time.sleep(10)
                # Let's say maximum time standing in queue is 10 minutes for now
                if time_elapsed > 600:
                    print(f"{dag_run_id} has waiting over 10 minutes in queue!\n\
                            This is to long time.\nExiting....")
                    sys.exit(1)
            elif str(api_response.state) == "running":
                print(f"{dag_run_id} is running! \n\
                      Let's sleep for 60 seconds before checking again.")
                time.sleep(60)
            elif str(api_response.state) == "failed":
                print(f"{dag_run_id} has failed!\nGetting logs...")
                return False
            elif str(api_response.state) == "success":
                print(f"{dag_run_id} has succeded!\nGetting logs...")
                return True
            else:
                print(f"{dag_run_id} has an unepected status!\nExiting....")
                sys.exit(1)

        except airflow_python_sdk.ApiException as airflow_exception:
            print("Exception when calling DAGRunApi->get_dag_run: %s\n" % airflow_exception)

        print(f"It has been {time_elapsed} seconds since the execution of dag started")
        if time_elapsed > 3600: # Let's say maximum time is 1 hours for now
            print(f"{dag_run_id} has taken over 1 hour to finish!\nThis is to long time.\
                  \nExiting....")
            sys.exit(1)

def start_dag_run(api_client, dag_id, commit_id, rng, gerrit_ref):
    """
    Function for starting the DAG.
    """
    api_instance = dag_run_api.DAGRunApi(api_client)
    # DAGRun
    dag_run = DAGRun(
        dag_run_id=f"{dag_id}-{commit_id}-{rng}",
    )
    dag_run.conf = {"gerrit_ref":f"{gerrit_ref}"}
    try:
        print(f"Beginning of starting DAG with {dag_id}")
        # Trigger a new DAG run
        api_response = api_instance.post_dag_run(dag_id, dag_run)
        pprint(api_response)
    except airflow_python_sdk.ApiException as airflow_exception:
        print("Exception when calling DAGRunApi->post_dag_run: %s\n" % airflow_exception)
    return dag_run.dag_run_id

def main(url, username, password, dag_id, commit_id, gerrit_ref):
    """
    Main for airflow_main.py.
    exists with stderr if DAG run was a failure and stdout if DAG run
    was a success.
    """
    configuration = airflow_python_sdk.Configuration(
        host=url,
        username=username,
        password=password
    )
    rng = random.randrange(0,100000,1)
    api_client = airflow_python_sdk.ApiClient(configuration)
    check_airflow_health(api_client)
    dag_run_id = start_dag_run(api_client, dag_id, commit_id, rng, gerrit_ref)
    succeded = get_dag_run(api_client, dag_id, dag_run_id)
    get_dag_run_logs(api_client, dag_id, dag_run_id)

    if succeded:
        print(f"Execution of {dag_id} was a SUCCESS!")
        sys.exit(0)
    else:
        print(f"Execution of {dag_id} was a FAILURE!")
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
