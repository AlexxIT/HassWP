from hass_win import __main__


def test_utf8():
    from logging import FileHandler
    from logging.handlers import RotatingFileHandler

    assert __main__.AtomicWriter(__file__, overwrite=False)
    assert FileHandler(__file__, 'r', None, False).encoding == "utf-8"
    assert RotatingFileHandler(__file__, 'r').encoding == "utf-8"


def test_validate_os():
    from homeassistant import __main__
    assert __main__.validate_python() is None


def test_timezone():
    from homeassistant.util import dt
    assert dt.get_time_zone("Europe/Moscow")
