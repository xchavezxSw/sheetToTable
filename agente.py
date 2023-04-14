import logging


class Logger:
    def __init__(self, logger_name):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)
        self.ch = logging.StreamHandler()
        self.ch.setLevel(logging.DEBUG)
        self.logger.addHandler(self.ch)
        self.fh = logging.FileHandler('debug.log')
        self.fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.fh.setFormatter(formatter)
        self.logger.addHandler(self.fh)
        self.levels = []
        
    def __call__(self, func):
        def wrapped_func(*args, **kwargs):
            level = len(self.levels)
            indent = "   " * level
            if level > 0:
                parent = self.levels[-1]
                self.logger.debug(f"{indent}{'|'}-- Calling function '{func.__name__}' from '{parent}' with arguments: {args}, {kwargs}")
            else:
                self.logger.debug(f"{indent}{'|'}-- Calling function '{func.__name__}' with arguments: {args}, {kwargs}")
            self.levels.append(func.__name__)
            result = func(*args, **kwargs)
            self.levels.pop()
            if level > 0:
                parent = self.levels[-1]
                self.logger.debug(f"{indent}{'|'}-- Function '{func.__name__}' returned: {result} (called from '{parent}')")
            else:
                self.logger.debug(f"{indent}{'|'}-- Function '{func.__name__}' returned: {result}")
            return result
        return wrapped_func
