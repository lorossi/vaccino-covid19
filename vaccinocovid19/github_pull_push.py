from git import Repo
import glob


repo = Repo("..")

new_files = glob.glob("/src/output/*.json")
repo.git.add("-A")
repo.index.commit("updated data")
repo.git.push()
repo.git.pull()
