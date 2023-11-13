import re


class Nicknames():
    def __init__(self):
        pass
    def get_key(self, search, dictionary, default = None):
        splitter = search.split(".")
        return self.get_key_rec(splitter, dictionary, default)
    def get_key_rec(self, search, dictionary, default = None):
        if len(search) == 0:
           return dictionary
       
        i = 0 
        for key, value in dictionary.items():
            #
            if len(search) < 0:
                return default
            if key == search[i]:
                if type(value) == type({}):
                    #
                    return self.get_key_rec(search[1:], value, default)
                else:
                    return value
    def pre_parse_nicknames(self, phrase, maml, config_item, bag, name):
        # load names from nicknames 
        # if nickname exists ,check bag for it, if not found raise exception 
        for name, nickname_val  in maml['nicknames'].items():
            if name == "notes" or name == "beats" or name == "scales":
                for nickname in nickname_val: 
                    val = nickname['value']
                    # re search for dollar signs with a word replace with bag value
                    if(type (val) == type({})):
                        bag[nickname['name']] = nickname['value']
                        continue # we don't do replacements this for dicts
                    replacements = re.findall(r'\$([a-zA-Z0-9_\.]+)', str(val))
                    for replacement in replacements:
                        if replacement in bag:
                            nickname['value'] =  nickname['value'].replace(f'${replacement}', bag[replacement])
                        else:
                            raise Exception(f'nickname {replacement} not found in bag, try adding it to an item above this one')
                        
                    bag[nickname['name']] = nickname['value']
                    
       
        # load nicknames into bag now that all dollars are replaced
    
       # 
       
    
    def replace_dollar_with_nicknames(self, phrase, maml, config_item, bag, name):
        notes = None
        notes = []
        # replace dollar signs with nicknames
        if config_item["input_body_key"] == 'notes':
            notes.append(phrase['notes'])
        elif self.get_key(f'{config_item["input_body_key"]}.notes', phrase):
            notes.append(self.get_key(f'{config_item["input_body_key"]}.notes', phrase))
        else: 
            raise Exception(f'input_body_key {config_item["input_body_key"]} not found in phrase {name}')
        i = 0 
        for note_str in notes[0]:
            replacements = re.findall(r'\$([a-zA-Z0-9_\.]+)', note_str)
            
            for replacement in replacements:
                if replacement in bag:
                    notes[0][i] =  note_str.replace(f'${replacement}', bag[replacement])
                    
                else:
                    raise Exception(f'nickname {replacement} not found in bag, try adding it to an item above this one')
            i +=1
        return
        return phrase
   
    def handle_beat_nicknames(self, phrase):
        if 'beat_nicknames' in phrase:
            for nickname in phrase['beat_nicknames']:
                phrase['notes'] = phrase['notes'].replace(nickname, phrase['beat_nicknames'][nickname])
        return phrase
   
