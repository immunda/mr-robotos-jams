from cmd import Cmd


class Terminal(Cmd):

    def __init__(self, collection, *args, **kwargs):
        self.collection = collection
        Cmd.__init__(self, *args, **kwargs)

    def preloop(self):
        print "we are in the preloop function" # this will be called before terminal.cmdloop() begins

    def postloop(self):
        print "we are in the postloop function" # this will be called when terminal.cmdloop() exits

    def do_next(self, e):
        """
        Change to next track
        """
        self.collection.next()

    def do_exit(self, e):
        """
        This exits the cmdloop
        """
        return True
