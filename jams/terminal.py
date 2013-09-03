from cmd import Cmd
from datetime import datetime


class Terminal(Cmd):

    prompt = 'Jams> '
    def __init__(self, collection, player, *args, **kwargs):
        self.player = player
        self.startup_time = datetime.now()
        self.collection = collection     
        Cmd.__init__(self, *args, **kwargs)

    def do_next(self, e):
        """
        Change to next track
        """
        self.player.next()

    def do_play(self, e):
        """
        Start playing a track
        """
        self.player.play()

    def do_stop(self, e):
        """
        Stop playing the track
        """
        self.player.stop()

    def do_playing(self, e):
        """
        Display information about now playing track
        """
        self.player.info()

    def do_random(self, e):
        """
        Start playing a random track
        """
        self.player.random()

    def do_stats(self, e):
        """
        Start playing a random track
        """
        print 'Started: %s' % self.startup_time
        self.collection.stats()

    def do_pause(self, e):
        """
        Pause play process
        """
        self.player.pause()

    def do_exit(self, e):
        """
        This exits the cmdloop
        """
        return True
