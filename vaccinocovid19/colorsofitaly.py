import ujson


class ColorsOfItaly:
    def __init__(self):
        self._paths = []
        self._ota = {}

        self.loadSettings()

    def loadSettings(self):
        # open paths file
        with open("src/settings/settings.json") as f:
            self._paths = ujson.loads(f.read())
        # open ota settings
        with open("src/settings/ota.json") as f:
            self._ota = ujson.loads(f.read())

    @property
    def ota_infos(self):
        return self._ota
