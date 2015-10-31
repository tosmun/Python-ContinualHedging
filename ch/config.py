import os.path, configparser

class Configuration(configparser.ConfigParser):
    _MAIN = 'MAIN'
    def __init__(self, path=None):
        super(Configuration, self).__init__(strict=False)
        # If file path was provided, read it
        if path is not None:
            # Expand path
            path = os.path.expanduser(path)
            # Ensure exists
            if not os.path.exists(path):
                raise IOError('Configuration file "%s" does not exist' % path)
            # Read the ch_config file
            with open(path, 'r') as configFile:
                self.read_file(configFile)
                
    def getLogFilePath(self):
        return os.path.expanduser(self.get(self._MAIN, 'logFile'))
    def getLogLevel(self):
        return self.get(self._MAIN, 'logLevel')