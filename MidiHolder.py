import mido
import midiutil
from midiutil import *
import re


class MidiHolder:
    def __init__(self, num_tracks=16, tempo=120):
        self.tempo = tempo
        self.track_time = {}
        self.time_to_place_add_tempo = 0
        self.ppq = 960

        self.mid = MIDIFile(
            numTracks=num_tracks,
            removeDuplicates=True,
            deinterleave=False,
            adjust_origin=False,
            file_format=1,
            ticks_per_quarternote=self.ppq,
            eventtime_is_ticks=True)
        #self.track_time[0] = 0
        #self.track_time[1] = 0 
       # self.create_tracks(num_tracks)
        self.create_time_tracks()
        self.mid.addTempo(0, self.time_to_place_add_tempo, self.tempo)
    
    def create_time_tracks(self):
        for i in range(0,len(self.mid.tracks)):
            if not self.track_time.get(i, None):
                self.track_time[i] = 0 
          
    def create_tracks(self, num_tracks):
        i = len(self.mid.tracks)
        while len(self.mid.tracks)  <= num_tracks:
            self.mid.tracks.append(midiutil.MidiFile.MIDITrack(True, False))
            self.add_tempo( self.tempo, i-1, insert_time=0)
            self.mid.numTracks = len(self.mid.tracks)
            
            i+=1
        self.create_time_tracks()

    def add_name(self, track_name, track_number, insert_time=0):
        self.mid.addTrackName(track_number, insert_time, track_name)
    def add_key_signature(self, track_number, insert_time=0, accidentals=0, accidental_type=MAJOR, mode=0):
        self.mid.addKeySignature(track_number,insert_time,accidentals,accidental_type, mode)
        # untested
    def add_tempo(self, tempo, track_number, insert_time=0):
        self.mid.addTempo(track_number, insert_time, tempo)

    def add_text(self, text, track_number, dur_sec=0):
        return
        # this is erroring out,and never really worked
        #dur_ticks =  #int(self.sec_to_ticks(dur_sec, self.tempo))
        if(track_number < 0):
            track_number = 0
        self.mid.addText(track_number, int(dur_sec), text)

    def add_note(self, channel, note_midi, dur_sec, velocity=64, is_chord=False):
        track = channel
        dur_ticks = int(self.sec_to_ticks(dur_sec, self.tempo))
        self.mid.addNote(track, channel, note_midi, self.track_time[channel], dur_ticks, velocity)
        if not is_chord:
            self.track_time[channel] += dur_ticks

    def add_note_on_off(self, channel, midi_type, note_midi, dur_sec, velocity=22):
        # 
        track = channel
        dur_ticks = abs(int(self.sec_to_ticks(dur_sec, self.tempo)))
        # handle rests:
        if note_midi == -1:
            self.track_time[channel] += dur_ticks
            return
        if note_midi == -2:  # rewind by specific time
            self.track_time[channel] -= dur_ticks
            return
        if note_midi == -3:  # set to specific time0
            self.track_time[channel] = dur_ticks
            return
        if note_midi == -4:  # set to specific time0
            raise Exception('-4 midi not implemented yet as a flag.')
            return
        if midi_type == 'note_on':
            # if len(self.mid.tracks) <= channel: # channel : 0 ,1 ,2 
            #     self.create_tracks(channel)
            self.mid.tracks[channel].eventList.append(
                midiutil.MidiFile.NoteOn(channel, note_midi, dur_ticks, self.track_time[channel], velocity))
            self.track_time[channel] += dur_ticks
        elif midi_type == 'note_off':
            self.mid.tracks[track].eventList.append(midiutil.MidiFile.NoteOff(channel, note_midi, dur_ticks, velocity))
        elif midi_type == 'tempo':
            # def __init__(self, tick, tempo, insertion_order=0): # midi = 120
            self.mid.tracks[track].eventList.append(
                midiutil.MidiFile.Tempo(self.track_time[channel], note_midi, 0))  # todo test
        elif midi_type == 'copyright':
            # def __init__(self, tick, notice, insertion_order=0): # midi = "copyright 2023 , robert fornof"
            self.mid.tracks[track].eventList.append(midiutil.MidiFile.Copyright(self.track_time[channel], note_midi, 0))
        elif midi_type == 'text':
            #  def __init__(self, tick, text, insertion_order=0): midi == "Hi mom!"
            self.mid.tracks[track].eventList.append(midiutil.MidiFile.Text(self.track_time[channel], note_midi, 0))
        elif midi_type == 'key_signature':
            # https://midiprog.com/midi-key-signature/
            #   def __init__(self, tick, accidentals, accidental_type, mode,
            # insertion_order=0):
            # midi = [4, 1]
            self.mid.tracks[track].eventList.append(
                midiutil.MidiFile.KeySignature(self.track_time[channel], note_midi[0], note_midi[1], 0))
        elif midi_type == 'program_change':
            # def __init__(self, channel, tick, programNumber,insertion_order=0):
            self.mid.tracks[track].eventList.append(
                midiutil.MidiFile.ProgramChange(channel, self.track_time[channel], note_midi, 0))
        elif midi_type == 'system_exclusive_event':
            # https://www.recordingblogs.com/wiki/midi-system-exclusive-message
            # def __init__(self, tick, manID, payload, insertion_order=0):
            self.mid.tracks[track].eventList.append(
                midiutil.MidiFile.SysExEvent(self.track_time[channel], note_midi[0], note_midi[1], 0))
        elif midi_type == 'universal_system_exclusive_event':
            # def __init__(self, tick, realTime, sysExChannel, code, subcode,payload, insertion_order=0):
            self.mid.tracks[track].MIDIEventList.append(midiutil.MidiFile.UniversalSysExEvent(
                self.track_time[channel], note_midi[0], note_midi[1],note_midi[2], note_midi[3], note_midi[4], 0))
        else:
            raise Exception("midi type not implemented yet for track: " + str(track) + " "+ midi_type )
        # 
    def writeEventMidiStream(self, track):
        previous_event_tick = 0
        for event in track.MIDIEventList:
            track.MIDIdata += event.serialize(previous_event_tick)
        
    def save(self, path):
        m = re.search(r'\.mid', path)
        # tracks = self.mid.tracks.copy()
        # self.mid.tracks = [self.mid.tracks.pop(0), self.mid.tracks.pop(0)]
        # self.mid.numTracks = 2
        # i = 0
        # origin = 10000000
        # for _, val in self.track_time.items():
        #     if(val < origin ):
        #         origin = val
        #     i+=1
      
        # for track in self.mid.tracks:
        #     track.closeTrack()
        #     track.processEventList()
        #     track.MIDIEventList.sort(key=lambda event: (event.tick, event.sec_sort_order, event.insertion_order))
        #     track.adjustTimeAndOrigin(origin, self.mid.adjust_origin)
        #     self.writeEventMidiStream(track)    
        if not m:
            with open(path + "/out.mid", "wb") as output_file:
                
                self.mid.writeFile(output_file)
        else:
            with open(path, "wb") as output_file:
                
                self.mid.writeFile(output_file)

    def sec_to_ticks(self, seconds, tempo):

        seconds_per_tick = (60000 / (tempo * self.mid.ticks_per_quarternote)) / 1000
        return float(seconds) / seconds_per_tick * 1.0
        # mido.second2tick(seconds,ticks_per_beat=480,tempo = tempo)#hardcoded

    def dur_to_ticks(self, dur, tempo):
        return self.sec_to_ticks(self, dur / 1000, tempo)

    def ticks_to_dur(self, ticks, ppq, tempo):
        return mido.tick2second(ticks, ppq, tempo) * 1000

    def set_ticks(self, ticks):
        self.mid.ticks_per_quarternote = ticks
