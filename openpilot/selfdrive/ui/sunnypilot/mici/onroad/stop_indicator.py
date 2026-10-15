"""
Planned stop info for the comma four set speed badge (fork feature, param ShowStopIndicator).

The badge that normally pops up "<set speed> MAX" shows "<distance> STOP" instead while the
driving model's planned speed reaches a stop within its 10 second plan. MAX still takes priority
whenever it would normally pop up. Only active while the car is following the model's plan
(experimental mode, and Dynamic Experimental Control in blended mode), so it reflects what the
car will actually do. Display only: reads existing messages, changes nothing in planning or control.
"""
from openpilot.cereal import custom
from openpilot.selfdrive.ui.ui_state import ui_state

DecState = custom.LongitudinalPlanSP.DynamicExperimentalControl.DynamicExperimentalControlState

STOP_SPEED = 1.0  # m/s, planned speed below this counts as a stop
MOVING_SPEED = 0.5  # m/s, below this we are already stopped and holding
METER_TO_FOOT = 3.28084


def planned_stop_distance(velocities, positions, v_ego: float) -> float | None:
  """Distance in meters to the first planned stop, 0 if already stopped and holding, None if no stop is planned."""
  for v, x in zip(velocities, positions, strict=False):
    if v < STOP_SPEED:
      return max(float(x), 0.) if v_ego > MOVING_SPEED else 0.
  return None


def stop_distance_text(distance: float) -> str:
  """Distance in display units (feet or meters) without the unit, like the set speed number."""
  if ui_state.is_metric:
    return str(int(round(distance / 5.) * 5))
  return str(int(round(distance * METER_TO_FOOT / 10.) * 10))


class PlannedStop:
  def _following_model_plan(self) -> bool:
    sm = ui_state.sm
    if not (ui_state.has_longitudinal_control and sm['selfdriveState'].enabled and sm['selfdriveState'].experimentalMode):
      return False
    dec = sm['longitudinalPlanSP'].dec
    return not dec.active or dec.state == DecState.blended

  def update(self) -> float | None:
    """Distance to the planned stop in meters, or None when the badge should not show STOP."""
    if not (ui_state.show_stop_indicator and self._following_model_plan()):
      return None
    model = ui_state.sm['modelV2']
    return planned_stop_distance(model.velocity.x, model.position.x, ui_state.sm['carState'].vEgo)
