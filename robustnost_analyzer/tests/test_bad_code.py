import pytest
from tests.util import analyze_yaml


BAD_CODES = [
    """
alias: D1_all_errors
trigger:
  - platform: state
    entity_id: light.living_room
    from: 'off'
    to: 'On'
condition:
  - condition: state
    entity_id: sensor.door
    state: 'Open'
action:
  - service: light.turn_on
    data:
      entity_id: light.kitchen
      state: 'On'
""",

    """
alias: D5_error_from_sheik_example
trigger:
  - platform: state
    entity_id: light.living_room
    from: 'off'
    to: 'on'
condition:
- condition: sun
  before: sunrise
  after: sunset
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
alias: Shutdown VM
trigger: []
condition: []
action:
  - service: rest_command.proxmox_vm_shutdown
    metadata:
      vmName: frigate
    data:
      vmid: "{{ (vm_list.content.data | select('search', vmName) | first).vmid }}"
      host: "{{ (vm_list.content.data | select('search', vmName) | first).node }}"
enabled: true
""",
"""
alias: D1 ale wait_template

trigger:
  - platform: state
    entity_id: sensor.dryer
    to: "running"

action:
  - wait_template: "{{ is_state('fan.bathroom', 'Off') }}"
""",
"""
alias: wrong_state_case
trigger:
  - type: no_motion
    platform: device
    device_id: e0954ea41d7a6da69baeff2e9558ed13
    entity_id: binary_sensor.v4b01_motion
    domain: binary_sensor
    id: '1'
    for:
      hours: 0
      minutes: "{{states('input_number.timeout_offices')|int(0) }}"
      seconds: 0
action: []
""",
"""
alias: D3_error
trigger:
  - platform: state
    entity_id: light.living_room
    from: 'off'
    to: 'on'
condition:
  - condition: state
    entity_id: sensor.door
    state: 'open'
action:
  - service: notify.mobile_app_huawei_p20
    data:
      title: Temperature Warning
      message: "Temperature is {{ sensor.temperatur_gefrierschrank }}"
""",
"""
alias: D5_error_trigger_offset_sun
trigger:
  - trigger: sun
    event: sunrise
    offset: "-25:00:00"
action: []
""",
"""
alias: D5_error_trigg_offset_time
trigger:
  - trigger: time
    at: "23:00:00"
    weekday: [mon]
    offset: "+25:00:00"
action: []
""",
"""
alias: D5_error_both_trigg_cond_num_state_above_below
trigger:
  - trigger: numeric_state
    entity_id: sensor.temp
    above: 10
    below: 5
condition:
  - condition: numeric_state
    entity_id: sensor.temp
    above: 100
    below: 0
action: []
""",
"""
alias: D5_error_zone_trigg
trigger:
  - trigger: zone
    entity_id: person.me
    zone: zone.home
    event: enter
  - trigger: zone
    entity_id: person.me
    zone: zone.home
    event: leave
action: []
""",
"""
alias: D5_error_action_if_sun
trigger:
  []
action:
  - if:
      - alias: "If no one is home"
        condition: sun
        before: sunrise
        after: sunset
    then:
      - alias: "Then start cleaning already!"
        action: vacuum.start
        target:
          area_id: living_room
    else:
      - action: notify.notify
        data:
          message: "Skipped cleaning, someone is home!"
""",
"""     
alias: D5_error_while_until
trigger:
  []
action:
  - repeat:
      while:
        - condition: time
          after: sunset
      until:
        - condition: time
          before: sunrise
""",
"""
alias: D6_error_unknown_parameter_condition 
trigger:
  []
condition:
  - condition: state
    entity_id: light.kuchyne
    state: 'on'
    atribute: "{{ states('light.kuchyne') == 'on' }}"
action:
  []
""",
"""
alias: D6_error_while_until_wrong_atribute
trigger:
  []
action:
  - repeat:
      while:
        - condition: sun
          after: sunset
          atribute: "asncjkbd"
      until:
        - condition: sun
          after: sunset
          atribute: "asncjkbd"
""",
"""
alias: Tool Bench Lights
description: ""
trigger: []
condition: []
action:
  - wait_for_trigger:
      - platform: state
        entity_id: light.kitchen
        to: 'on'
""",
"""
alias: Tool Bench Lights
trigger: []
condition: []
action:
  - wait_for_trigger:
      - type: no_motion
        platform: device
        device_id: 09ea66b8006a002cb6ffa125e6f7deeb
        entity_id: f2d3faa59b3fa5680c49eab5927b5010
        domain: binary_sensor
        to: 'on'
mode: single
""",
"""
alias: Tool Bench Lights rovnaky trigger && wait_for_trigger
trigger:
  - platform: state
    entity_id: binary_sensor.pohyb
    to: 'on'
condition: []
action:
  - wait_for_trigger:
      - platform: state
        entity_id: binary_sensor.pohyb
        to: 'off'
  - wait_for_trigger:
      - platform: state
        entity_id: binary_sensor.pohyb
        to: 'on'
  - service: notify.send
mode: single
""",
"""
alias: Tool Bench Lights
trigger:
  - platform: state
    entity_id: binary_sensor.pohyb
    to: 'on'
condition: []
action:
- service: tts.google_say
  data:
  entity_id: media_player.living_room_speaker
  message: Dryer has started
  cache: true
  cache_dir: /tmp/tts
mode: single
""",
"""
alias: Fix Broken Sensor

trigger:
  - platform: time
    at: "03:00:00"

action:
  - service: homeassistant.update_entity
    target:
      entity_id: sensor.temperature_outside
    data:
      state: "20"
      unit: "°C"
""",
""" 
alias: Dryer Notification zanoreny 'state'

trigger:
  - platform: state
    entity_id: sensor.dryer
    to: "running"

action:
  - choose:
      - conditions:
          - condition: time
            after: "08:00:00"
        sequence:
          - service: media_player.turn_on
            target:
              entity_id: media_player.living_room
            data:
              state: "on" 
              volume: 0.5
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
alias: no_trigger_and_action

trigger: []

action: []
"""
]

@pytest.mark.parametrize("code", BAD_CODES)
def test_bad_codes_raise_errors(code):
    errors = analyze_yaml(code)
    assert len(errors) > 0, "Bad code should have errors"