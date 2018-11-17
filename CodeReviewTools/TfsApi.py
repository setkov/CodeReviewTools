import copy
import base64
import requests

class TfsApi():
    """ TFS API class """

    def __init__(self, instance):

        self.instance = instance

        with open("TfsPat.txt", "r") as token:
            personal_access_token = ":" + token.read().strip()
        
        self.headers = {
            "Content-type": "application/json",
            "Authorization": b"Basic " + base64.b64encode(personal_access_token.encode("utf-8"))
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
        if response.ok:
            return response.json()

    def codeReviewRequest(self, project, changesetId):
        """ get code review item from changeset id """

        query = {"query": "SELECT [Id] FROM WorkItems WHERE [Work Item Type] = 'Code Review Request' AND [Associated Context] = '%s'" % changesetId}
        response = requests.post(self.instance + "/DefaultCollection/" + project + "/_apis/wit/wiql", headers = self.headers, params = self.params, json = query)
        if response.ok and len(response.json()["workItems"]) == 1:
            return response.json()

    def workItem(self, project, url):
        """ get work item by url """

        response = requests.get(url, headers = self.headers, params = self.params)
        if response.ok:
            return response.json()

    def workItem_add(self, project, workItemTypeName, fields):
        """ add new work item; fields - list of dict {path: ..., value: ...} """

        headers = copy.deepcopy(self.headers)
        headers["Content-type"] = "application/json-patch+json"

        body = []
        for field in fields:
            body.append({"op": "add", "path": field["path"], "value": field["value"]})

        response = requests.patch(self.instance + "/DefaultCollection/" + project + "/_apis/wit/workitems/$" + workItemTypeName, headers = headers, params = self.params, json = body)
        if response.ok:
            return response.json()





