#!/bin/bash

hostname="$1auth/login"
pw=$2
login=$3
curl $hostname -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"password\": \"$pw\", \"login\": \"$login\"}" -k -v >output 2>&1

token=$(grep -oP "Authorization: \K.*" output)
echo $token
