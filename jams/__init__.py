import os
import sys
import time
import logging
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import uuid

JAM_DIR = "/Users/phil/Rushmore jams/"

class JamTrack(object):

    def __init__(self, filepath, *args, **kwargs):
        self.id = uuid.uuid1()
        self.filepath = filepath


class JamCollection(object):

    def __init__(self, *args, **kwargs):

        self.jams = {}

    def skip(self):
        pass

    def play(self):
        pass

    @staticmethod
    def valid_file_check(filepath):
        if filepath.endswith('.mp3'):
            return True
        return False

    def add_track(self, filepath):
        if not self.valid_file_check(filepath):
            return
        new_track = JamTrack(filepath)
        self.jams[new_track.id] = new_track 
        happy_file_name = filepath.split('/')[-1].split('.')[0]
        intro_voice_proc = subprocess.Popen(["say", happy_file_name], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        intro_voice_proc.wait()
        play_proc = subprocess.Popen(["mpg321", filepath], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def remove_track(self, filepath):
        pass

class JamFileHandler(FileSystemEventHandler):

    def __init__(self, collection, *args, **kwargs):
        self.jam_collection = collection
        super(JamFileHandler, self).__init__(*args, **kwargs)

    def dispatch(self, event):
        if not event.is_directory:
            super(JamFileHandler, self).dispatch(event)

    def on_created(self, event):
        filepath = event.src_path
        if JamCollection.valid_file_check(filepath):
            self.jam_collection.add_track(filepath)

    # def on_deleted(self, event):
    #     filepath = event.src_path
    #     if JamCollection.valid_file_check(filepath) and filepath in self.jams.keys():
    #         del self.jam_collection.remove_track(filepath)

    def on_modified(self, event):
        pass

    # def on_moved(self, event):
    #     old_filepath = event.from_path
    #     if JamCollection.valid_file_check(old_filepath) and old_filepath in self.jams.keys():
    #         new_file_path = event.src_path
    #         self.jams[new_file_path] = self.jams[old_filepath]
    #         del self.jams[old_filepath]


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    observer = Observer()
    jam_collection = JamCollection()
    event_handler = JamFileHandler(jam_collection)
    observer.schedule(event_handler, JAM_DIR, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
