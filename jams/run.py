# -*- coding: utf-8 -*-
import sys
import os
import time
from watchdog.observers import Observer
from collection import JamCollection, JamFileHandler
from player import JamPlayer
from terminal import Terminal

JAM_DIR = "/Users/phil/Rushmore jams/"

def clear_sreen():
    os.system('clear')

if __name__ == "__main__":
    clear_sreen()
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    observer = Observer()
    collection = JamCollection()
    player = JamPlayer(collection)
    
    valid_filepaths = []
    for dirpath, dirnames, filenames in os.walk(JAM_DIR):
        files_with_paths = [os.path.join(dirpath, filename) for filename in filenames if JamCollection.valid_file_check(filename)]
        if len(files_with_paths) > 0:
            collection.batch_add_tracks(files_with_paths)

    event_handler = JamFileHandler(collection)

    observer.schedule(event_handler, JAM_DIR, recursive=True)
    observer.start()

    term = Terminal(collection, player)
    intro = \
    """
      ___           ___           ___           ___           ___     
     /\  \         /\  \         /\__\         /\  \         /\  \    
    /::\  \        \:\  \       /:/ _/_        \:\  \       |::\  \   
   /:/\:\__\        \:\  \     /:/ /\  \        \:\  \      |:|:\  \  
  /:/ /:/  /    ___  \:\  \   /:/ /::\  \   ___ /::\  \   __|:|\:\  \ 
 /:/_/:/__/___ /\  \  \:\__\ /:/_/:/\:\__\ /\  /:/\:\__\ /::::|_\:\__\\
 \:\/:::::/  / \:\  \ /:/  / \:\/:/ /:/  / \:\/:/  \/__/ \:\~~\  \/__/
  \::/~~/~~~~   \:\  /:/  /   \::/ /:/  /   \::/__/       \:\  \      
   \:\~~\        \:\/:/  /     \/_/:/  /     \:\  \        \:\  \     
    \:\__\        \::/  /        /:/  /       \:\__\        \:\__\    
     \/__/         \/__/         \/__/         \/__/         \/__/    
      ___           ___           ___           ___           ___     
     /\  \         /\  \         /\__\         /\__\         /\  \    
    /::\  \       /::\  \       /:/ _/_       /:/ _/_       |::\  \   
   /:/\:\  \     /:/\:\__\     /:/ /\__\     /:/ /\__\      |:|:\  \  
  /:/  \:\  \   /:/ /:/  /    /:/ /:/ _/_   /:/ /:/  /    __|:|\:\  \ 
 /:/__/ \:\__\ /:/_/:/__/___ /:/_/:/ /\__\ /:/_/:/  /    /::::|_\:\__\\
 \:\  \ /:/  / \:\/:::::/  / \:\/:/ /:/  / \:\/:/  /     \:\~~\  \/__/
  \:\  /:/  /   \::/~~/~~~~   \::/_/:/  /   \::/__/       \:\  \      
   \:\/:/  /     \:\~~\        \:\/:/  /     \:\  \        \:\  \     
    \::/  /       \:\__\        \::/  /       \:\__\        \:\__\    
     \/__/         \/__/         \/__/         \/__/         \/__/ (FM)

    """

    term.cmdloop(intro)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
