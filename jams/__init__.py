# -*- coding: utf-8 -*- 
import sys
import os
import time
from watchdog.observers import Observer
from collection import JamCollection, JamFileHandler
from terminal import Terminal

JAM_DIR = "/Users/phil/Rushmore jams/"


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    observer = Observer()
    jam_collection = JamCollection()

    valid_filepaths = []
    for dirpath, dirnames, filenames in os.walk(JAM_DIR):
        files_with_paths = [os.path.join(dirpath, filename) for filename in filenames if JamCollection.valid_file_check(filename)]
        if len(files_with_paths) > 0:
            jam_collection.batch_add_tracks(files_with_paths)

    event_handler = JamFileHandler(jam_collection)

    observer.schedule(event_handler, JAM_DIR, recursive=True)
    observer.start()

    term = Terminal(jam_collection)
    term.cmdloop()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    # observer.join()
