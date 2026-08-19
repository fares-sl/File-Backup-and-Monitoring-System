import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ChangeHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print(f'created: {event.src_path}')

    def on_modified(self, event):
        if not event.is_directory:
            print(f'modified: {event.src_path}')

    def on_deleted(self, event):
        if not event.is_directory:
            print(f"DELETED: {event.src_path}")

    def on_moved(self, event):
        if not event.is_directory:
            print(f"MOVED: {event.src_path} -> {event.dest_path}")

if __name__ == '__main__':
    path_to_watch = "./test_folder"
    handler = ChangeHandler()
    observer = Observer()
    observer.schedule( handler, path_to_watch, recursive = True)
    observer.start()
    print(f"watching {path_to_watch}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
