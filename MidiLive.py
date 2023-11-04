import mido
class MidiLive: 
    def __init__(self,port_name):
        self.port = mido.open_output(port_name) or None
        if not self.port:
            print('hey dude, your port needs a name to send, have you tried listing midi ports?')
    def send(self,channel, type_onoff, midi_note,velocity = 65):
        if not self.port:
            raise Exception("self.port name not defined in MidiLive, so can't do anything")
        msg =  mido.Message( type=type_onoff, note=midi_note, channel=channel, velocity= velocity)
        self.port.send(msg)
        return 