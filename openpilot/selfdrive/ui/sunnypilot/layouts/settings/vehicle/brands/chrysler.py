"""
Copyright (c) 2021-, Haibin Wen, sunnypilot, and a number of other contributors.

This file is part of sunnypilot and is licensed under the MIT License.
See the LICENSE.md file in the root directory for more details.
"""
from openpilot.selfdrive.ui.sunnypilot.layouts.settings.vehicle.brands.base import BrandSettings
from openpilot.selfdrive.ui.ui_state import ui_state
from openpilot.system.ui.lib.multilang import tr
from openpilot.system.ui.sunnypilot.widgets.list_view import toggle_item_sp
from opendbc.sunnypilot.car.chrysler.values_ext import JEEPS


class ChryslerSettings(BrandSettings):
  def __init__(self):
    super().__init__()
    self.is_jeep_brake_hold_platform = False

    self.brake_hold_toggle = toggle_item_sp(tr("Jeep Brake Hold (Alpha)"), "", param="JeepBrakeHold")

    self.items = [self.brake_hold_toggle]

  def brake_hold_disabled_msg(self):
    if not self.is_jeep_brake_hold_platform:
      return tr("This feature is currently not available on this platform.")
    elif not ui_state.is_offroad():
      return tr("Enable \"Always Offroad\" in Device panel, or turn vehicle off to toggle.")
    return ""

  def update_settings(self):
    bundle = ui_state.params.get("CarPlatformBundle")
    if bundle:
      self.is_jeep_brake_hold_platform = bundle.get("platform") in JEEPS
    elif ui_state.CP is not None:
      self.is_jeep_brake_hold_platform = ui_state.CP.carFingerprint in JEEPS

    disabled_msg = self.brake_hold_disabled_msg()
    desc = tr("Hold the brakes after ACC auto-cancels at a standstill and automatically resume when the lead vehicle departs. " +
              "Intended for Jeep models without full stop-and-go support (e.g., 2017 Grand Cherokee). Thanks to jvePilot for this implementation!")

    self.brake_hold_toggle.action_item.set_enabled(self.is_jeep_brake_hold_platform and ui_state.is_offroad())
    self.brake_hold_toggle.set_description(f"<b>{disabled_msg}</b><br><br>{desc}" if disabled_msg else desc)
