import logging

class Backup:
    def __init__(self):
        logfile = "backup.log"
        logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s",
                            level=logging.INFO, filename=logfile,
                            filemode="a")
        return

    def backup(self):
        from git import Repo
        logging.info("Started backup process")
        # now push all to to github
        # repo folder is parent
        repo = Repo(".", search_parent_directories=True)
        repo.git.pull()
        logging.info("Repo pulled")
        # add all modified files
        repo.git.add("-A")
        logging.info("Added files")
        repo.index.commit("updated data")
        logging.info("Commit created")
        # push
        repo.git.push()
        logging.info("Repo pushed")


if __name__ == "__main__":
    b = Backup()
    logging.info("Item created")
    b.backup()
    logging.info("Backup completed")