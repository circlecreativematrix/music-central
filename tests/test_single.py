
import sys
from unittest.mock import MagicMock
import subprocess
import pytest


#@pytest.mark.skip(reason="no way of currently testing this")
import requests
sys.path.append('../')

maml_path = "./data/example_1.yaml"
from Printer import Printer 
from ParseMaml import ParseMaml
#@pytest.mark.skip(reason="no way of currently testing this")

# def test_live_out_phrases_file():
#     parser = ParseMaml("./data/test_output_live_phrases.yaml")
#     parser.fill_vars_with_nbef()
#     # should hear something in midi channl
#     assert True

def test_combo_phrases():
    parser = ParseMaml("./data/test_combinations1.yaml")
    parser.fill_vars_with_nbef()
    parser.handle_combinations()