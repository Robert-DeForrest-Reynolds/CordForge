from unittest.mock import patch
from CordForge import __main__ as main_module


def test_run_normal():
    with patch("CordForge.__main__.Launcher", autospec=True):
        main_module.run()


def test_run_exception():
    with patch("CordForge.__main__.Launcher", side_effect=Exception("boom")):
        main_module.run()
