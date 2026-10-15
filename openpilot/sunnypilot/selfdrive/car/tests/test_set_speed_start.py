from openpilot.common.constants import CV
from openpilot.common.test import OpenpilotTestCase
from openpilot.cereal import custom
from opendbc.car.structs import car
from openpilot.selfdrive.car.cruise import VCruiseHelper, V_CRUISE_INITIAL, V_CRUISE_INITIAL_EXPERIMENTAL_MODE, V_CRUISE_MAX
from openpilot.selfdrive.ui.sunnypilot.mici.onroad.stop_indicator import planned_stop_distance


class TestSetSpeedStart(OpenpilotTestCase):
  def setup_method(self):
    self.helper = VCruiseHelper(car.CarParams(pcmCruise=False), custom.CarParamsSP())

  def set_at(self, mph: float, mode: int, metric: bool = False, experimental: bool = True) -> float:
    self.helper.set_speed_start = mode
    self.helper.set_speed_start_metric = metric
    self.helper.initialize_v_cruise(car.CarState(vEgo=mph * CV.MPH_TO_MS), experimental, False)
    return self.helper.v_cruise_kph

  def test_default_keeps_stock_experimental_floor(self):
    assert self.set_at(30, 0) == V_CRUISE_INITIAL_EXPERIMENTAL_MODE

  def test_my_speed(self):
    assert round(self.set_at(30, 1) * CV.KPH_TO_MPH) == 30

  def test_my_speed_plus_offsets_imperial(self):
    assert round(self.set_at(30, 2) * CV.KPH_TO_MPH) == 35
    assert round(self.set_at(30, 3) * CV.KPH_TO_MPH) == 40

  def test_my_speed_plus_offset_metric(self):
    assert self.set_at(50 * CV.KPH_TO_MPH, 2, metric=True) == 55

  def test_clamped(self):
    assert self.set_at(5, 1) == V_CRUISE_INITIAL
    assert self.set_at(100, 3) == V_CRUISE_MAX

  def test_also_applies_outside_experimental(self):
    assert round(self.set_at(45, 2, experimental=False) * CV.KPH_TO_MPH) == 50


class TestPlannedStopDistance:
  def test_no_stop_planned(self):
    assert planned_stop_distance([10., 10., 10.], [0., 10., 20.], 10.) is None

  def test_stop_ahead(self):
    assert planned_stop_distance([10., 5., 0.5, 0.], [0., 30., 45., 46.], 10.) == 45.

  def test_already_stopped_and_holding(self):
    assert planned_stop_distance([0., 0., 0.], [0., 0., 0.], 0.) == 0.
