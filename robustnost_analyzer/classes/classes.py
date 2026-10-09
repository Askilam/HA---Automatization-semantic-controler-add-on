#definicia tried
from dataclasses import dataclass, field
from typing import List, Optional, Union, Any, Dict

@dataclass
class Automation:
    alias: Optional[str] = None
    id: Optional[str] = None
    description: Optional[str] = None
    mode: Optional[str] = None
    max: Optional[int] = None
    max_exceeded: Optional[str] = None
    trigger_variables: Optional[Dict[str, Any]] = None
    triggers: List["Trigger"] = field(default_factory=list)
    conditions: List["Condition"] = field(default_factory=list)
    actions: List["Action"] = field(default_factory=list)
    variables: Optional[Any] = None
    metadata: Optional[Dict[str, Any]] = None
#------------TRIG-----------
@dataclass
class Trigger:
    id: Optional[str] = None
    enabled: Optional[bool] = True
    variables: Optional[Dict[str, Any]] = None

@dataclass
class Event_trigger(Trigger):
    event_type: Union[str, List[str]] = field(default_factory=list)
    event_data: Optional[Dict[str, Any]] = None
    context: Optional[Dict[str, Any]] = None
    trigger_type: str = "event"

@dataclass
class Home_assistant_trigger(Trigger):
    trigger_type: str = "homeassistant"
    event: str = ""

@dataclass
class MQTT_trigger(Trigger):
    trigger_type: str = "mqtt"
    topic: str = ""
    payload: Optional[str] = None
    encoding: Optional[str] = "utf-8"
    value_template: Optional[str] = None

@dataclass
class Numeric_state_trigger(Trigger):
    trigger_type: str = "numeric_state"
    entity_id: Union[str, List[str]] = field(default_factory=list)
    attribute: Optional[str] = None
    above: Optional[Union[float, str]] = None
    below: Optional[Union[float, str]] = None
    value_template: Optional[str] = None
    for_loop: Optional[Dict[str, int]] = None

@dataclass
class State_trigger(Trigger):
    trigger_type: str = "state"
    entity_id: Union[str, List[str]] = field(default_factory=list)
    from_: Optional[Union[str, List[str]]] = None
    to_: Optional[Union[str, List[str]]] = None
    for_loop: Optional[Dict[str, int]] = None
    not_from: Optional[Union[str, List[str]]] = None
    not_to: Optional[Union[str, List[str]]] = None
    attribute: Optional[str] = None

@dataclass
class Sun_trigger(Trigger):
    trigger_type: str = "sun"
    event: str = ""
    offset: Optional[str] = None

@dataclass
class Tag_trigger(Trigger):
    trigger_type: str = "tag"
    tag_id: Union[str, List[str]] = field(default_factory=list)
    device_id: Optional[Union[str, List[str]]] = None

@dataclass
class Template_trigger(Trigger):
    trigger_type: str = "template"
    value_template: str = ""
    for_loop: Optional[Dict[str, int]] = None

@dataclass
class Time_trigger(Trigger):
    trigger_type: str = "time"
    at: Union[str, List[str]] = field(default_factory=list)
    offset: Optional[str] = None
    weekday: Optional[Union[str, List[str]]] = None

@dataclass
class Time_pattern_trigger(Trigger):
    trigger_type: str = "time_pattern"
    hours: Optional[str] = None
    minutes: Optional[str] = None
    seconds: Optional[str] = None

@dataclass
class Persistent_notification_trigger(Trigger):
    trigger_type: str = "persistent_notification"
    notification_id: Union[str, List[str]] = field(default_factory=list)
    update_type: str = ""

@dataclass
class Webhook_trigger(Trigger):
    trigger_type: str = "webhook"
    webhook_id: str = ""
    allowed_methods: Optional[List[str]] = None
    local_only: Optional[bool] = True

@dataclass
class Zone_trigger(Trigger):
    trigger_type: str = "zone"
    entity_id: Union[str, List[str]] = field(default_factory=list)
    zone: str = ""
    event: str = ""

@dataclass
class Geolocation_trigger(Trigger):
    trigger_type: str = "geo_location"
    source: str = ""
    zone: str = ""
    event: str = ""

@dataclass
class Calendar_trigger(Trigger):
    trigger_type: str = "calendar"
    event: str = ""
    entity_id: str = ""
    offset: Optional[str] = None

@dataclass
class Sentence_trigger(Trigger):
    trigger_type: str = "conversation"
    command: List[str] = field(default_factory=list)

@dataclass
class Unknown_trigger(Trigger):
    trigger_type: str = ""
    params: Dict[str, Any] = field(default_factory=dict)

Trigger = Union[
    Event_trigger, Home_assistant_trigger, MQTT_trigger, Numeric_state_trigger, 
    State_trigger, Sun_trigger, Tag_trigger, Template_trigger, Time_trigger, 
    Time_pattern_trigger, Persistent_notification_trigger, 
    Webhook_trigger, Zone_trigger, Geolocation_trigger, Calendar_trigger, 
    Sentence_trigger, Unknown_trigger
]
#------------COND-----------
@dataclass
class Condition:
    condition_type: str = ""
    enabled: Optional[bool] = True

@dataclass
class And_condition(Condition):
    condition_type: str = "and"
    conditions: List["Condition"] = field(default_factory=list)

@dataclass
class Or_condition(Condition):
    condition_type: str = "or"
    conditions: List["Condition"] = field(default_factory=list)

