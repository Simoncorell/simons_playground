#!/bin/bash

echo "Starting deploying helm chart"

envsubst < ./mapr-spark/values.yaml.template > ./mapr-spark/values.yaml

helm upgrade --install mapr-spark$1 mapr-spark --namespace outliers-system-tests

sleep 10

podname=$(kubectl get pods -l=app.kubernetes.io/managed-by=Helm,app.kubernetes.io/instance=mapr-spark$1 --namespace outliers-system-tests | awk NF=1 | grep mapr-spark)

while true
do
    status=$(kubectl describe pod $podname --namespace outliers-system-tests | grep "Status:" | awk '{print $NF}')

    if [ -z $status ]
    then
        echo "Pod not found! Probably due to error. Exiting."
        exit 1
    fi

    if [ $status == "Running" ]
    then
        echo "Test is still running!!!"
        echo "Sleeping for 60 secs...."
        sleep 60
        continue
    elif [ $status == "Succeeded" ]
    then
        echo "Test has Succeeded!!!"
        echo "Fetching logs......!!!"
        kubectl logs $podname --namespace outliers-system-tests
        echo "Deleting helm release mapr-spark$1"
        helm delete mapr-spark$1 --namespace outliers-system-tests
        echo "Exiting with stdout"
        exit 0
    elif [ $status == "Failed" ]
    then
        echo "Test has failed!!!"
        echo "Fetching logs......!!!"
        kubectl logs $podname --namespace outliers-system-tests
        echo "Deleting helm release mapr-spark$1"
        helm delete mapr-spark$1 --namespace outliers-system-tests
        echo "Exiting with stderr"
        exit 1
    else
        echo "Unexpected status! Exiting..."
        echo "Fetching logs......!!!"
        kubectl logs $podname --namespace outliers-system-tests
        echo "Deleting helm release mapr-spark$1"
        helm delete mapr-spark$1 --namespace outliers-system-tests
        exit 1
    fi
done




