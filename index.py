# this is a poc for getting things up and going . 
''' I full expect to refactor this into working config and arrangement file'''
from MidiHolder import MidiHolder
from MidiLive import MidiLive
import yaml
import time
import requests 
import mido
import mido.backends.rtmidi
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
    

    def read_notes(self, generated, track = 0, to_live=False, to_file= True, to_nbef= True):
        nbef_note_output = []
        errors = []
        # todo read header
        # todo : note_type and beat_type should be first class citizens, and at the start of the note, not inner
        # time should be time. 
        start_time = time.time()
       
        for notebeat in generated['notes']:
                print(notebeat['signal'], 'signal')
                type_onoff = notebeat['signal']
                val = None
                try:
                    val = str(notebeat['midi'])
                except Exception as e:
                    errors.append(str([e, notebeat, 'generated']))
                    continue
            
        
            
                time_ms = notebeat['time_ms']/1000
                velocity = notebeat['velocity']
                if to_nbef: 
                    nbef_note_output.append({'midi': int(val), 'velocity': velocity, 'time_ms': time_ms*1000, 'track': track})
                if to_file:
                    self.midi.add_note_on_off(track,type_onoff,int(val), time_ms,velocity) # ischord?
                if to_live:
                    current_time = time.time() - start_time
                    if velocity == 0:
                        type_onoff = 'note_off'
                    print(current_time,'curtime')
                    print(type_onoff, 'type_out')
                    if time_ms-current_time <= 0:
                        print(type_onoff, 'type')
                        self.live.send(track, type_onoff,int(val),100)
                    else:
                        time.sleep(time_ms-current_time)
                        self.live.send(track, type_onoff,int(val),100)
        if to_nbef: 
            return nbef_note_output, errors
        return errors
    def save(self, name='./poc.mid'):
        self.midi.save(name)

if __name__ == '__main__':
    printer = Printer()
    notes =printer.request_notes()
    
    out,err = printer.read_notes(notes,0,to_live=True,to_file=False, to_nbef=True)
    print(out, err)
    #printer.save("poc3.mid")

