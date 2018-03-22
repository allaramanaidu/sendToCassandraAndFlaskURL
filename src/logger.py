import logging
import configparser

class logger_class:
    def __init__(self, name):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.logtype = self.config['log']['level']
        self.loglocation = str(self.config['log']['location'])
        self.logger = logging.getLogger(name)
        self.formater = logging.Formatter('[%(asctime)s] [%(filename)-12s] [%(levelname)-8s] [%(message)s]')

        if self.loglocation == 'console':
            self.consoleHandler = logging.StreamHandler()
            self.consoleHandler.setFormatter(self.formater)
            self.logger.addHandler(self.consoleHandler)
            if self.logtype == 'INFO':
                self.consoleHandler.setLevel(logging.INFO)
            elif self.logtype == 'DEBUG':
                self.consoleHandler.setLevel(logging.DEBUG)
            elif self.logtype == 'ERROR':
                self.consoleHandler.setLevel(logging.ERROR)
            else :
                pass

        else:  # save into file
            self.fileHandler = logging.FileHandler('test.log')
            self.fileHandler.setFormatter(self.formater)
            self.logger.addHandler(self.fileHandler)
            if self.logtype == 'INFO':
                self.fileHandler.setLevel(logging.INFO)
            elif self.logtype == 'DEBUG':
                self.fileHandler.setLevel(logging.DEBUG)
            elif self.logtype == 'ERROR':
                self.fileHandler.setLevel(logging.ERROR)
            else:
                pass


    def something(self):
        pass