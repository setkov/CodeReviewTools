
from TfsApi import TfsApi
import json
import logging
import random

class CodeReviewTools():

    def __init__(self, configPath="CodeReviewTools.json"):

        logging.basicConfig(filename = "CodeReviewTools.log", level = logging.INFO, format = "%(asctime)s - %(module)s - %(levelname)s - %(message)s")
        logging.info("")
        logging.info("CodeReviewTools start")

        with open(configPath, "r") as configFile:
            self.config = json.load(configFile)
            logging.info("read configuration file: %s", configPath)

        self.tfs = TfsApi(self.config["tfs_instance"])
        logging.info("connect to TFS: %s", self.config["tfs_instance"])

    def __del__(self):

        logging.info("CodeReviewTools end")

    def addCodeReviews(self, fromDate):

        items_project = self.config["items_project"]
        for code_project in self.config["code_projects"]:
            logging.info("project: %s", code_project["project"])
            for branche in code_project["branches"]:
                logging.info("branche: %s", branche)
                            
                changesets = self.tfs.changesets(code_project["project"], branche, fromDate)
                if changesets is None or len(changesets["value"]) == 0:
                    logging.info("changesets not found")
                else:
                    for changeset in changesets["value"]:

                        id = str(changeset["changesetId"])
                        user = changeset["author"]["displayName"]
                        date = changeset["createdDate"][:19].replace("T", " ")
                        comment = changeset["comment"] if "comment" in changeset else ""
                        logging.info("changeset: %s %s %s %s", id, user, date, comment)

                        codeReviewRequest = self.tfs.codeReviewRequest(items_project, id)
                        if not codeReviewRequest is None:
                            logging.info("code review request: %s", codeReviewRequest["workItems"][0]["id"])
                        else:
 
                            requester = changeset["author"]["uniqueName"]
                            while True:
                                reviewer = random.choice(code_project["reviewers"])
                                if reviewer != requester:
                                    break

                            # fields for Code Review Request
                            areaPath = {"path": "/fields/System.AreaPath", "value": code_project["project"]}
                            iterationPath = {"path": "/fields/System.IterationPath", "value": code_project["project"]}
                            history = {"path": "/fields/System.History", "value": "Created by CodeReviewTools"}
                            contextType = {"path": "/fields/Microsoft.VSTS.CodeReview.ContextType", "value": "Changeset"}
                            context = {"path": "/fields/Microsoft.VSTS.CodeReview.Context", "value": id}
                            title = {"path": "/fields/System.Title", "value": comment}
                            assignedTo = {"path": "/fields/System.AssignedTo", "value": requester}

                            # add Code Review Request
                            fields = [areaPath, iterationPath, history, contextType, context, title, assignedTo]
                            codeReviewRequest = self.tfs.workItem_add(items_project, "Code Review Request", fields)
                            if not codeReviewRequest is None:
                                logging.info("add code review request: %s, assigned to: %s", str(codeReviewRequest["id"]), requester)

                                # fields for Code Review Response
                                assignedTo = {"path": "/fields/System.AssignedTo", "value": reviewer}
                                relation = {"rel": "System.LinkTypes.Hierarchy-Reverse", "url": codeReviewRequest["url"]}
                                relations = {"path": "/relations/-", "value": relation}

                                # add Code Review Response
                                fields = [areaPath, iterationPath, history, title, assignedTo, relations]
                                codeReviewResponse = self.tfs.workItem_add(items_project, "Code Review Response", fields)
                                if not codeReviewResponse is None:
                                    logging.info("add code review response: %s, assigned to: %s", str(codeReviewResponse["id"]), reviewer)

def main():
    tools = CodeReviewTools()
    date = "2018-11-15"
    tools.addCodeReviews(date)

if __name__ ==  "__main__":
    main()