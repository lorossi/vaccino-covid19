class Backup:
    def __init__(self):
        return

    def backup(self):
        from git import Repo
        # now push all to to github
        # repo folder is parent
        repo = Repo(".", search_parent_directories=True)
        # add all modified files
        repo.git.add("-A")
        repo.index.commit("updated data")
        # pull and push
        repo.git.pull()
        repo.git.push()


if __name__ == "__main__":
    b = Backup()
    b.backup
