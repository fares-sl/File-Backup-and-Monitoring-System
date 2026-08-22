from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from local_db import createConnection
from actionHandlers import createFileHandler, modifyFileHandler, deleteFileHandler, moveFileHandler
from config import AGENT_DB
import config
import os
import time
from utilities import extension

class ChangeHandler(FileSystemEventHandler):
    def fetchConnection(self):
        if not hasattr(self, 'conn'):
            self.conn = createConnection(AGENT_DB)
        return self.conn
    def on_created(self, event):
        if not event.is_directory and extension(event.src_path) in config.WATCHED_EXTENSIONS:
            createFileHandler(self.fetchConnection(), event.src_path)

    def on_modified(self, event):
        if not event.is_directory and extension(event.src_path) in config.WATCHED_EXTENSIONS:
            modifyFileHandler(self.fetchConnection(), event.src_path)

    def on_deleted(self, event):
        if event.is_directory or extension(event.src_path) in config.WATCHED_EXTENSIONS:
            deleteFileHandler(self.fetchConnection(), event.src_path)
        
    def on_moved(self, event):
        if event.is_directory or extension(event.src_path) in config.WATCHED_EXTENSIONS:
            moveFileHandler(self.fetchConnection(), event.dest_path, event.src_path)
            
def ConfigurateWatchers(observer, handler, watchers, watchedRoots):
    for path in list(watchers):
        if path not in watchedRoots:
            observer.unschedule(watchers[path])
            watchers.pop(path)
    for root in watchedRoots:
        if root not in watchers:
            watchers[root] = observer.schedule(handler, root, recursive = True)


if __name__ == '__main__':
    path_to_watch = "./test_folder"
    path = os.path.abspath(path_to_watch)
    handler = ChangeHandler()
    observer = Observer()
    observer.schedule( handler, path, recursive = True)
    observer.start()
    print(f"watching {path}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
