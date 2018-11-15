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
            'Authorization': b'Basic ' + base64.b64encode(personal_access_token.encode('utf-8'))
        }

        self.params = {'api-version': '1.0'}

    def changesets(self, project, itemPath, fromDate):
        """ get changesets """
        
        params = copy.deepcopy(self.params)
        params["searchCriteria.itemPath"] = itemPath
        params["searchCriteria.fromDate"] = fromDate
        params["$orderby"] = "id asc"

        response = requests.get(self.instance + "/DefaultCollection/" + project + "/_apis/tfvc/changesets", headers = self.headers, params = params)
        if response.ok:
            return response.json()

    def codeReviewRequest(self, project, changesetId):
        """ get code review item from changeset id """

        query = {"query": "SELECT [Id], [Assigned To] FROM WorkItems WHERE [Work Item Type] = 'Code Review Request' AND [Associated Context] = " + changesetId}
        response = requests.post(self.instance + "/DefaultCollection/" + project + "/_apis/wit/wiql", headers = self.headers, params = self.params, json = query)
        if response.ok:
            return response.json()