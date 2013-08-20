# -*- coding: utf-8 -*- 
import logging
import subprocess
from time import sleep
from watchdog.events import FileSystemEventHandler
import uuid


class JamTrack(object):

    def __init__(self, filepath, *args, **kwargs):
        self.id = uuid.uuid1()
        self.filepath = filepath

    def change_filepath(self, new_filepath):
        self.filepath = new_filepath


class JamCollection(object):

    def __init__(self, *args, **kwargs):
        self.jams = {}
        self.jam_filepaths = {}
        self.queue = []
        self.current_track = None

    def skip(self):
        pass

    def play(self):
        if len(self.queue) > 0:
            track_id = self.queue[0]
            self.play_track(track_id)
        return

    def stats(self):
        print '%s tracks' % len(self.jams)

    @staticmethod
    def valid_file_check(filepath):
        if filepath.endswith('.mp3'):
            return True
        return False

    def get_track(self, track_id):
        track = self.jams.get(track_id, None)
        if track is not None:
            return track

    def get_track_by_filepath(self, filepath):
        track_id = self.jam_filepaths.get(filepath, None)
        if track_id is None:
            return
        track = self.jams[track_id]
        return track

    def add_to_queue(self, track_id):
        self.queue.append(track_id)

    def batch_add_tracks(self, filepaths):
        for filepath in filepaths:
            self.add_track(filepath)

    def add_track(self, filepath):
        if not self.valid_file_check(filepath):
            return
        new_track = JamTrack(filepath)
        self.jams[new_track.id] = new_track 
        self.jam_filepaths[filepath] = new_track.id
        self.add_to_queue(new_track.id)

    def play_track(self, track_id):
        track = self.get_track(track_id)
        happy_file_name = track.filepath.split('/')[-1].split('.')[0]
        intro_voice_proc = subprocess.Popen(["say", happy_file_name], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        intro_voice_proc.wait()
        sleep(2)
        play_proc = subprocess.Popen(["mpg321", track.filepath], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def change_track_filepath(self, old_filepath, new_filepath):
        track = self.get_track_by_filepath(old_filepath)
        track.change_filepath(new_filepath)
        del self.jam_filepaths[old_filepath]
        self.jam_filepaths[new_filepath] = track

    def remove_track(self, track_id):
        del self.jams[track_id]
        return True

    def remove_track_by_filepath(self, filepath):
        track_id = self.jam_filepaths(filepath, None)
        if track_id is None:
            return
        success = self.remove_track(track_id)
        if success:
            del self.jam_filepaths[filepath]

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

    def on_deleted(self, event):
        filepath = event.src_path
        if JamCollection.valid_file_check(filepath) and filepath in self.jams.keys():
            self.jam_collection.remove_track_by_filepath(filepath)

    def on_modified(self, event):
        pass

    def on_moved(self, event):
        old_filepath = event.from_path
        if JamCollection.valid_file_check(old_filepath):
            new_filepath = event.src_path
            self.jam_collection.change_track_filepath(old_filepath, new_filepath)
