import pytest
from tests.util import analyze_yaml

GOOD_CODES = [
"""
- alias: Startup PrusaConnect LXC When Printers Turn On
  id: '3d_printer_startup_prusaconnect_lxc_when_printers_turn_on'

  triggers:
    - trigger: state
      entity_id: switch.prusa_mk4s
      to: 'on'
      for:
        hours: 0
        minutes: 1
        seconds: 0
    - trigger: state
      entity_id: switch.prusa_mk4s_mmu3
      to: 'on'
      for:
        hours: 0
        minutes: 1
        seconds: 0

  conditions:
    - condition: state
      entity_id: binary_sensor.lxc_prusaconnect_cam_108_status
      state: 'off'

  actions:
    - action: button.press
      target:
        entity_id: button.lxc_prusaconnect_cam_108_start
""",
"""
alias: Good D15
trigger:
  - platform: state
    entity_id: sensor.x
    to: "on"
action:
  - wait_template: "{{ states('sensor.x') }}"
    timeout: "00:01:00"
""",
    """
alias: wait_template_no_timer
trigger:
  - platform: state
    entity_id: sensor.dryer
    to: "running"

action:
  - wait_template: "{{ is_state('fan.bathroom', 'off') }}"
""",
"""
- alias: Shutdown PrusaConnect LXC When MK4S Turns Off
  id: '3d_printer_shutdown_prusaconnect_lxc_when_mk4s_turns_off'

  triggers:
    - trigger: state
      entity_id: switch.prusa_mk4s
      to: 'off'
      for:
        hours: 0
        minutes: 5
        seconds: 0

  conditions:
    - condition: state
      entity_id: binary_sensor.lxc_prusaconnect_cam_108_status
      state: 'on'
    - condition: state
      entity_id: switch.prusa_mk4s
      state: 'off'
    - condition: state
      entity_id: switch.prusa_mk4s_mmu3
      state: 'off'

  actions:
    - action: button.press
      target:
        entity_id: button.lxc_prusaconnect_cam_108_shutdown
""",
"""
- alias: 3D-Printer - Prusa MK4S Print Stopped
  id: '3d_printer_prusa_mk4s_print_stopped'

  triggers:
    - trigger: state
      entity_id: sensor.prusa_mk4s
      from: 'printing'
      to: 'stopped'

  conditions:
    - condition: state
      entity_id: input_boolean.disable_notifications
      state: 'off'
    - condition: not
      conditions:
      - condition: state
        entity_id: sensor.prusa_mk4s
        state: 'printing'

  actions:
    - action: light.turn_on
      target:
        entity_id:
          - light.prusa_mk4s
      data:
        brightness_pct: 100
        color_name: "purple"
    - action: notify.USER1_devices
      data:
        message: Print Stopped (MK4S)
        data:
          tag: prusa_mk4s
          entity_id: camera.prusa_mk4s
""",
"""
- alias: Alarm - Triggered Armed Away
  id: 'alarm_triggered_armed_away'

  triggers:
    - trigger: state
      entity_id: alarm_control_panel.alarm
      to: 'triggered'

  conditions:
    - condition: not
      conditions:
      - condition: state
        entity_id: group.household
        state: 'home'
    - condition: state
      entity_id: input_boolean.guest_mode
      state: 'off'
    - condition: not
      conditions:
      - condition: state
        entity_id: input_boolean.home_showing_mode
        state: 'on'

  actions:
    - action: light.turn_on
      target:
        entity_id:
          - light.smart_bulbs
      data:
       brightness_pct: 100
       color_name: "red"
    - action: light.turn_on
      target:
        entity_id:
          - light.smart_bulbs_exterior
      data:
       brightness_pct: 100
    - action: light.turn_on
      target:
        entity_id:
          - light.lutron_lights
      data:
       brightness_pct: 100
    - action: light.turn_on
      target:
        entity_id:
          - light.lutron_lights_exterior
      data:
       brightness_pct: 100
    - action: light.turn_on
      target:
        entity_id:
          - light.smart_bulbs
      data:
       flash: long
    - action: switch.turn_on
      target:
        entity_id:
          - switch.siren
    - action: media_player.play_media
      target:
        entity_id: 
          - media_player.sonos_living_room
          - media_player.sonos_dining_room
          - media_player.sonos_kitchen
          - media_player.sonos_bathroom
          - media_player.sonos_bedroom
          - media_player.sonos_bedroom_closet
          - media_player.sonos_USER1s_office
          - media_player.sonos_USER2s_office
          - media_player.sonos_move
          - media_player.sonos_fitness_room
          - media_player.sonos_craft_room
      data:
        announce: true
        media_content_id: >
          media-source://tts/cloud?message="You are not Authorized to be Here. Law Enforcement Has Been Notified!"
        media_content_type: "music"
        extra:
          volume: 90
    - action: notify.USER1_devices
      data:
        message: Alarm Triggered!
        data:
          push:
            sound:
              name: default
              critical: 1
              volume: 1.0
          tag: alarm
          entity_id:
           - camera.front_porch
          actions:
            - action: "disarm_alarm"
              title: "Disable Alarm System"
              destructive: true
              activationMode: background
            - action: "siren_off"
              title: "Siren Off"
              activationMode: background
    - action: notify.USER2_devices
      data:
        message: Alarm Triggered!
        data:
          push:
            sound:
              name: default
              critical: 1
              volume: 1.0
          tag: alarm
          entity_id:
           - camera.front_porch
          actions:
            - action: "disarm_alarm"
              title: "Disable Alarm System"
              destructive: true
              activationMode: background
            - action: "siren_off"
              title: "Siren Off"
              activationMode: background
""",
"""
- alias: Bedtime - Thermostat
  id: 'bedtime_thermostat'

  triggers:
    - trigger: state
      entity_id: input_boolean.bedtime
      to: 'on'
      for:
        hours: 0
        minutes: 4
        seconds: 0

  conditions:
    - condition: state
      entity_id: input_boolean.overnight_guest_mode
      state: 'off'
    - condition: state
      entity_id: input_boolean.thermostat_away
      state: 'off'
    - condition: time
      after: '17:00:00'
      before: '23:00:00'

  actions:
    - action: climate.set_preset_mode
      data:
        entity_id: climate.main_floor
        preset_mode: 'sleep'
""",
"""
- alias: Blinds - USER1's Office Blinds When Motion Detected
  id: 'blinds_USER1_office_blinds_when_motion_detected'

  triggers:
    - trigger: state
      entity_id: binary_sensor.USER1s_office_motion
      from: 'off'
      to: 'on'

  conditions:
    - condition: state
      entity_id: input_boolean.disable_blinds
      state: 'off'
    - condition: state
      entity_id: person.USER1
      state: 'home'
    - condition: state
      entity_id: sun.sun
      state: 'above_horizon'
    - condition: time
      after: '08:00:00'
    - condition: numeric_state
      entity_id: sensor.REDACTED_temperature
      below: 85
    - condition: numeric_state
      entity_id: sensor.REDACTED_temperature
      above: 20
    - condition: numeric_state
      entity_id: sensor.REDACTED_forecasted_temperature_high
      below: 90
    - condition: numeric_state
      entity_id: sensor.REDACTED_forecasted_temperature_high
      above: 20
    - condition: or
      conditions:
      - condition: state
        entity_id: cover.USER1_s_office_blinds
        state: 'closed'
      - condition: state
        entity_id: input_boolean.USER1_office_portable_ac
        state: 'on'
    - condition: sun
      after: sunrise
      after_offset: "00:60:00"
      before: sunset
      before_offset: "-00:45:00"
    - condition: not
      conditions:
      - condition: state
        entity_id: vacuum.upstairs_roomba
        state: 'cleaning'
      - condition: state
        entity_id: vacuum.upstairs_roomba
        state: 'returning'
    - condition: state
      entity_id: input_boolean.USER1_office_guest
      state: 'off'

  actions:
    - action: cover.open_cover
      data:
        entity_id: 
          - cover.USER1_s_office_blinds
""",
"""
- alias: Bug Zapper - Turn Off Bug Zapper at Sunrise
  id: 'bug_zapper_turn_off_bug_zapper_at_sunrise'

  triggers:
    - trigger: sun
      event: 'sunrise'
      offset: '+00:15:00'

  conditions:
    - condition: state
      entity_id: switch.bug_zapper
      state: 'on'

  actions:
    - action: switch.turn_off
      target:
        entity_id:
          - switch.bug_zapper
""",
"""
- alias: Camera - Turn On Front Porch Lights when Motion Detected
  id: 'camera_turn_on_front_porch_lights_when_motion_detected'

  triggers:
    - trigger: state
      entity_id: binary_sensor.front_door_camera_person_detected
      from: 'off'
      to: 'on'
    - trigger: state
      entity_id: binary_sensor.front_porch_person_detected
      from: 'off'
      to: 'on'
    - trigger: state
      entity_id: binary_sensor.front_yard_camera_person_detected
      from: 'off'
      to: 'on'

  conditions:
    - condition: state
      entity_id: sun.sun
      state: 'below_horizon'
    - condition: state
      entity_id: input_boolean.disable_doorbell
      state: 'off'

  actions:
    - action: light.turn_on
      target:
        entity_id:
          - light.front_porch
      data:
        brightness_pct: 100
""",
"""
- alias: Christmas - Turn on Christmas Lights when Home

  trigger:
    - platform: state
      entity_id: group.household
      from: 'not_home'
      to: 'home'

  condition:
    - condition: state
      entity_id: input_boolean.disable_home_away
      state: 'off'
    - condition: state
      entity_id: sun.sun
      state: 'below_horizon'
    - condition: state
      entity_id: switch.exterior_christmas_lights
      state: 'off'
    - condition: or
      conditions:
        - condition: state
          entity_id: input_select.holiday
          state: 'Christmas'
        - condition: state
          entity_id: sensor.holidays_calendar
          state: "New Year's Eve"
    - condition: or
      conditions:
        - condition: state
          entity_id: input_boolean.USER1_away
          state: 'on'
        - condition: state
          entity_id: input_boolean.USER2_away
          state: 'on'

  action:
    - service: switch.turn_on
      entity_id:
        - switch.exterior_christmas_lights
""",
"""
- alias: Laundry - Washing Machine Done USER2 iOS Notification
  id: 'laundry_washing_machine_done_USER2_ios_notification'

  triggers:
    - trigger: state
      entity_id: binary_sensor.washer_wash_completed
      from: 'off'
      to: 'on'
      for:
        hours: 0
        minutes: 0
        seconds: 1

  conditions:
    - condition: state
      entity_id: group.household
      state: 'home'
    - condition: state
      entity_id: person.USER2
      state: 'home'
    - condition: state
      entity_id: input_boolean.disable_notifications
      state: 'off'

  actions:
    - action: notify.USER2_devices
      data:
        message: Washing Machine Finished
        data:
          tag: washer
""",
"""
- alias: Lights - Reset Exterior Garage Light Brightness when Garage Closed
  id: 'lights_reset_exterior_garage_light_brightness_when_garage_closed'

  triggers:
    - trigger: state
      entity_id: cover.garage_door
      to: 'closed'
      for:
        hours: 0
        minutes: 5
        seconds: 0

  conditions:
    - condition: state
      entity_id: input_boolean.disable_door_open_lights_on
      state: 'off'
    - condition: state
      entity_id: sun.sun
      state: 'below_horizon'
    - condition: state
      entity_id: light.garage_light
      state: 'on'

  actions:
    - action: light.turn_on
      target:
        entity_id:
          - light.garage_light
      data:
       brightness_pct: 2
       transition: 330
""",
"""
- alias: Lights - Turn Off Back Door Lights at Midnight Weekdays Friends Visiting
  id: 'lights_turn_off_back_door_lights_at_midnight_weekdays_friends_visiting'

  triggers:
    - trigger: time
      at: '00:00:00'

  conditions:
    - condition: state
      entity_id: sun.sun
      state: 'below_horizon'
    - condition: state
      entity_id: input_boolean.disable_exterior_off_night
      state: 'off'
    - condition: state
      entity_id: input_boolean.guest_mode
      state: 'on'
    - condition: time
      weekday:
        - mon
        - tue
        - wed
        - thu

  actions:
   - action: light.turn_off
     target:
      entity_id:
       - light.back_door
   - delay: '00:00:30'
   - action: light.turn_off
     target:
      entity_id:
       - light.back_door
""",
"""
- alias: Location - Household Away Mode Locks
  id: 'location_household_away_mode_locks'

  triggers:
    - trigger: state
      entity_id: group.household
      from: 'home'
      to: 'not_home'

  conditions:
    - condition: state
      entity_id: input_boolean.disable_home_away
      state: 'off'

  actions:
    - action: lock.lock
      target:
        entity_id:
        - lock.front_door
        - lock.back_door
        - lock.basement_door
""",
"""
- alias: Locks - Lock Front Door After 30 Mins
  id: 'locks_lock_front_door_after_30_mins'

  triggers:
    - trigger: state
      entity_id: lock.front_door
      from: 'locked'
      to: 'unlocked'
      for:
        hours: 0
        minutes: 30
        seconds: 0

  conditions:
    - condition: state
      entity_id: input_boolean.disable_lock_unlock_doors
      state: 'off'
    - condition: state
      entity_id: binary_sensor.front_door_opened
      state: 'off'
    - condition: state
      entity_id: lock.front_door
      state: 'unlocked'

  actions:
    - action: lock.lock
      entity_id: lock.front_door
""",
"""
- alias: Motion - Turn Off Living Room Lights when No Motion Detected
  id: 'motion_turn_off_living_room_lights_when_no_motion_detected'

  triggers:
    - trigger: state
      entity_id: binary_sensor.living_room_motion
      from: 'on'
      to: 'off'
      for:
        hours: 2
        minutes: 0
        seconds: 0

  conditions:
    - condition: state
      entity_id: input_boolean.disable_motion
      state: 'off'
    - condition: state
      entity_id: input_boolean.living_room_guest
      state: 'off'
    - condition: state
      entity_id: group.household
      state: 'home'
    - condition: state
      entity_id: light.living_room_lights
      state: 'on'
    - condition: not
      conditions:
      - condition: state
        entity_id: vacuum.main_floor_roomba
        state: 'cleaning'
      - condition: state
        entity_id: vacuum.main_floor_roomba
        state: 'returning'

  actions:
    - action: light.turn_off
      target:
        entity_id:
          - light.living_room_lights
""",
"""
- alias: Network - Re-Enable Pi-hole After 30 Mins
  id: 'network_reenable_pihole_after_30_mins'

  triggers:
    - trigger: state
      entity_id: input_boolean.pihole
      from: 'on'
      to: 'off'
      for:
        hours: 0
        minutes: 31
        seconds: 0

  conditions:
    - condition: state
      entity_id: input_boolean.pihole
      state: 'off'

  actions:
    - action: homeassistant.turn_on
      target:
        entity_id:
          - input_boolean.pihole
""",
"""
- alias: Network - Re-Enable Pi-hole After 30 Mins
  id: 'network_reenable_pihole_after_30_mins'

  triggers:
    - trigger: state
      entity_id: input_boolean.pihole
      from: 'on'
      to: 'off'
      for:
        hours: 0
        minutes: 31
        seconds: 0

  conditions:
    - condition: state
      entity_id: input_boolean.pihole
      state: 'off'

  actions:
    - action: homeassistant.turn_on
      target:
        entity_id:
          - input_boolean.pihole
""",
"""
- alias: Occupancy - Turn Off Guest Bedroom Lights when Unoccupied
  id: 'occupancy_turn_off_guest_bedroom_lights_when_unoccupied'

  triggers:
    - trigger: state
      entity_id: binary_sensor.guest_bedroom_occupancy
      from: 'on'
      to: 'off'
      for:
        hours: 0
        minutes: 30
        seconds: 0

  conditions:
    - condition: state
      entity_id: input_boolean.disable_occupancy
      state: 'off'
    - condition: state
      entity_id: input_boolean.guest_mode
      state: 'off'
    - condition: not
      conditions:
      - condition: state
        entity_id: vacuum.upstairs_roomba
        state: 'cleaning'
      - condition: state
        entity_id: vacuum.upstairs_roomba
        state: 'returning'

  actions:
    - action: light.turn_off
      entity_id: light.guest_bedroom_lights
"""
]


@pytest.mark.parametrize("code", GOOD_CODES)
def test_good_codes_have_no_errors(code):
    errors = analyze_yaml(code)
    real_errors = [e for e in errors if not e.get('rule', '').startswith('warning_')]
    assert len(real_errors) == 0, f"Good code has real errors: {real_errors}"