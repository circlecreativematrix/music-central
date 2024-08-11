
import sys
from unittest.mock import MagicMock
import subprocess
import pytest

import yaml
#@pytest.mark.skip(reason="no way of currently testing this")
import requests
sys.path.append('../')
import time
from MidiHolder import MidiHolder

def test_track_count():
    midi = MidiHolder( tempo=111)
    midi.add_note_on_off(channel=0,midi_type='note_on',note_midi=60,dur_sec=0,velocity=127)
    midi.add_note_on_off(channel=0,midi_type='note_off',note_midi=60,dur_sec=3.5,velocity=127)
    midi.add_note_on_off(channel=1,midi_type='note_on',note_midi=64,dur_sec=1.5,velocity=127)
    midi.add_note_on_off(channel=1,midi_type='note_off',note_midi=64,dur_sec=4.5,velocity=127)
    midi.add_note_on_off(channel=2,midi_type='note_on',note_midi=69,dur_sec=2.5,velocity=127)
    midi.add_note_on_off(channel=2,midi_type='note_off',note_midi=69,dur_sec=5.5,velocity=127)
    midi.add_note_on_off(channel=3,midi_type='note_on',note_midi=71,dur_sec=5.5,velocity=127)
    midi.add_note_on_off(channel=3,midi_type='note_off',note_midi=71,dur_sec=7.5,velocity=127)

    midi.save("./test_midi_holder.mid")
    assert midi.mid.numTracks == 17

