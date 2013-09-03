# -*- coding: utf-8 -*- 
from watchdog.events import FileSystemEventHandler
import uuid
from mutagen import File
from random import choice


class JamTrack(object):

    def __init__(self, filepath, *args, **kwargs):
        self.id = uuid.uuid1()
        self.filepath = filepath
        metadata = File(filepath)
        if 'TIT2' in metadata:
            self.title = str(metadata['TIT2'])
        else:
            self.title = 'Untitled Track'

        if 'TPE1' in metadata:
            self.artist = str(metadata['TPE1'])
        else:
            self.artist = 'Unkown Artist'

    def get_artist(self):
        return self.artist

    def get_title(self):
        return self.title

    def change_filepath(self, new_filepath):
        self.filepath = new_filepath


class JamCollection(object):

    def __init__(self, *args, **kwargs):
        self.jams = {}
        self.jam_filepaths = {}
        self.queue = []
        self.current_track = None

    def stats(self):
        stats_str = '%s tracks' % len(self.jams)
        stats_str += '\n'
        print stats_str

    @staticmethod
    def valid_file_check(filepath):
        if filepath.endswith('.mp3'):
            return True
        return False

    def get_track(self, track_id):
        track = self.jams.get(track_id, None)
        if track is not None:
            return track

    def get_next_track(self):
        track_id = self.queue.pop(0)
        self.queue.append(track_id)
        return self.jams[track_id]

    def get_random_track(self):
        random_track_id = choice(self.queue)
        track_index = self.queue.index(random_track_id)
        self.queue.pop(track_index)
        self.queue.append(random_track_id)

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
