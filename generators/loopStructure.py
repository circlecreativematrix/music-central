import re
import math
class Constants:
    def __init__(self):
        self.notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        self.notes_sharps = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        self.notes_flats =  ['C', 'D@', 'D', 'E@', 'E', 'F', 'G@', 'G', 'A@', 'A', 'B@', 'B']
        self.major_mask =   [ 1,     0,  1,    0,   1,   1,    0,   1,   0,    1,   0,   1  ]
        self.minor_mask =   [ 1,     0,  1,    1,   0,   1,    0,   1,   1,    0,   1,   0  ]
class LoopSah:
    def main(self):
        out = looper.loop_sah("F3", "E5")
        out += looper.loop_sah("E5", "F3")
        print("\n".join(out))
    def __init__(self):
        self.constants = Constants()
        self.notes = self.mask(self.constants.notes_sharps, self.constants.major_mask, "C")
        print(self.notes, 'notes')
    def mask(self, notes, mask, start_note = "C"):
        result = []
        start_index = notes.index(start_note)
        for i in range(0,len(notes)):
            if(mask[i] == 0):
                continue
            else:
                result.append(notes[(i+start_index )%len(notes)])
        return result   
    
    def condition(self, note, start,end, num, incrementing):
        added_num = -1
        if incrementing:
            added_num = 1
        if(num == end[1]):
            if(note == self.notes[(end[0]+added_num)%len(self.notes)]):
                return False
            
        return True
    # takes in inputs like C4 , no sharps or flats in this puppy
    def loop_sah(self,in_begin, in_end):
        # ignore sharps and flats
        in_octave_begin = re.search(r'(\d+)', in_begin)
        in_octave_end = re.search(r'(\d+)', in_end) 
        if in_octave_end:
            in_octave_end = in_octave_end.group(0)
        if in_octave_begin:
            in_octave_begin = in_octave_begin.group(0)
        print(in_octave_begin, 'in_accidental', 'in_begin', in_begin, 'in_end', in_end)
        
        in_begin_no_octave = re.sub(r"\d+","",in_begin)
        in_end_no_octave = re.sub(r"\d+","",in_end)
        
        result = []
        start = [self.notes.index(in_begin_no_octave),int(in_octave_begin)]
        end = [self.notes.index(in_end_no_octave), int(in_octave_end)]
        if start[1] < end[1]:
            incrementing = True
        elif start[1] == end[1] and start[0] < end[0]:
            incrementing = True
        else:
            incrementing = False
        print(end)
        note = self.notes[start[0]]
        num = start[1]
        while self.condition(note,start,end, num,incrementing):
            
            #print(f"!{note}{num} $sah")
            
            if incrementing:
                if(note == "C"):
                    num +=1
                result.append(f"key_note:{note}{num}")
                result.append(f"note:-1,dur:0,vol:0")
                result.append(f"$sah")
                note = self.notes[(self.notes.index(note)+1)%len(self.notes)]
            else:
                if(note == "B"):
                    num -=1
                result.append(f"key_note:{note}{num}")
                result.append(f"note:-1,dur:0,vol:0")
                result.append(f"$sah")
                note = self.notes[(self.notes.index(note)-1)%len(self.notes)]
           
        return result
    

looper = LoopSah()
looper.main()