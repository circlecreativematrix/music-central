
import sys
from unittest.mock import MagicMock
import subprocess
import pytest

import yaml
#@pytest.mark.skip(reason="no way of currently testing this")
import requests
sys.path.append('../')
import time
from Printer import Printer 
from Nicknames import Nicknames
#@pytest.mark.skip(reason="no way of currently testing this")

# def test_live_out_phrases_file():
#     parser = ParseMaml("./data/test_output_live_phrases.yaml")
#     parser.fill_vars_with_nbef()
#     # should hear something in midi channl
#     assert True

# def test_combo_phrases():
#     parser = ParseMaml("./data/test_combinations1.yaml")
#     parser.fill_vars_with_nbef()
#     parser.handle_combinations()

# def test_combo_phrases():
#     parser = ParseMaml("./data/test_combinations1.yaml")
#     parser.fill_vars_with_nbef()
#     parser.handle_combinations()
#     time.sleep(.1)
#     with open( "..\\..\\savenbef\\combo.sample3.yaml", "r") as file:
#         mid_nbef =yaml.safe_load(file.read())
       
#         assert len(mid_nbef['notes']) > 0

def test_get_key():
    parser = Nicknames()
    result = parser.get_key("a.b.c", {'a':{'b':{'c':[1]}}}, None)
    #parser.handle_combinations()
    assert result[0] == 1 

def test_pre_parse_nicknames():
    printer = Printer()
    config = printer.load_yaml("./config/config.yaml")
    data = printer.load_yaml('./data/test_nicknames_1.yaml')
    #printer.run_command_return_output_file  = MagicMock(return_value=data)
    
    nick = Nicknames()
    bag = {}
    nick.pre_parse_nicknames(data['phrases']['phrase.note_offset.1'], data, config['fornof.offset'],bag,'phrase.note_offset.1')
    nick.replace_dollar_with_nicknames(data['phrases']['phrase.note_offset.1'], data, config['fornof.offset'], bag, 'phrase.note_offset.1')
    #print(bag, 'bag',data['phrases']['phrase.note_offset.1']['input']['notes'])
    #parser.handle_combinations()
    assert len(bag) > 0 
# def test_note_beats():
#     parser = ParseMaml("./data/test_converter_note_beat.yaml")
#     parser.fill_vars_with_nbef()
#     #parser.handle_combinations()
#     time.sleep(1.1)
#     with open( "..\\..\\savenbef\\phrase.note_beat.working.1.yaml", "r") as file:
#         mid_nbef =yaml.safe_load(file.read())
       
#         assert len(mid_nbef['notes']) > 0