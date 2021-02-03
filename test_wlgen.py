import pytest

import wlgen

ALPHABET = "12345"


class TestNextChar:
    def test_next_char(self):
        assert wlgen.next_char("1", ALPHABET) == "2"

    def test_next_char_is_last(self):
        with pytest.raises(wlgen.LastCharException):
            wlgen.next_char("5", ALPHABET)


class TestNext:
    def test_next_for_empty(self):
        assert wlgen.next("", ALPHABET) == "1"
        
    def test_next_not_inc(self):
        assert wlgen.next("23", ALPHABET) == "24"

    def test_next_inc(self):
        assert wlgen.next("25", ALPHABET) == "31"
        assert wlgen.next("55", ALPHABET) == "111"
