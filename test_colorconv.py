import pytest

import colorconv


def test_parse_six_digit_hex():
    assert colorconv.parse_hex("#3b82f6") == (59, 130, 246)

def test_parse_three_digit_hex_expands():
    assert colorconv.parse_hex("#fff") == (255, 255, 255)


def test_parse_hex_rejects_junk():
    with pytest.raises(ValueError):
        colorconv.parse_hex("not-a-color")

def test_to_hex_round_trip():
    assert colorconv.to_hex(colorconv.parse_hex("#3b82f6")) == "#3b82f6"


def test_rgb_to_hsl_for_pure_red():
    h, s, l = colorconv.rgb_to_hsl((255, 0, 0))
    assert round(h) == 0 and round(s) == 100 and round(l) == 50

def test_hsl_round_trip():
    rgb = (59, 130, 246)
    assert colorconv.hsl_to_rgb(colorconv.rgb_to_hsl(rgb)) == rgb


def test_parse_accepts_rgb_call():
    assert colorconv.parse("rgb(59, 130, 246)") == (59, 130, 246)

def test_contrast_black_on_white_is_21():
    ratio = colorconv.contrast_ratio((0, 0, 0), (255, 255, 255))
    assert round(ratio, 1) == 21.0


def test_wcag_grades():
    assert colorconv.wcag_grade(21) == "AAA"
    assert colorconv.wcag_grade(4.6) == "AA"
    assert colorconv.wcag_grade(1.2) == "fail"
