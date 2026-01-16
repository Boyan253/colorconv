import pytest

import colorconv


def test_parse_six_digit_hex():
    assert colorconv.parse_hex("#3b82f6") == (59, 130, 246)

def test_parse_three_digit_hex_expands():
    assert colorconv.parse_hex("#fff") == (255, 255, 255)
