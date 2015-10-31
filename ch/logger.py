import logging

class Log(logging.Logger):
    _FORMAT='%(asctime)-15s [%(process)d] [%(thread)d, %(threadName)s] [%(name)s] [%(levelname)s]: %(message)s'

    def __init__(self, configuration, name=None):
        if configuration is None:
            raise Exception("No configuration provided")
        path = configuration.getLogFilePath()
        if path is None:
            raise Exception("No log path provided")
        level = configuration.getLogLevel()
        if level is None:
            raise Exception("No log level provided")
        level = self._getLogLevel(level)
        super(Log, self).__init__(name=name)
        self.setLevel(level)
        fileHandler = logging.FileHandler(filename=path, mode='a')
        fileHandler.setFormatter(logging.Formatter(fmt=self._FORMAT))
        self.addHandler(fileHandler)
        
    def isDebugEnabled(self):
        return self.isEnabledFor(logging.DEBUG)
    
    def _getLogLevel(self, levelStr):
        if levelStr is None:
            return None
        # Sanitize
        levelStr = levelStr.strip().upper()
        if levelStr == 'INFO':
            return logging.INFO
        elif levelStr == 'WARN':
            return logging.WARN
        elif levelStr == 'ERROR':
            return logging.ERROR
        elif levelStr == 'DEBUG':
            return logging.DEBUG
        elif levelStr == 'CRITICAL':
            return logging.CRITICAL
        elif levelStr == 'FATAL':
            return logging.FATAL
        else:
            return None