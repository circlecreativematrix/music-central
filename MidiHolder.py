import mido
import midiutil
from midiutil import *
import re
class MidiHolder:
    def __init__(self,num_tracks=1, tempo=120):
        self.tempo = tempo
        self.track_time = []
        time_to_place_add_tempo = 0
        self.ppq = 960
        
        self.mid = MIDIFile(
          numTracks=num_tracks,
          removeDuplicates=True,
          deinterleave=False,
          adjust_origin=False,
          file_format=1,
          ticks_per_quarternote=self.ppq,
          eventtime_is_ticks=True)
        
        for i in range(0,num_tracks):
            self.track_time.append(0)
            self.mid.addTempo(i, time_to_place_add_tempo, tempo)

    def add_name(self,track_name, track_number, insert_time = 0):
        self.mid.addTrackName(track_number, insert_time,track_name )


    def add_tempo(self,tempo, track_number, insert_time = 0):
        self.mid.addTempo(track_number, insert_time,tempo )    


    def add_note(self,channel, note_midi, dur_sec, velocity = 64,is_chord = False ):
        track = channel
        dur_ticks = int(self.sec_to_ticks(dur_sec, self.tempo))
        self.mid.addNote(track, channel, note_midi, self.track_time[channel], dur_ticks, velocity)
        if not is_chord:
            self.track_time[channel] +=  dur_ticks
    
    def add_note_on_off(self, channel, midi_type,note_midi, dur_sec, velocity = 22 ):
        #print(track, channel, midi_type,note_midi, dur_sec, velocity ,'stuff')
        track = channel
        dur_ticks = abs(int(self.sec_to_ticks(dur_sec, self.tempo)))
        if midi_type == 'note_on':
            self.mid.tracks[track].eventList.append(midiutil.MidiFile.NoteOn(channel, note_midi, dur_ticks, self.track_time[channel], velocity))
            self.track_time[0] +=  dur_ticks
        elif midi_type =='note_off':
            self.mid.tracks[track].eventList.append(midiutil.MidiFile.NoteOff(channel,note_midi, dur_ticks, velocity))
        else: 
            raise Exception("no note_on or note_off for track: "+ str(track))
        #print(self.mid.tracks[track].eventList, 'event_list')

    def save(self, path):
        m = re.search(r'\.mid', path)
        if not m:
            with open(path+"/out.mid", "wb") as output_file:
                self.mid.writeFile(output_file)
        else:
            with open(path, "wb") as output_file:
                self.mid.writeFile(output_file)

    
    def sec_to_ticks(self, seconds,tempo):
      
        seconds_per_tick = (60000 / (tempo * self.mid.ticks_per_quarternote))/1000
        return seconds/seconds_per_tick*1.0
        #mido.second2tick(seconds,ticks_per_beat=480,tempo = tempo)#hardcoded

    def dur_to_ticks(self, dur,tempo):
        return self.sec_to_ticks(self, dur/1000,tempo)

    def ticks_to_dur(self, ticks, ppq, tempo):
        return mido.tick2second(ticks,ppq,tempo)*1000

    def set_ticks(self,ticks):
        self.mid.ticks_per_quarternote= ticks