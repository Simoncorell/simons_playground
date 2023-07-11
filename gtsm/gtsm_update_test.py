'''
Python Script for making requests to GTSM instance.
Initialize the token and push the Test Case Verdict.
'''

import subprocess
import sys
import logging
from xml.dom.minidom import parseString
import requests
import urllib3
from dicttoxml import dicttoxml

logging.getLogger("requests").setLevel(logging.DEBUG)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class TestCaseVerdict:
    '''
    Class for handling GTSM requests.
    '''
    def __init__(self, hostname, pw, username, testcaseid, jobinstance,
                testcaseversion, softwareversion, verdict):
        self._hostname = hostname
        self._pw = pw
        self._username = username
        self._testcaseid = testcaseid
        self._jobinstance = jobinstance
        self._testcaseversion = testcaseversion
        self._softwareversion = softwareversion
        self._verdict = verdict
        self._headers = ""
        self._json_dict = ""

    def init_gtsm_headers(self):
        '''
            Login to the gtsm instance and retrieved the token.
            Save the neccessary headers.
        '''
        token = self.login()

        if len(token) == 0:
            print("Enable to retrieve the token. Please check your credentials!")
            sys.exit(1)

        self._headers = {
                        'Accept':'application/json',
                        'Content-type': 'application/json',
                        'Authorization': token
                        }

    def login(self):
        '''
            Login and retrieve the token.
        '''
        result = subprocess.run(["./login_get_token.sh", self._hostname, self._pw, self._username],
                stdout=subprocess.PIPE,
                check=True
                )
        return result.stdout.decode("utf-8").rstrip()

    def list_test_case(self):
        '''
            Retrieves names for given Test Case ID.
        '''
        data = {
                "ids": [str(self._testcaseid)],
                "id": str(self._testcaseid)
            }

        try:
            response = requests.post(self._hostname + "tcm/test-cases/names",
                                    headers = self._headers,verify = False, json = data)
        except:
            print("Unable to make list-test-case request")
            sys.exit(1)

        if response.status_code == 200:
            print("OK!")
        else:
            print("Not OK!")
            print(response.json())
            sys.exit(1)

    def create_test_verdict(self):
        '''
            Create test case verdict for given Test Case ID.
        '''
        data = {
                "optionalParameters": {
                    "softwareVersion": str(self._softwareversion)
                },
                "verdictEnum": str(self._verdict),
                "jobInstance": str(self._jobinstance)
            }
        try:
            response = requests.post(self._hostname + "mtv/tc-verdicts/test-cases/"
                                    + self._testcaseid + "/versions/" + self._testcaseversion,
                                    headers = self._headers, verify = False, json = data)
        except:
            print("Unable to make create-test-case-verdict request")
            sys.exit(1)

        if response.status_code == 200:
            print("OK!")
            self._json_dict = response.json()
        else:
            print("Not OK!")
            print(response.json())
            sys.exit(1)

    def json_to_xml_file(self):
        '''
            Convertes and saves the json reply into a xml file.
            Also use pretty xml to make the file more readable.
        '''
        xml = dicttoxml(self._json_dict, attr_type=False)

        with open("json_response.xml", "w") as file:
            dom = parseString(xml)
            file.write(dom.toprettyxml())
            file.close()

def main(hostname, password, username, testcaseid, jobinstance,
        testcaseversion, softwareversion, verdict):
    '''
        Args: hostname: URL of the gtsm instance.
              pw: Password for the gtsm user.
              username: Username for the gtsm user.
              testcaseid: The ID for the test case to create verdict for.
              jobinstance: The job instance name to create the verdict for.
              testcaseversion: The test case version.
              softwareversion: Additional fields added by Alliance:
                               The software version of rdi-dashboard. Starting with 1.0.0
              verdict: Verdict of the test case. SUCCESS or FAILURE.

        Function: Creates testverdict obj with all neccessary members.
                  Login to the gtsm instance and get the headers including the token.
                  Through a request to the gtsm instance; Create a test case verdict.
                  Get the json reply and convertes/saves into a xml file.
    '''
    testverdict_obj = TestCaseVerdict(hostname, password, username, testcaseid, jobinstance,
                                     testcaseversion, softwareversion, verdict)
    testverdict_obj.init_gtsm_headers()
    testverdict_obj.create_test_verdict()
    testverdict_obj.json_to_xml_file()

if __name__ == '__main__':
    main(sys.argv[1],
         sys.argv[2],
         sys.argv[3],
         sys.argv[4],
         sys.argv[5],
         sys.argv[6],
         sys.argv[7],
         sys.argv[8])
