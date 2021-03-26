import re
import ujson
from datetime import datetime


class ColorsOfItaly:
    def __init__(self):
        self._paths = []
        self._emails = []
        self._ota = {}

        self.loadSettings()

    def loadSettings(self):
        # open paths file
        with open("src/settings/settings.json") as f:
            self._paths = ujson.loads(f.read())
        # open ota settings
        with open("src/settings/ota.json") as f:
            self._ota = ujson.loads(f.read())

    def loadEmails(self):
        file_path = self._paths["output_folder"] + \
            self._paths["emails"]

        with open(file_path) as f:
            self._emails = ujson.loads(f.read())

    def saveSettings(self):
        file_path = self._paths["output_folder"] + \
            self._paths["emails"]

        with open(file_path, "w") as f:
            ujson.dump(self._emails, f, indent=2)

    def addEmail(self, email):
        self.loadEmails()
        # remove spaces
        email = email.replace(" ", "")
        # set lowercase
        email = email.lower()
        if email not in self._emails["emails"]:
            self._emails["emails"][email] = datetime.now().isoformat()
            self.saveSettings()

    def parseEmail(self, email):
        if not email:
            # no email provided
            return 400

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            # dot after @
            return 400
        else:
            return 200

    @property
    def emails(self):
        self.loadEmails()
        emails = [e for e in self._emails["emails"]]
        return emails

    @property
    def ota_infos(self):
        return self._ota
