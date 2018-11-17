
from TfsApi import TfsApi
import logging
import json

logging.basicConfig(filename = "CodeReviewTools.log", level = logging.INFO, format = "%(asctime)s - %(module)s - %(levelname)s - %(message)s")
logging.info("CodeReviewTools started")

# read configuration file
with open("CodeReviewTools.json", "r") as configFile:
    config = json.load(configFile)

logging.info("Connect to TFS %s", config["tfs_instance"])
tfs = TfsApi(config["tfs_instance"])

for code_project in config["code_projects"]:
    logging.info("project: %s", code_project["project"])
    for branche in code_project["branches"]:
        logging.info("branche: %s", branche)
                            
        changesets = tfs.changesets(code_project["project"], branche, "2018-11-01")
        if changesets is None:
            logging.info("Changesets not found")
        else:
            for changeset in changesets["value"]:
                id = changeset["changesetId"]
                user = changeset["author"]["displayName"]
                date = changeset["createdDate"][:19].replace("T", " ")
                comment = changeset["comment"] if "comment" in changeset else ""
                logging.info("changeset: %s %s %s %s", id, user, date, comment)

