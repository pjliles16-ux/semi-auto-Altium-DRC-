import os

class FileWatcher:

    def __init__(self, filepath, callback):
        self.filepath = filepath
        self.callback = callback
        self.last_modified = None

    def check(self):
        if not self.filepath:
            return

        modified = os.path.getmtime(self.filepath)

        if self.last_modified and modified != self.last_modified:
            self.callback()

        self.last_modified = modified