
import sys
from unittest.mock import MagicMock
import subprocess
import pytest

import yaml
#@pytest.mark.skip(reason="no way of currently testing this")
import requests
sys.path.append('../')
import time
maml_path = "./data/example_1.yaml"
from Printer import Printer 
from ParseMaml import ParseMaml
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

def test_combo_phrases():
    parser = ParseMaml("./data/test_converter_offset.yaml")
    parser.fill_vars_with_nbef()
    #parser.handle_combinations()
    time.sleep(1.1)
    with open( "..\\..\\savenbef\\phrase.note_beat.working.1.yaml", "r") as file:
        mid_nbef =yaml.safe_load(file.read())
       
        assert len(mid_nbef['notes']) > 0

# def test_note_beats():
#     parser = ParseMaml("./data/test_converter_note_beat.yaml")
#     parser.fill_vars_with_nbef()
#     #parser.handle_combinations()
#     time.sleep(1.1)
#     with open( "..\\..\\savenbef\\phrase.note_beat.working.1.yaml", "r") as file:
#         mid_nbef =yaml.safe_load(file.read())
       
#         assert len(mid_nbef['notes']) > 0