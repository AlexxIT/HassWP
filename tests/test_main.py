from hass_win import __main__


def test_utf8():
    from logging import FileHandler
    from logging.handlers import RotatingFileHandler
    # noinspection PyPackageRequirements
    from atomicwrites import AtomicWriter

    assert AtomicWriter(__file__, overwrite=False)
    assert FileHandler(__file__, 'r', None, False).encoding == "utf-8"
    assert RotatingFileHandler(__file__, 'r').encoding == "utf-8"


def test_validate_os():
    from homeassistant import __main__
    assert __main__.validate_python() is None


def test_timezone():
    from homeassistant.util import dt
    assert dt.get_time_zone("Europe/Moscow")


def test_av():
    if __main__.ARCH == "32":
        return
    # noinspection PyPackageRequirements
    from av import __version__
    assert __version__


def test_turbojpeg():
    __main__.fix_requirements(["PyTurboJPEG==1.6.3"])
    # noinspection PyPackageRequirements
    from turbojpeg import TurboJPEG
    assert TurboJPEG()


def test_pyserial():
    __main__.fix_requirements(["pyserial==3.5"])
    # noinspection PyPackageRequirements
    import serial
    assert serial.serial_for_url("socket://", do_not_open=True).out_waiting


def test_dummy():
    __main__.fix_requirements(["dummy"])
