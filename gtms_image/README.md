# Image used for sending GTMS test report

This README file provides some information about the image used for sending GTMS test reports. This directory contains the following files:
- README.md file with basic documentation
- Dockerfile used for building the image
- gtms_update_test.py file used for sending HTTP requests to the GTMS server via its API
- login_get_token.sh file used for retrieving authentication token for GTMS

## Dockerfile

The Dockerfile is built according to the Ericsson Common-Base OS standards. The following command-line utilities are installed:
- python3
- pip3 
- curl

Besides the command-line utilities, some python modules are installed which are necessary to run the script. Here they are:
- urllib3
- requests
- dicttoxml

This Dockerfile will create a user **eallprod** assigned to a group **eallprod**. The home directory for **eallprod** user will be `/home/eallprod` and **eallprod** will be the owner of the directory.

The last steps of Dockerfile include adding `gtms_update_test.py` and `login_get_token.sh` files to the working directory under ownership of **eallprod** user and **eallprod** group.

The image is pushed to artifactory as `armdocker.rnd.ericsson.se/proj-dsi-portal/daas-ut/send-test-result-to-gtms:1.0.0`.
