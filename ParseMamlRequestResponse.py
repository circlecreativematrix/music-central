from ParseMaml import ParseMaml
import yaml
import time
from threading import Thread
from Nicknames import Nicknames
from PrinterRequestResponse import PrinterRequestResponse as Printer 
from Combinations import Combinations
class ParseMamlRequestResponse(ParseMaml):
    '''
     This constructs yaml from maml path, config is hardcoded as I don't see this changing. 
     @ bag holds all the notes in nbef form for each phrase/ combination
    '''
    def __init__(self, maml_path, tmp_path = "/tmp/midiout/"):
        self.printer = Printer(tmp_path)
        self.combinations = Combinations()
        self.nickname = Nicknames()
        if type(maml_path) == type({}):
            self.maml = maml_path
        else: 
            self.maml = self.printer.load_yaml(maml_path)
        self.config= self.printer.load_yaml("./config/config.yaml") # hardcoded, change based on user data? 
        self.bag = {}
       

    def fill_vars_with_nbef(self):

        #port = self.maml['header'].get('output_live_port')
        
        #if port:
        #    self.printer.set_port( port)
        #    self.printer.live.open_port()
     
        for name, phrase in self.maml['phrases'].items(): 
            config_item = self.config[phrase['type']]
            if self.maml.get('nicknames'):
                self.nickname.pre_parse_nicknames(phrase, self.maml, config_item,self.bag,name)
                self.nickname.replace_dollar_with_nicknames(phrase, self.maml, config_item,self.bag,name)
            if config_item['type'] == "url":
               # these might be able to be threaded 
               self.bag[name] =  self.printer.handle_url(config_item, phrase)
            if config_item['type'] == "file":
               self.bag[name] = self.printer.handle_file(config_item, phrase, name)
            if config_item['type'] == 'nbef':
                self.bag[name] = self.printer.handle_nbef_flatfile(phrase)
            # this is just a stint, I actually want query params to determine this or ACCEPT header
            #if phrase.get('output_midi', None):
            return self.printer.handle_output_midi( phrase, self.maml, self.bag, name)
            # this does not include Combinations! so ... put into combinations if working.
            #if phrase.get('output_nbef', None):
            # else:
            #     return self.printer.handle_output_nbef(phrase,self.maml, self.bag, name)
                
        self.printer.play()
        while len(self.printer.tracks_playing) > 0:
                time.sleep(.1)
        self.printer.stop_clean()
         #maml, configs, bag, printer)
        
if __name__ == '__main__':
    parser = ParseMaml("./arrangements/examples/example_1.yaml")
    parser.fill_vars_with_nbef()

