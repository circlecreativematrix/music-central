# this is a poc for getting things up and going . 
''' I full expect to refactor this into working config and arrangement file'''
from MidiHolder import MidiHolder
from MidiLive import MidiLive
import yaml
import time
import requests 
import mido
import mido.backends.rtmidi
import subprocess
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
# next up , put things into configs - one for urls (handle files later), one for music similar to MamlReader. read in as yaml




# need an array of entries maybe? for now , just stealing the notes
class Printer():
    def __init__(self):
        self.generator_url = "http://localhost:3000/"
        track_count = 1
        tempo = 60
        self.midi = MidiHolder(track_count, tempo )
        self.live = MidiLive("IAC_DRIVER b1 2")
    def request_notes(self):
        result = requests.get(self.generator_url)
        # handle errors by failing 
        generated = yaml.safe_load(result.content)
        return generated
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
            return { "velocity": notebeat['velocity'], "midi": int(notebeat['midi']), "track": notebeat.get('track', 0) }
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
                #def handle_live(self, start_time, velocity, time_ms,track, midi_num)
                self.handle_live(start_time, note['velocity'], beat['time_ms'], note['track'], note['midi'], beat['signal'])
        if to_nbef: 
            return nbef_note_output, errors
        return None, errors
    

    
    def save(self, name='./poc.mid'):
        self.midi.save(name)

if __name__ == '__main__':
    printer = Printer()
    #notes =printer.request_notes()
    #out,err = printer.read_notes(notes,0,to_live=True,to_file=False, to_nbef=True)
    #print(out, err)
    #printer.save("poc3.mid")

    notes = printer.file_run_and_open_notes()
    nbef,err = printer.read_notes(notes,0,to_live=True,to_file=True, to_nbef=True)
    printer.save('maml-thing.mid')
    print(nbef )
