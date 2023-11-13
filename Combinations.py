# todo: handle tempo, beat type, and note_type by putting them on the note for combos, that way it can be different and you still get notes ? 
import time
class Combinations():
    def __init__(self):
        pass

    def add_to_bag(self, name, maml, bag, combination_nbef):
        if maml['combinations'].get(name) is None:
            raise Exception('cannot find', name)
        print(name, 'needs a search')
        for item in maml['combinations'][name]['list']:
            to_add= bag.get(item['name'])
            if to_add is None:
                self.add_to_bag(item['name'], maml)
                to_add= bag.get(item['name'])
                if to_add:
                    combination_nbef.append(to_add)
                else:
                    raise Exception('could not find whatever to add to bag', item['name'], name)
            else:
                 combination_nbef.append(to_add)
        return 

    def blob_nbef(self, nbef_array):
        # take array and iterate through
          # combine all the notes 
        # if headers are different raise Exception - to handle /fix later.
        blobbed_output_nbef = {}
        first = True
        key_time = None
        i = 0
        for nbef in nbef_array:
            if first:
                blobbed_output_nbef['tempo'] = nbef['tempo']
                beat_type = nbef['beat_type']
                if beat_type == "signal_tick":
                    blobbed_output_nbef['midi_ppq'] = nbef['midi_ppq']
                    key_time = "time_tick"
                if beat_type == "signal_ms":
                    key_time = "time_ms"
                blobbed_output_nbef['beat_type'] = nbef['beat_type']
                blobbed_output_nbef['note_type'] = nbef['note_type']
                blobbed_output_nbef['notes'] = nbef['notes'].copy()
                first = False
                continue
            if blobbed_output_nbef['note_type'] != nbef['note_type']:
                raise Exception('cannot have different note_types for shared combos, (future case to convert here)')
            if blobbed_output_nbef['beat_type'] != nbef['beat_type']:
                raise Exception('cannot have different beat_types for shared combos, all beats must be same type (future case to convert here)')
       
            last_note_time_offset = blobbed_output_nbef['notes'][-1][key_time]
            # get last note time_ms, 
            # add that time to each note in the next array

            for note in nbef['notes']:
                print(note, "!!", i )
                notecp = note.copy()
                notecp[key_time] += last_note_time_offset
                blobbed_output_nbef['notes'].append(notecp)
                i +=1
        def sort_time(val):
                return val[key_time]
        
        blobbed_output_nbef['notes'].sort(key=sort_time)
        return blobbed_output_nbef
    
    def add_combo_to_bag_key(self, combo, combination_nbef, bag, name):
        for item in combo['list']:
            to_add= bag.get(item['name'])
            if to_add is None:
                raise Exception('cannot find bag name. todo: search and add in', item['name'] )
            #     self.add_to_bag(item['name'], maml, bag, combination_nbef)
            # else:
            combination_nbef.append(to_add) # this works for phrases , not for combos not defined yet. 
        bag[name] = self.blob_nbef(combination_nbef)

    def handle(self, maml, configs, bag, printer):
        self.printer = printer
        port = maml['header'].get('output_live_port')
        print(f'outlive opened to {port}')
        if port:
            self.printer.set_port( port)
            self.printer.live.open_port()
        
        # take combinations and iterate over each one. 
            # if bag.get(name) is not None on this, 
                # skip as it has already been handled
            # iterate over input
                # get nbef from bag[name]
                # if bag[name] isn't found (assume its a combo? )
                #   then call find_and_add_to_bag("name") -  go to name and add it
                #   try one more time, raise error if not found 
            # output_live 
            # output_nbef
            # output_midi

        combination_nbef = []
        for combo in maml['combinations']:
            name = combo['name']
            if bag.get(name) is None:
                self.add_combo_to_bag_key(combo, combination_nbef, bag, name)
            self.printer.after_parse_features(combo, maml, bag, name,port)
        self.printer.play()
        while len(self.printer.tracks_playing) > 0:
            time.sleep(1)
        self.printer.stop_clean()