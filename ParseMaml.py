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

         
    def handle_output_nbef(self,phrase):
                name = phrase['name']
                track = phrase.get('track', 0)
                save_path = self.maml['header']['save_path']
                nbef_save_path = phrase.get('output_nbef')
                path = save_path + nbef_save_path
                print(self.bag[name], 'fooey')
                if not self.bag[name]:
                     raise Exception('this bag name is blank for', name)
                nbef, _ = self.printer.read_notes(self.bag[name], track,  to_live=False, to_file= False , to_nbef= True)
                with open(path,'w+') as file:
                    file.write(yaml.dump(nbef))
                print(f'saved {name} to {path}')

    def handle_output_midi(self, phrase):
            name = phrase['name']
           # get header save path 
            save_path = self.maml['header']['save_path']
            # get path to save
            track = phrase.get('track', 0)
            midi_save = phrase.get('output_midi')
            path = save_path + midi_save
            # call printer for a readnotes to save 
            # read_notes(self, generated, track = 0, to_live=False, to_file= True, to_nbef= True):
            self.printer.read_notes(self.bag[name], track,  to_live=False, to_file= True , to_nbef= False)
            self.printer.save(path)
            print(f'saved {name} to {path}')
            self.printer.clear()
    def handle_combinations(self):
         self.combinations.handle(self.maml, self.configs, self.bag, self.printer)
    def fill_vars_with_nbef(self):
        # run through each of the phrases< -- do this first 
        # if file , handle based on type key (1 tested and working)
        # if url , handle based on type key (1 tested and working)
        # if any have output_midi or output_nbef , then process and then output. (1 tested and working) 
        # I can put in resulting_notes internally that contain the entire nbef, then handle notes individually (todo)
        # todo : (big lift) - make a program that reads midi and then converts to yaml/nbef? 
        # run through each of the combinations
        # todo - fix \\ to r " \" whenever I get to it (done)
        # todo check directories and add them if they don't exist.  (done)
        port = self.maml['header'].get('output_live_port')
        print(f'outlive opened to {port}')
        if port:
            self.printer.set_port( port)
            self.printer.live.open_port()
        for phrase in self.maml['phrases']: 
            config_item = self.config[phrase['type']]
            name = phrase['name']
            if config_item['type'] == "url":
               # these might be able to be threaded 
               self.bag[name] =  self.printer.handle_url(config_item, phrase)
            if config_item['type'] == "file":
               self.bag[name] = self.printer.handle_file(config_item, phrase)
               print(self.bag[name], 'bag name file')
            if config_item['type'] == 'nbef':
                self.bag[name] = self.printer.handle_nbef_flatfile(phrase)
            if phrase.get('output_live', None):
                
            
                track = phrase.get('track', 0)
               # this needs to be threaded
               
                to_live=True
                to_file = False
                to_nbef = False
                thread_live = Thread(target=self.printer.play_wait_live, args=[self.bag[name], track])
                thread_live.start()
                
            if phrase.get('output_midi', None):
                thread_midi = Thread(target= self.handle_output_midi, args = [phrase])
                thread_midi.start()
            if phrase.get('output_nbef', None):
                print(self.bag[name], 'name bagger')
                thread_nbef = Thread(target= self.handle_output_nbef, args = [phrase])
                thread_nbef.start()
        self.printer.play()
        while len(self.printer.tracks_playing) > 0:
             time.sleep(.1)
        self.printer.stop_clean()
        
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
