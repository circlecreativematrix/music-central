
import sys
from unittest.mock import MagicMock

sys.path.append('../')
import time
maml_path = "./data/example_1.yaml"
from Printer import Printer 
from ParseMaml import ParseMaml

def test_perform_notes():
    
    #print(mido.get_output_names())
    config = "./config/config.yaml"
    #parser = ParseMaml('C:\\projects\\music-user-reform\\converter-standard-note\\maml_test.yml')
    maml_path = "/mnt/c/projects/music-user-reform/converter-standard-note/maml_test.yml"
    parser = ParseMaml(maml_path, config )
    #(r"C:\projects\music-user-reform\converter-midi-offset-note\aladdin_new_world.maml.yml" )
    #
    parser.fill_vars_with_nbef()
    parser.handle_combinations()
    print('stuff')
    time.sleep(1.1)
    # with open( "..\\..\\savenbef\\test_single.yaml", "r") as file:
    #     mid_nbef =yaml.safe_load(file.read())
       
    #     assert len(mid_nbef['notes']) > 0