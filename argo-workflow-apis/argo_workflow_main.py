#!/usr/bin/python3

from pprint import pprint

import argo_workflows
from argo_workflows.api import workflow_service_api
from argo_workflows.model.io_argoproj_workflow_v1alpha1_workflow_create_request import \
    IoArgoprojWorkflowV1alpha1WorkflowCreateRequest
from openapi_client.rest import ApiException
import requests
import yaml
import time
import sys
import re

def create_workflow(api_client, namespace, workflow_yaml):
    try:
        api_instance = workflow_service_api.WorkflowServiceApi(api_client)

        with open(workflow_yaml, 'r') as file:
            manifest = yaml.safe_load(file)

        api_response = api_instance.create_workflow(
            namespace=namespace,
            body=IoArgoprojWorkflowV1alpha1WorkflowCreateRequest(workflow=manifest, _check_type=False),
            _check_return_type=False)
    except ApiException as e:
        print("Exception when calling WorkflowServiceApi->create_workflow: %s\n" % e)
    return api_response.metadata['name']

def check_workflow(api_client, name, namespace):
    api_instance = workflow_service_api.WorkflowServiceApi(api_client)
    start_getting_dag = time.time()

    while (True):
        try:
            api_response = api_instance.get_workflow(namespace, name)
            now = time.time()
            time_elapsed = now - start_getting_dag

            if str(api_response.status['started_at']) == "None":
                print(f"{name} have not started yet!\nSleeping for 10 secs...")
                time.sleep(10)
                if time_elapsed > 600: # Let's say maximum time standing in queue is 10 minutes for now
                    print(f"{name} has waiting over 10 minutes in queue!\nThis is to long time.\nExiting....")
                    sys.exit(1)

            elif str(api_response.status['phase']) == "Running":
                print(f"{name} is running!\nSleeping for 60 secs...")
                time.sleep(60)
            elif str(api_response.status['phase']) == "Succeeded":
                print(f"{name} have Succeeded!\nGetting logs...")
                return {"succeeded": True, "namespace": namespace, "name": name}
            elif str(api_response.status['phase']) == "Failed":
                print(f"{name} have failed!\nGetting logs...")
                return {"succeeded": False, "namespace": namespace, "name": name}
            else:
                print(f"{name} have an unexpected status!\nExiting...")
                sys.exit(1)
        except ApiException as e:
            print("Exception when calling WorkflowServiceApi->get_workflow: %s\n" % e)

        print(f"It has been {time_elapsed} seconds since the execution of {name} started")
        if time_elapsed > 3600: # Let's say maximum time is 1 hours for now
            print(f"{name} has taken over 1 hour to finish!\nThis is to long time.\nExiting....")
            sys.exit(1)

def get_workflow_logs(api_client, workflow_dict):
    api_instance = workflow_service_api.WorkflowServiceApi(api_client)
    try:
        api_response = api_instance.workflow_logs(workflow_dict["namespace"], workflow_dict["name"], log_options_container="main")
        # Received data is a large string with a ugly format. Did some cleanup with regex.
        x = re.sub("{\"result\":{\"content\":\"", "", api_response)
        x = re.sub("{\"result\":{\"", "", x)
        x = re.sub("\"podName\":\".*", "", x)
        x = re.sub("podName\":\".*", "", x)
        pprint(x)

    except ApiException as e:
        print("Exception when calling WorkflowServiceApi->workflow_logs: %s\n" % e)
    return workflow_dict["succeeded"]

def main(host, namespace, workflow_yaml):
    configuration = argo_workflows.Configuration(host=host)
    configuration.verify_ssl = False
    api_client = argo_workflows.ApiClient(configuration)
    if get_workflow_logs(api_client, check_workflow(api_client, create_workflow(api_client, namespace, workflow_yaml), namespace)):
        print("Outliers System Test was a SUCCESS!")
        sys.exit(0)
    else:
        print("Outliers System Test was a FAILURE!")
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])