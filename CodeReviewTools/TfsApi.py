import base64
import copy
import json
import logging
import requests

class TfsApi():
    """ TFS API class """

    def __init__(self, instance):

        self.instance = instance

        with open("TfsPat.json", "r") as tokensFile:
            self.tokens = json.load(tokensFile)

        tfs_api_token = ":" + self.tokens["tfs_api_token"]
        
        self.headers = {
            "Content-type": "application/json",
            "Authorization": b"Basic " + base64.b64encode(tfs_api_token.encode("utf-8"))
        }

        self.params = {"api-version": "1.0"}

    def changesets(self, project, itemPath, fromDate):
        """ get changesets """
        
        params = copy.deepcopy(self.params)
        params["searchCriteria.itemPath"] = itemPath
        params["searchCriteria.fromDate"] = fromDate
        params["$orderby"] = "id asc"
        params["maxCommentLength"] = "2000"

        response = requests.get(self.instance + "/DefaultCollection/" + project + "/_apis/tfvc/changesets", headers = self.headers, params = params)
        if not response.ok:
            logging.error(str(response.status_code) + " " + response.reason)
        else:
            return response.json()

    def codeReviewRequest(self, project, changesetId):
        """ get code review item from changeset id """

        query = {"query": "SELECT [Id] FROM WorkItems WHERE [Work Item Type] = 'Code Review Request' AND [Associated Context] = '%s'" % changesetId}
        response = requests.post(self.instance + "/DefaultCollection/" + project + "/_apis/wit/wiql", headers = self.headers, params = self.params, json = query)
        if not response.ok:
            logging.error(str(response.status_code) + " " + response.reason)
        elif len(response.json()["workItems"]) == 1:
            return response.json()

    def workItem(self, project, url):
        """ get work item by url """

        response = requests.get(url, headers = self.headers, params = self.params)
        if not response.ok:
            logging.error(str(response.status_code) + " " + response.reason)
        else:
            return response.json()

    def workItem_add(self, project, workItemTypeName, fields, account = None):
        """ add new work item; fields - list of dict {path: ..., value: ...} """

        headers = copy.deepcopy(self.headers)
        headers["Content-type"] = "application/json-patch+json"
        if not account is None and account in self.tokens["requesters"]:
            account_token = ":" + self.tokens["requesters"][account]
            headers["Authorization"] = b"Basic " + base64.b64encode(account_token.encode("utf-8"))

        body = []
        for field in fields:
            body.append({"op": "add", "path": field["path"], "value": field["value"]})

        response = requests.patch(self.instance + "/DefaultCollection/" + project + "/_apis/wit/workitems/$" + workItemTypeName, headers = headers, params = self.params, json = body)
        if not response.ok:
            logging.error(str(response.status_code) + " " + response.reason)
        else:
            return response.json()





