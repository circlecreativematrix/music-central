
import sys
from unittest.mock import MagicMock
import subprocess
import pytest

class DictObj():
  pass

#@pytest.mark.skip(reason="no way of currently testing this")
import requests
sys.path.append('../')

maml_path = "./data/example_1.yaml"
from Printer import Printer 
from ParseMaml import ParseMaml
import time, yaml
#@pytest.mark.skip(reason="no way of currently testing this")
def test_handle_url():
    printer = Printer()
    result = None
    with open( "./data/gifts_data_out.json") as file:
        result = file.read()
    dictObj = DictObj()
    dictObj.content = result
    dictObj.key = "content"
    requests.request = MagicMock(return_value=dictObj)
    config = printer.load_yaml("./config/config.yaml")
    maml_phrase_item = printer.load_yaml(maml_path)
    nbef = printer.handle_url(config["fornof.gifts.url"],maml_phrase_item['phrases']['phrase.sample2'])
    assert nbef['notes'] != None
#@pytest.mark.skip(reason="no way of currently testing this")
def test_handle_file():
    printer = Printer()
    result = None
    with open( "./data/gifts_data_out.json") as file:
        result = file.read()
    dictObj = DictObj()
    dictObj.content = result
    dictObj.key = "content"
    #subprocess.check_output = MagicMock(return_value=True)
    config = printer.load_yaml("./config/config.yaml")
    maml_phrase_item = printer.load_yaml(maml_path)
    data = printer.load_yaml('./data/maml_out.yaml')
    printer.run_command_return_output_file  = MagicMock(return_value=data)
    nbef = printer.handle_file(config["fornof.mamlsocket"],maml_phrase_item['phrases']['phrase.mamlsocket.1'], 'name')
    print(nbef, 'nbef')
    assert nbef['notes'] != None

#@pytest.mark.skip(reason="no way of currently testing this")
def test_handle_maml_phrases_file():
    parser = ParseMaml("./data/test_parseMaml.yaml")
    parser.fill_vars_with_nbef()
    printer = Printer()
    result = None
    with open( "./data/gifts_data_out.json") as file:
        result = file.read()
    dictObj = DictObj()
    dictObj.content = result
    dictObj.key = "content"
    data = printer.load_yaml('./data/maml_out.yaml')
    printer.run_command_return_output_file  = MagicMock(return_value=data)
    config = printer.load_yaml("./config/config.yaml")

    maml_phrase_item= parser.maml
    nbef = printer.handle_file(config["fornof.mamlsocket"],maml_phrase_item['phrases']['phrase.mamlsocket.1'], 'name')
    assert nbef['notes'] != None

@pytest.mark.skip(reason="slows down tests, but works if unskipped")
def test_live_out_phrases_file():
    parser = ParseMaml("./data/test_output_live_phrases.yaml")
    parser.fill_vars_with_nbef()
    # should hear something in midi channl
    assert True

def test_mid_file_read_to_nbef():
    parser = ParseMaml("./data/test_mid_type.yaml")
    parser.fill_vars_with_nbef()
    mid_nbef = parser.printer.load_yaml("..\\..\\savenbef\\phrase.midi.working.1.yaml")
    assert len(mid_nbef['notes']) > 0 

#@pytest.mark.skip(reason="slows down tests, but works if unskipped")
def test_mid_file_read_to_nbef():
    parser = ParseMaml("./data/test_nbef_flatfile.yaml")
    parser.fill_vars_with_nbef()
    mid_nbef = parser.printer.load_yaml("..\\..\\savenbef\\phrase.nbef.yaml")
    assert len(mid_nbef['notes']) > 0 

#@pytest.mark.slow
def test_combo_phrases():
    parser = ParseMaml("./data/test_combinations1.yaml")
    parser.fill_vars_with_nbef()
    parser.handle_combinations()
    time.sleep(1.1)
    with open( "..\\..\\savenbef\\combo.sample3.yaml", "r") as file:
        mid_nbef =yaml.safe_load(file.read())
       
        assert len(mid_nbef['notes']) > 0

def test_combo_phrases():
    parser = ParseMaml("./data/test_combinations2-multi.yaml")
    parser.fill_vars_with_nbef()
    parser.handle_combinations()
    time.sleep(1.1)
    with open( "..\\..\\savenbef\\combo.sample4.yaml", "r") as file:
        mid_nbef =yaml.safe_load(file.read())
       
        assert len(mid_nbef['notes']) > 0