SDM IMAGE

# A minimalistic Docker CBO image with 3 SDM purposes. 
  Generating the SDM.json (for repo and artifactory ) via python script. Therefore need to install Python Interpreter & Python libs (via pip) used in script.
  Push the Artifactory SDM.json to Artifactory via cURL. Need to install cURL via package manager zypper. 
  Push the repo SDM.json to git refs/notes via git push. Need to have git installed (it came with the CBO version). 


Added the unix user eallprod since this is the functional user to be used in pipeline. 

