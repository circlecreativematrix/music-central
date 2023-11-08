# this is a poc for getting things up and going . 
''' I full expect to refactor this into working config and arrangement file'''
import shutil
from MidiHolder import MidiHolder
from MidiLive import MidiLive
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
class console():
    @staticmethod
    def log( *data):
        print(data)
# load the json from http request using requests 
# iterate over the notes
#   todo first --> output notes to file (done)
#   output notes to live midi (done)
#  (done) nbef needs to be pancaked to a flat key value pairs first.
# (done) also version needs to be at the top 
# (done) type of notes need to be at the top - not in the f'in body of notes
#   (done)goes for note_type, and beat_type
# (done)   output notes to nbef
# yay ! 
# (done) next up , put things into configs - one for urls (handle files later), one for music similar to MamlReader. read in as yaml (done)
# wahoo! 
# todo: bug? - Is the nbef correct for output of one of these things? perhaps a pull down, and a flat_file read from one of these outputs - timing correct? 
# todo : converter: put in a new type of converter for .mid that takes in a mid an outputs a nbef



# need an array of entries maybe? for now , just stealing the notes
class Printer():
    def __init__(self):
    
        track_count = 1
        tempo = 60
        self.midi = MidiHolder(track_count, tempo )
        self.live = MidiLive()
        self.port = None
        self.can_play = False
        self.tracks_playing = []
        #self.maml = self.load_yaml('./arrangements/examples/example_1.yaml') # hardcoded
        # print( self.url_config['fornof.gifts.url'], 'keys')

    def load_yaml(self, path):
        with open(path,'r') as file:
            data = file.read()
            return yaml.safe_load(data)
    def set_port(self, port):
        self.live.port = port
    def get_config_data(self,config_item, maml_phrase_item):
        input_body_key = config_item['input_body_key']
        command_for_body = config_item['command_for_body']
        yamlReplacement =  yaml.dump(maml_phrase_item['input'])
        command_for_body.replace( f'${input_body_key}', yamlReplacement)
        return command_for_body
  

    def handle_url(self, config_item, maml_phrase_item):
        get_data = self.get_config_data(config_item, maml_phrase_item)
        if config_item['input_file_type'] == 'json':
            config_item['headers']['content-type']= "application/json"
        if  config_item['input_file_type'] == 'yaml':
             config_item['headers']['content-type'] = "application/yaml"
        verb = config_item.get("method", "GET")
        result = requests.request(
        verb,
        headers=config_item.get("headers", None),
        url=config_item['url'],
        data= get_data)
        return yaml.safe_load(result.content)

    @DeprecationWarning     
    def request_notes(self):
       
        result = requests.get(self.generator_url)
        # handle errors by failing 
        generated = yaml.safe_load(result.content)
        return generated
    '''
    config_item
  type: file
  input_body_key: notes
  input_body_type: text
  input_file: $PATH\\target\\midi_split.txt # this is what will be populated with string or yaml dumps. 
  input_file_type: text # yaml, json 
  path: "C:\\projects\\music-user-reform\\MamlSocket"
  source_file: None # placeholder for sourcing things like venv and such. 
  call: "java -jar $PATH\\target\\MamlSocket-1.0-SNAPSHOT.jar -i $INPUT_FILE -o '$OUTPUT_FILE'"
  output_file: "c:\\web\\mid\\central_use.yml"

    '''
    def exists_or_add_path(self, input_path, trim_file=True):
        input_path = input_path.replace('\\\\', "\\") # .replace("\\", "/")
        if trim_file:
          
           print('inputfile', input_path)
           no_file = re.search(r'(.*/|.*\\)', input_path)
           input_path = no_file.groups(0)[0]
        if not os.path.exists(input_path):
            os.makedirs(input_path)
        else: 
            print('path exists', input_path)


    def touch_file(self, input_path):
        return Path(input_path).touch()
    
    
    def copy_binary_file(self,source_path, destination_path):
        try:
            shutil.copyfile(source_path, destination_path)
            print("Binary file copied successfully!")
        except FileNotFoundError:
            print("Error: One or both of the file paths are invalid.")

    def write_input_to_input_file(self,input_file,config_item, maml_phrase_item):
        #    self.write_input_to_input_file(input_file, maml_phrase_item['input'], config_item['input_body_type'])
        input_type = config_item['input_body_type']
        input_key = config_item['input_body_key']
        
        
        if input_type == "text":
            input_from_maml = maml_phrase_item['input']
            #print(input_from_maml, 'what is this type? ' ,type(input_from_maml))
            with open(input_file, 'w') as file:
                file.write(input_from_maml)
        elif input_type == "mid":
           input_from_maml = maml_phrase_item[input_key]
           self.copy_binary_file( input_from_maml, input_file)
        elif input_type == "yaml":
            input_from_maml = maml_phrase_item[input_key]
            with open(input_file, 'w') as file:
                file.write(yaml.dump(input_from_maml))
        else:
            raise Exception(f'unhandled input type {input_type}')
        # todo for this is yaml and json types. 
        return
    
    def add_folder_file_if_not_exists(self, input_file):
            self.exists_or_add_path(input_file)
            self.touch_file(input_file)

    def run_command_return_output_file(self, command, output_file):
        nbef_data = None
        cmd = command
        subprocess.run(cmd, shell=True)
        with open(output_file,'r') as file:
            print('reading', output_file)
            nbef_data = file.read()
            return yaml.safe_load(nbef_data)

    def handle_nbef_flatfile(self, phrase):
         with open(phrase['path']) as file: 
              return yaml.safe_load(file.read()) 
         
    def handle_file(self, config_item, maml_phrase_item):
        path = config_item['path'] # does thsi have quotes when replaced/
        output_file = config_item['output_file'].replace("$PATH", path).replace('\\\\', "\\")
        input_file = config_item['input_file'].replace("$PATH", path).replace('\\\\', "\\")
        self.add_folder_file_if_not_exists(output_file)
        self.add_folder_file_if_not_exists(input_file)
        self.write_input_to_input_file(input_file, config_item,maml_phrase_item)
        command = config_item['call'].replace("$PATH", path).replace("$INPUT_FILE", input_file).replace("$OUTPUT_FILE", output_file)
        result = self.run_command_return_output_file( command, output_file)
        return result
    @DeprecationWarning
    def file_run_and_open_notes(self):
        path = "C:\\projects\\music-user-reform\\MamlSocket"
        output_file = "c:\\web\\mid\\central_use.yml"
        command =  f'java -jar {path}\\target\\MamlSocket-1.0-SNAPSHOT.jar -i {path}\\target\\midi_split.txt -o "{output_file}"'
        nbef_data = None

        subprocess.check_output(command)
        with open(output_file,'r') as file:
            nbef_data = file.read()
            return yaml.safe_load(nbef_data)
    

    def handle_live(self, start_time, velocity, time_ms,track, midi_num, type_onoff):
       
        #self.live.open_port()
    
        current_time = time.time() - start_time
        if velocity == 0:
            type_onoff = 'note_off'
        if time_ms-current_time <= 0:
            self.live.send(track, type_onoff,int(midi_num),100)
        else:
            time.sleep(time_ms-current_time)
            self.live.send(track, type_onoff,int(midi_num),100)
            
    def get_note_details(self,generated, notebeat ):
        if generated['note_type'] == "midi":
          
            return { "velocity": notebeat['velocity'], "midi": notebeat['midi'], "track": notebeat.get('track', 0) }
        else:
            raise Exception(f'unsupported note type {generated["note_type"]}')
        
    def get_beat_details(self,generated, notebeat ):
        if generated['beat_type'] == "signal_ms":
            return { "signal": notebeat['signal'], "time_ms": notebeat['time_ms'], }
        if generated['beat_type'] == "signal_tick":
            # todo - revisit ticks_to_dur - 11/4/2023 , it sounds correct? but time_ms is in seconds  ,not ms? yet it works fine
            return { "signal": notebeat['signal'], "time_ms": self.midi.ticks_to_dur( notebeat['time_tick'], generated['midi_ppq']/4,generated['tempo'])}
        else:
            raise Exception(f'unsupported beat type {generated["beat_type"]}')
    def clear(self):
        track_count = 1
        tempo = 60
        self.midi = MidiHolder(track_count, tempo )
        #self.live = MidiLive("IAC_DRIVER b1 2")
    
       
    def format_nbef(self, beat_type, note_type="midi" , tempo = 111 , notes= []):
        return { 'beat_type': beat_type, 
                 'note_type': note_type,
                 'tempo': tempo ,
                 'notes': notes}

    def read_notes(self, generated, track = 0, to_live=False, to_file= True, to_nbef= True):
        nbef_note_output = []
        errors = []
        start_time = time.time()
        
        for notebeat in generated['notes']:
            
            note = self.get_note_details(generated, notebeat)
            beat =  self.get_beat_details(generated, notebeat)
            # each of these can happen in a separate thread. 11/4/23 -todo
            if to_nbef: 
                nbef_note_output.append({'midi': int(note['midi']), 'velocity': note['velocity'], 'time_ms': beat['time_ms']*1000, 'track': note['track']})
            if to_file:
                #add_note_on_off(self, channel, midi_type,note_midi, dur_sec, velocity = 22 )
                self.midi.add_note_on_off(track,beat['signal'],note['midi'], beat['time_ms'],note['velocity']) # ischord?
            if to_live:
                if not self.live.port :
                     self.live.port = self.port
                     self.live.open_port()
                #def handle_live(self, start_time, velocity, time_ms,track, midi_num)
                self.handle_live(start_time, note['velocity'], beat['time_ms'], track  or note['track'], note['midi'], beat['signal'])
                #print('todo-handle live needs a port from CLI or config, preferrably config? or CLI is alright too')
        if to_nbef: 
           return self.format_nbef("time_ms","midi", generated['tempo'] , nbef_note_output), errors
        return None, errors
    def play(self):
        self.can_play = True

    def stop_clean(self):
        #print('begin clean')
        self.can_play = False
        if self.live.output_midi:
            self.live.output_midi.close()
            self.live.open_once = False
        #print('end clean')

    def play_wait_live(self, generated, track = 0 ):
        marker = [True]
        self.tracks_playing.append(marker)
        #self.can_play = True
        while self.can_play == False: 
             start_time = time.time()
             print('waiting...')
             time.sleep(.01)

        for notebeat in generated['notes']:
           
            note = self.get_note_details(generated, notebeat)
            beat =  self.get_beat_details(generated, notebeat)
            print('note', note, 'beat', beat, 'start_time', start_time)
            self.handle_live(start_time,note['velocity'], beat['time_ms'], track-1  or note['track'], note['midi'], beat['signal'] )
        self.tracks_playing.remove(marker)

    def save(self, name='./poc.mid'):
        self.midi.save(name)

    def handle_output_nbef(self,phrase,maml,bag, name):
             
                track = phrase.get('track', 0)
                save_path = maml['header']['save_path']
                nbef_save_path = phrase.get('output_nbef')
                path = save_path + nbef_save_path
               
                if not bag[name]:
                     raise Exception('this bag name is blank for', name)
                nbef, _ = self.read_notes(bag[name], track,  to_live=False, to_file= False , to_nbef= True)
                with open(path,'w+') as file:
                    file.write(yaml.dump(nbef))
                print(f'saved {name} to {path}')

    def handle_output_midi(self, phrase, maml, bag, name):
            
           # get header save path 
            save_path = maml['header']['save_path']
            # get path to save
            track = phrase.get('track', 0)
            midi_save = phrase.get('output_midi')
            path = save_path + midi_save
            # call printer for a readnotes to save 
            # read_notes(self, generated, track = 0, to_live=False, to_file= True, to_nbef= True):
            self.read_notes(bag[name], track,  to_live=False, to_file= True , to_nbef= False)
            self.save(path)
            print(f'saved {name} to {path}')
            self.clear()

    def feature_fun(self, phrase,maml,bag, name):
        if phrase.get('output_live', None):  
            track = phrase.get('track', 0)
            print(bag[name], 'name baggy')
            thread_live = Thread(target=self.play_wait_live, args=[bag[name], track ])
            thread_live.start()

        if phrase.get('output_midi', None):
            thread_midi = Thread(target= self.handle_output_midi, args = [phrase, maml, bag, name])
            thread_midi.start()

        if phrase.get('output_nbef', None):
            thread_nbef = Thread(target= self.handle_output_nbef, args = [phrase,maml, bag, name])
            thread_nbef.start()

    

if __name__ == '__main__':
    printer = Printer()
    #notes =printer.request_notes()
    #out,err = printer.read_notes(notes,0,to_live=True,to_file=False, to_nbef=True)
    #print(out, err)
    #printer.save("poc3.mid")

    notes = printer.file_run_and_open_notes()
    nbef,err = printer.read_notes(notes,0,to_live=False,to_file=True, to_nbef=True)
    #printer.save('maml-thing.mid')
    #print(nbef )
