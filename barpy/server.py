from threading import Lock


class Server(object):
    def __init__(self, flask_app):
        self.done = False
        self.lock = Lock()
        self.app = flask_app

    def is_done(self):
        with self.lock:
            return self.done

    def shutdown(self):
        with self.lock:
            self.done = True
