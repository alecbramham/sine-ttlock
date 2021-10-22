# [START cloudrun_SineTTLock_service]
# [START run_SineTTLock_service]

import os
import time
import requests
import json
from typing import Text
from flask import Flask
from flask import request


app = Flask(__name__)


def UnlockKeysafe():
    content = request.json
    questionId = request.args.get("questionId")
    print("1. json Data Loaded")
    for i in content["data"]["formResponses"]["responses"]:
        if i["id"] == questionId and i["value"] == True:
            print("2. Key Required")
            return(True)


def SineTTLock():
    print("3. Importing Lock ID")
    lockId = request.args.get("lockId")
    print("4. Generating Unix Timestamp")
    date = int(round(time.time() * 1000))
    getUrl = "https://api.ttlock.com/v3/lock/unlock?lockId={}&clientId=bab50b785ed8424f9daf41e8e3c249d5&accessToken=45ef0dc52edd65f08a4c7a7021310947&date={}".format(lockId, date)
    print("5. Sending Get Request")
    response = requests.get(getUrl)
    statusCode = (response.status_code)
    urlText = (response.text)
    return statusCode, urlText


@app.route("/")
def Main():
    if UnlockKeysafe() == True:
        statusCode, urlText = SineTTLock()
        returnText = "Request Status: {} | Request Contents: {} | Key is required, opening key safe".format(statusCode, urlText)
        print("6. Program Ending")
        return(returnText)
    else:
        print("Unlock Request Not Required")
        return("Key is not required, ending program")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# [END run_SineTTLock_service]
# [END cloudrun_SineTTLock_service]
