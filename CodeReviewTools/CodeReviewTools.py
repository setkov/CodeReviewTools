
from TfsApi import TfsApi
import json

# read configuration file
with open("CodeReviewTools.json", "r") as configFile:
    config = json.load(configFile)

tfs = TfsApi(config["tfs_instance"])

for code_project in config["code_projects"]:
    print("project:", code_project["project"])
    for branche in code_project["branches"]:
        print(" branche:", branche)
                            
        changesets = tfs.changesets(code_project["project"], branche, "2018-11-01")
        if changesets is None:
            print("  Changesets not found")
        else:
            for changeset in changesets["value"]:
                print("  Changeset:", changeset["changesetId"], changeset["createdDate"], changeset["author"]["displayName"], changeset["comment"] if "comment" in changeset else "")


