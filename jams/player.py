# -*- coding: utf-8 -*-
import subprocess
import signal
from time import sleep


class JamPlayer(object):

    def __init__(self, collection, *args, **kwargs):
        self.collection = collection
        self.player_proc = None
        self.current_track =  None
        self.is_paused = False


    def play_track(self, track):
#        happy_file_name = track.filepath.split('/')[-1].split('.')[0]
        self.current_track = track
        intro_voice_proc = subprocess.Popen(["say", "%s by %s" % (track.title, track.artist)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while True:
            if intro_voice_proc.poll() is not None:
                break
            sleep(0.2)
        self.player_proc = subprocess.Popen(["mpg321", track.filepath], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def play(self):
        if self.is_paused:
            self.unpause()
            return

        self.next()

    def info(self):
        current_track_str = 'Current track: '
        if self.current_track is not None:
            current_track_str += '%s by %s' % (self.current_track.title, self.current_track.artist)
        else:
            current_track_str += '-'
        current_track_str += '\n'
        print current_track_str

    def next(self):
        self.stop()
        track = self.collection.get_next_track()
        self.play_track(track)

    def stop(self):
        if self.player_proc is not None:
            self.player_proc.kill()
            self.current_track = None
            self.is_paused = False

    def unpause(self):
        if self.player_proc is not None and self.is_paused:
            self.player_proc.send_signal(signal.SIGCONT)
            self.is_paused = False

    def pause(self):
        if self.player_proc is not None:
            if not self.is_paused:
                self.player_proc.send_signal(signal.SIGTSTP)
                self.is_paused = True
            else:
                self.player_proc.send_signal(signal.SIGCONT)
                self.is_paused = False


    def random(self):
        track = self.collection.random_track()
        self.play_track(track)
