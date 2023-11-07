import mido
class MidiLive: 
    def __init__(self):
        self.port = None
        self.output_midi = None
        self.open_once = False
    def open_port(self):
        if self.open_once:
            print('already open')
            return
        self.output_midi =  mido.open_output(self.port)
        self.open_once = True

    def send(self,channel, type_onoff, midi_note,velocity = 65):
      
        if channel < 0:
          channel = 0
        print(channel, type_onoff, midi_note, 'SENDING...' , self.port)
        if self.port == None:
            raise Exception("self.port name not defined in MidiLive, so can't do anything")
        self.open_port() 
        msg =  mido.Message( type=type_onoff, note=midi_note, channel=channel, velocity= velocity)
        self.output_midi.send(msg)
        return 