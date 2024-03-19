# this is a poc for getting things up and going . 
''' I full expect to refactor this into working config and arrangement file'''
import shutil

from Printer import Printer
from MidiHolder import MidiHolder
from MidiLive import MidiLive
import uuid
import yaml
import time
import requests 
import mido
import mido.backends.rtmidi
import subprocess
import re
import json
from pathlib import Path
import yaml
import os
import shlex
from threading import Thread

from Nicknames import Nicknames
    
class PrinterRequestResponse(Printer):
    def __init__(self, tmp_path = "/tmp/midiout/"):
        super().__init__()
        self.path = tmp_path
        self.final_path = None

    def handle_output_midi(self, phrase, maml, bag, name):
            
           # get header save path 
         
            # get path to save
            track = phrase.get('track', 0)
            midi_save = str(uuid.uuid1()) # this needs to change to a non-user specified uuid
            self.final_path = f'{self.path}{midi_save}.mid'
            # call printer for a readnotes to save 
            # read_notes(self, generated, track = 0, to_live=False, to_file= True, to_nbef= True):
            self.read_notes(bag[name], track,  to_live=False, to_file= True , to_nbef= False)
            self.save(self.final_path)
            
            self.clear()
            


if __name__ == '__main__':
    printer = PrinterRequestResponse()

