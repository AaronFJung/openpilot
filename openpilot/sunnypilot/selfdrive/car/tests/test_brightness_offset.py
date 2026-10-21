from types import SimpleNamespace

from openpilot.common.test import OpenpilotTestCase
from openpilot.selfdrive.ui.sunnypilot.ui_state import DeviceSP


def offset(brightness: float, value: int) -> float:
  return DeviceSP.apply_brightness_offset(SimpleNamespace(auto_brightness_offset=value), brightness)


class TestAutoBrightnessOffset(OpenpilotTestCase):
  def test_zero_is_unchanged(self):
    assert offset(30., 0) == 30.
    assert offset(5., 0) == 5.

  def test_shifts(self):
    assert offset(50., 10) == 60.
    assert offset(50., -15) == 35.

  def test_limits(self):
    assert offset(30., -20) == 10.
    assert offset(95., 20) == 100.