@dataclass
class Not_condition(Condition):
    condition_type: str = "not"
    conditions: List["Condition"] = field(default_factory=list)
    

@dataclass
class Numeric_state_condition(Condition):
    condition_type: str = "numeric_state"
    entity_id: Union[str, List[str]] = field(default_factory=list)
    above: Optional[Union[float, str]] = None
    below: Optional[Union[float, str]] = None
    value_template: Optional[str] = None
    attribute: Optional[str] = None

@dataclass
class State_condition(Condition):
    condition_type: str = "state"
    entity_id: str = ""
    state: Union[str, List[str]] = field(default_factory=list)
    for_loop: Optional[Dict[str, int]] = None
    attribute: Optional[str] = None
    extra_params: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Sun_condition(Condition):
    condition_type: str = "sun"
    after: Optional[str] = None
    before: Optional[str] = None
    after_offset: Optional[str] = None
    before_offset: Optional[str] = None
    extra_params: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Template_condition(Condition):
    condition_type: str = "template"
    value_template: str = ""

@dataclass
class Time_condition(Condition):
    condition_type: str = "time"
    after: Optional[str] = None
    before: Optional[str] = None
    weekday: Optional[Union[str, List[str]]] = None
    extra_params: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Trigger_condition(Condition):
    condition_type: str = "trigger"
    id: Union[str, List[str]] = field(default_factory=list)

@dataclass
class Zone_condition(Condition):
    condition_type: str = "zone"
    zone: str = ""
    entity_id: Union[str, List[str]] = field(default_factory=list)
    state: Optional[Union[str, List[str]]] = None
    extra_params: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Unknown_condition(Condition):
    condition_type: str = ""
    params: Dict[str, Any] = field(default_factory=dict)

Condition = Union[
    And_condition, Or_condition, Not_condition, Numeric_state_condition,
    State_condition, Template_condition, Time_condition, Trigger_condition, 
    Zone_condition, Sun_condition, Unknown_condition
]
#------------ACTI-----------
@dataclass
class Action: 
    action_type: Optional[str] = None
    id: Optional[str] = None
    alias: Optional[str]  = None
    enabled: Optional[bool] = True
    continue_on_error: Optional[bool] = False
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class Service_action(Action):
    action_type: str = "service"
    service: str = ""
    target: Optional[Dict[str, Any]] = None
    data: Optional[Dict[str, Any]] = None
    data_template: Optional[Dict[str, Any]] = None
    response_variable: Optional[str] = None
    extra_params: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Scene_action(Action):
    action_type: str = "scene"
    scene: str = ""

@dataclass
class Variable_action(Action):
    action_type: str = "variables"
    variables: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Condition_action(Action):
    action_type: str = "condition"
    conditions: List[Condition] = field(default_factory=list)

@dataclass
class Delay_action(Action):
    action_type: str = "delay"
    delay: Union[str, Dict[str, int]] = ""

@dataclass
class Wait_template_action(Action):
    action_type: str = "wait_template"
    wait_template: str = ""
    timeout: Optional[Union[str, Dict[str, int]]] = "None"
    continue_on_timeout: Optional[bool] = True
    response_variable: Optional[str] = None

@dataclass
class Wait_trigger_action(Action):
    action_type: str = "wait_for_trigger"
    wait_for_trigger: List[Trigger] = field(default_factory=list)
    timeout: Optional[Union[str, Dict[str, int]]] = None
    continue_on_timeout: Optional[bool] = True
    response_variable: Optional[str] = None

@dataclass
class Event_action(Action):
    action_type: str = "event"
    event: str = ""
    event_data: Optional[Dict[str, Any]] = None

@dataclass
class Repeat_action(Action):
    action_type: str = "repeat"
    count: Optional[Union[int, str]] = None
    for_each: Optional[List[Any]] = None
    while_: Optional[List[Condition]] = None
    until: Optional[List[Condition]] = None
    sequence: List["Action"] = field(default_factory=list)

@dataclass
class If_action(Action):
    action_type: str = "if"
    if_: List[Condition] = field(default_factory=list)
    then: List["Action"] = field(default_factory=list)
    else_: Optional[List["Action"]] = field(default_factory=list)

@dataclass
class Choose_action(Action):
    action_type: str = "choose"
    choose: List[Dict[str, Any]] = field(default_factory=list)
    default: Optional[List["Action"]] = field(default_factory=list)

@dataclass
class Sequence_action(Action):
    action_type: str = "sequence"
    sequence: List["Action"] = field(default_factory=list)

@dataclass
class Parallel_action(Action):
    action_type: str = "parallel"
    parallel: List[List["Action"]] = field(default_factory=list)

@dataclass
class Stop_action(Action):
    action_type: str = "stop"
    stop: str = ""
    error: Optional[bool] = False

@dataclass
class Set_conversation_response_action(Action):
    action_type: str = "set_conversation_response"
    set_conversation_response: Union[str, None] = None

@dataclass
class Device_action(Action):
    action_type: str = "device"
    params: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Unknown_action(Action):
    action_type: str = ""
    params: Dict[str, Any] = field(default_factory=dict)

Action = Union[
    Service_action, Scene_action, Variable_action, Condition_action, 
    Delay_action, Wait_template_action, Wait_trigger_action, Event_action, 
    Repeat_action, If_action, Choose_action, Sequence_action, Parallel_action, 
    Stop_action, Set_conversation_response_action, Device_action, Unknown_action
]