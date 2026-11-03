from iran_bourse_mcp.text import ascii_digits, clean, match_key


def test_arabic_letters_become_persian():
    assert clean("فولاد مباركه اصفهان") == "فولاد مبارکه اصفهان"
    assert clean("كگل") == "کگل"


def test_clean_handles_none_and_whitespace():
    assert clean(None) is None
    assert clean("  فولاد \n  مبارکه ") == "فولاد مبارکه"


def test_match_key_ignores_script_variants_spaces_and_zwnj():
    assert match_key("كگل") == match_key("کگل")
    assert match_key("می‌نا") == match_key("مینا")
    assert match_key("خودرو ") == match_key("خودرو")


def test_ascii_digits():
    assert ascii_digits("۱۴۰۵/۰۸/۱۲ ٠١٢") == "1405/08/12 012"
