import yaml
import time
from threading import Thread
from Printer import Printer 
from Combinations import Combinations
        
class ParseMaml:
    '''
     This constructs yaml from maml path, config is hardcoded as I don't see this changing. 
     @ bag holds all the notes in nbef form for each phrase/ combination
    '''
    def __init__(self, maml_path):
        self.printer = Printer()
        self.combinations = Combinations()
        self.maml = self.printer.load_yaml(maml_path)
        self.config= self.printer.load_yaml("./config/config.yaml") # hardcoded
        self.bag = {}

         

    def handle_combinations(self):
         self.combinations.handle(self.maml, self.config, self.bag, self.printer)
    def fill_vars_with_nbef(self):
        # run through each of the phrases< -- do this first 
        # if file , handle based on type key (1 tested and working)
        # if url , handle based on type key (1 tested and working)
        # if any have output_midi or output_nbef , then process and then output. (1 tested and working) 
        # I can put in resulting_notes internally that contain the entire nbef, then handle notes individually (todo)
        # (done) todo : (big lift) - make a program that reads midi and then converts to yaml/nbef? 
        # run through each of the combinations
        # todo - fix \\ to r " \" whenever I get to it (done)
        # todo check directories and add them if they don't exist.  (done)
        port = self.maml['header'].get('output_live_port')
        print(f'outlive opened to {port}')
        if port:
            self.printer.set_port( port)
            self.printer.live.open_port()
        else: 
            raise Exception('header section needs to have something for port, for example: output_live_port: "IAC_DRIVER b1 2"')
        for name, phrase in self.maml['phrases'].items(): 
            config_item = self.config[phrase['type']]
     
            if config_item['type'] == "url":
               # these might be able to be threaded 
               self.bag[name] =  self.printer.handle_url(config_item, phrase)
            if config_item['type'] == "file":
               self.bag[name] = self.printer.handle_file(config_item, phrase)
            if config_item['type'] == 'nbef':
                self.bag[name] = self.printer.handle_nbef_flatfile(phrase)
            self.printer.feature_fun(phrase, self.maml, self.bag, name)
        self.printer.play()
        while len(self.printer.tracks_playing) > 0:
                time.sleep(1)
        self.printer.stop_clean()
         #maml, configs, bag, printer)
        
if __name__ == '__main__':
    parser = ParseMaml("./arrangements/examples/example_1.yaml")
    parser.fill_vars_with_nbef()
    #notes =printer.request_notes()
    #out,err = printer.read_notes(notes,0,to_live=True,to_file=False, to_nbef=True)
    #print(out, err)
    #printer.save("poc3.mid")

    # notes = printer.file_run_and_open_notes()
    # nbef,err = printer.read_notes(notes,0,to_live=False,to_file=True, to_nbef=True)
    #printer.save('maml-thing.mid')
    #print(nbef )
