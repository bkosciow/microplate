class Handler:
    def __init__(self, *argv):
        self.workers = []
        for worker in argv:
            self.workers.append(worker)

    def add_worker(self, worker):
        self.workers.append(worker)

    def handle(self, message):
        raise NotImplementedError("handle not implemented")


class DecryptNotFound(Exception):
    pass


class NoDecodersDefined(Exception):
    pass


class EventOnStart:
    def on_start(self):
        raise NotImplementedError("EventOnStart not implemented")
