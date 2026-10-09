#naplnenie tried (instancie) = tvorba IR (intermediate representation)
from __future__ import annotations
from typing import Union, List, Dict, Any
from ruamel.yaml.comments import CommentedMap, CommentedSeq
from classes.classes import (
    Automation,
    Trigger, Event_trigger, Home_assistant_trigger, MQTT_trigger, Numeric_state_trigger,
    State_trigger, Sun_trigger, Tag_trigger, Template_trigger, Time_trigger,
    Time_pattern_trigger, Persistent_notification_trigger, Webhook_trigger,
    Zone_trigger, Geolocation_trigger, Calendar_trigger, Sentence_trigger, Unknown_trigger,
    Condition, And_condition, Or_condition, Not_condition, Numeric_state_condition,
    State_condition, Template_condition, Time_condition, Trigger_condition,
    Zone_condition, Sun_condition, Unknown_condition,
    Action, Service_action, Scene_action, Variable_action, Condition_action,
    Delay_action, Wait_template_action, Wait_trigger_action, Event_action,
    Repeat_action, If_action, Choose_action, Sequence_action, Parallel_action,
    Stop_action, Set_conversation_response_action, Device_action, Unknown_action
)
def ruamel_to_plain(obj: Any) -> Any:
    if isinstance(obj, (CommentedMap, dict)):
        return {k: ruamel_to_plain(v) for k, v in obj.items()}
    elif isinstance(obj, (CommentedSeq, list)):
        return [ruamel_to_plain(item) for item in obj]
    else:
        return obj

def ruamel_to_IR(data: Any, errors: List[Dict[str, Any]] = None) -> List[Automation]:
    plain_data = ruamel_to_plain(data)
    if isinstance(plain_data, dict):
        plain_data = [plain_data]
    automations = []
    for one_automation in plain_data:
        
        triggers_data = one_automation.get('triggers') or one_automation.get('trigger', [])
        conditions_data = one_automation.get('conditions') or one_automation.get('condition', [])
        actions_data = one_automation.get('actions') or one_automation.get('action', [])
        
        if not isinstance(triggers_data, list):
            triggers_data = [triggers_data] if triggers_data else []
        if not isinstance(actions_data, list):
            actions_data = [actions_data] if actions_data else []

        
        triggers_ir = [ruamel_to_trigger(one_trig) for one_trig in triggers_data if isinstance(one_trig, dict)]
        if not triggers_ir:
            triggers_ir = [Unknown_trigger(trigger_type="empty")]

        actions_ir = [ruamel_to_action(one_act, errors) for one_act in actions_data if isinstance(one_act, dict)]
        if not actions_ir:
            actions_ir = [Unknown_action(action_type="empty")]

        one_automation_final = Automation(
            alias=one_automation.get('alias'),
            id=one_automation.get('id'),
            description=one_automation.get('description'),
            mode=one_automation.get('mode'),
            max=one_automation.get('max'),
            max_exceeded=one_automation.get('max_exceeded'),
            trigger_variables=one_automation.get('trigger_variables'),
            variables=one_automation.get('variables'),
            triggers=triggers_ir,
            conditions=[ruamel_to_condition(one_cond) for one_cond in condition_to_list(conditions_data)],
            actions=actions_ir
        )
        automations.append(one_automation_final)
    return automations


def condition_to_list(conditions: Union[Dict[str, Any], List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    if isinstance(conditions, dict):
        return [conditions]
    return conditions


def ruamel_to_trigger(one_trigger: Dict[str, Any]) -> Trigger:
    
    trigger_type = one_trigger.get('platform', '')
    
    if trigger_type == 'event':
        event_type = one_trigger.get('event_type')
        if event_type is None:
            return Unknown_trigger(trigger_type=trigger_type, params=one_trigger)
        return Event_trigger(
            id = one_trigger.get('id'),
            enabled = one_trigger.get('enabled', True),
            variables = one_trigger.get('variables'),
            trigger_type = trigger_type,
            event_type = event_type,
            event_data = one_trigger.get('event_data'),
            context = one_trigger.get('context')
        )
    elif trigger_type == 'homeassistant':
        return Home_assistant_trigger(
            id = one_trigger.get('id'),
            enabled = one_trigger.get('enabled', True),
            variables = one_trigger.get('variables'),
            trigger_type = trigger_type,
            event = one_trigger.get('event', '')
        )
    elif trigger_type == 'mqtt':
        return MQTT_trigger(
            id = one_trigger.get('id'),
            enabled = one_trigger.get('enabled', True),
            variables = one_trigger.get('variables'),
            trigger_type = trigger_type,
            topic = one_trigger.get('topic', ''),
            payload = one_trigger.get('payload'),
            encoding = one_trigger.get('encoding', 'utf-8'),
            value_template = one_trigger.get('value_template')
        )
    elif trigger_type == 'numeric_state':
        return Numeric_state_trigger(
            id = one_trigger.get('id'),
            enabled = one_trigger.get('enabled', True),
            variables = one_trigger.get('variables'),
            trigger_type = trigger_type,
            entity_id = one_trigger.get('entity_id', []),
            attribute = one_trigger.get('attribute'),
            above = one_trigger.get('above'),
            below = one_trigger.get('below'),
            value_template = one_trigger.get('value_template'),
            for_loop = one_trigger.get('for')
        )
    elif trigger_type == 'state':
        return State_trigger(
            id = one_trigger.get('id'),
            enabled = one_trigger.get('enabled', True),
            variables = one_trigger.get('variables'),
            trigger_type = trigger_type,
            entity_id = one_trigger.get('entity_id', []),
            from_ = one_trigger.get('from'),
            to_ = one_trigger.get('to'),
            for_loop = one_trigger.get('for'),
            not_from = one_trigger.get('not_from'),
            not_to = one_trigger.get('not_to'),
            attribute = one_trigger.get('attribute')
        )
    elif trigger_type == 'sun':
        return Sun_trigger(
            id = one_trigger.get('id'),
            enabled = one_trigger.get('enabled', True),
            variables = one_trigger.get('variables'),
            trigger_type = trigger_type,
            event = one_trigger.get('event', ''),
            offset = one_trigger.get('offset')
        )
    elif trigger_type == 'tag':
        return Tag_trigger(
            id = one_trigger.get('id'),
            enabled = one_trigger.get('enabled', True),
            variables = one_trigger.get('variables'),
            trigger_type = trigger_type,
            tag_id = one_trigger.get('tag_id', []),
            device_id = one_trigger.get('device_id')
        )
    elif trigger_type == 'template':
        return Template_trigger(
            id = one_trigger.get('id'),
            enabled = one_trigger.get('enabled', True),
            variables = one_trigger.get('variables'),
            trigger_type = trigger_type,
            value_template = one_trigger.get('value_template', ''),
            for_loop = one_trigger.get('for')
        )
    elif trigger_type == 'time':
        return Time_trigger(
            id = one_trigger.get('id'),
            enabled = one_trigger.get('enabled', True),
            variables = one_trigger.get('variables'),
            trigger_type = trigger_type,
            at = one_trigger.get('at', []),
            offset = one_trigger.get('offset'),
            weekday = one_trigger.get('weekday')
        )
    elif trigger_type == 'time_pattern':
        return Time_pattern_trigger(
            id = one_trigger.get('id'),
            enabled = one_trigger.get('enabled', True),
            variables = one_trigger.get('variables'),
            trigger_type = trigger_type,
            hours = one_trigger.get('hours'),
            minutes = one_trigger.get('minutes'),
            seconds = one_trigger.get('seconds')
        )
    elif trigger_type == 'persistent_notification':
        return Persistent_notification_trigger(
            id = one_trigger.get('id'),
            enabled = one_trigger.get('enabled', True),
            variables = one_trigger.get('variables'),
            trigger_type = trigger_type,
            notification_id = one_trigger.get('notification_id', []),
            update_type = one_trigger.get('update_type', '')
        )
    elif trigger_type == 'webhook':
        return Webhook_trigger(
            id = one_trigger.get('id'),
            enabled = one_trigger.get('enabled', True),
            variables = one_trigger.get('variables'),
            trigger_type = trigger_type,
            webhook_id = one_trigger.get('webhook_id', ''),
            allowed_methods = one_trigger.get('allowed_methods'),
            local_only = one_trigger.get('local_only', True)
        )
    elif trigger_type == 'zone':
        return Zone_trigger(
            id = one_trigger.get('id'),
            enabled = one_trigger.get('enabled', True),
            variables = one_trigger.get('variables'),
            trigger_type = trigger_type,
            entity_id = one_trigger.get('entity_id', []),
            zone = one_trigger.get('zone', ''),
            event = one_trigger.get('event', '')
        )
    elif trigger_type == 'geo_location':
        return Geolocation_trigger(
            id = one_trigger.get('id'),
            enabled = one_trigger.get('enabled', True),
            variables = one_trigger.get('variables'),
            trigger_type = trigger_type,
            source = one_trigger.get('source', ''),
            zone = one_trigger.get('zone', ''),
            event = one_trigger.get('event', '')
        )
    elif trigger_type == 'calendar':
        return Calendar_trigger(
            id = one_trigger.get('id'),
            enabled = one_trigger.get('enabled', True),
            variables = one_trigger.get('variables'),
            trigger_type = trigger_type,
            event = one_trigger.get('event', ''),
            entity_id = one_trigger.get('entity_id', ''),
            offset = one_trigger.get('offset')
        )
    elif trigger_type == 'conversation':
        return Sentence_trigger(
            id = one_trigger.get('id'),
            enabled = one_trigger.get('enabled', True),
            variables = one_trigger.get('variables'),
            trigger_type = trigger_type,
            command = one_trigger.get('command', [])
        )
    else:
        return Unknown_trigger(
            id = one_trigger.get('id'),
            enabled = one_trigger.get('enabled', True),
            variables = one_trigger.get('variables'),
            trigger_type = trigger_type,
            params = one_trigger
        )


def ruamel_to_condition(one_condition: Dict[str, Any]) -> Condition:
    
    condition_type = one_condition.get('condition', '')

    if condition_type == 'and':
        return And_condition(
            enabled = one_condition.get('enabled', True),
            conditions=[ruamel_to_condition(condition) for condition in condition_to_list(one_condition.get('conditions', []))]
        )
    elif condition_type == 'or':
        return Or_condition(
            enabled = one_condition.get('enabled', True),
            conditions = [ruamel_to_condition(condition) for condition in condition_to_list(one_condition.get('conditions', []))]
        )
    elif condition_type == 'not':
        return Not_condition(
            enabled=one_condition.get('enabled', True),
            conditions=[ruamel_to_condition(condition) for condition in condition_to_list(one_condition.get('conditions', []))]
        )
    elif condition_type == 'numeric_state':
        return Numeric_state_condition(
            enabled = one_condition.get('enabled', True),
            entity_id = one_condition.get('entity_id', []),
            above = one_condition.get('above'),
            below = one_condition.get('below'),
            value_template = one_condition.get('value_template'),
            attribute = one_condition.get('attribute')
        )
    elif condition_type == 'sun':
        known_keys = {'alias', 'condition', 'enabled', 'after', 'before', 'after_offset', 'before_offset'}
        extra = {key: val for key, val in one_condition.items() if key not in known_keys}
        return Sun_condition(
            enabled=one_condition.get('enabled', True),
            after=one_condition.get('after'),
            before=one_condition.get('before'),
            after_offset=one_condition.get('after_offset'),
            extra_params=extra,
            before_offset=one_condition.get('before_offset')
    )
    elif condition_type == 'state':
        known_keys = {'alias', 'condition', 'enabled', 'entity_id', 'state', 'for', 'attribute'}
        extra = {key: val for key, val in one_condition.items() if key not in known_keys}
        return State_condition(
            enabled = one_condition.get('enabled', True),
            entity_id = one_condition.get('entity_id', ''),
            state = one_condition.get('state', []),
            for_loop = one_condition.get('for'),
            attribute = one_condition.get('attribute'),
            extra_params=extra
        )
    elif condition_type == 'template':
        return Template_condition(
            enabled = one_condition.get('enabled', True),
            value_template = one_condition.get('value_template', '')
        )
    elif condition_type == 'time':
        known_keys = {'alias', 'condition', 'enabled', 'after', 'before', 'weekday'}
        extra = {key: val for key, val in one_condition.items() if key not in known_keys}
        return Time_condition(
            enabled = one_condition.get('enabled', True),
            after = one_condition.get('after'),
            before = one_condition.get('before'),
            weekday = one_condition.get('weekday'),
            extra_params=extra
        )
    elif condition_type == 'trigger':
        return Trigger_condition(
            enabled = one_condition.get('enabled', True),
            id = one_condition.get('id', [])
        )
    elif condition_type == 'zone':
        known_keys = {'alias', 'condition', 'enabled', 'zone', 'entity_id', 'state'}
        extra = {key: val for key, val in one_condition.items() if key not in known_keys}
        return Zone_condition(
            enabled = one_condition.get('enabled', True),
            zone = one_condition.get('zone', ''),
            entity_id = one_condition.get('entity_id', []),
            state = one_condition.get('state'),
            extra_params=extra
        )
    else:
        return Unknown_condition(
            enabled = one_condition.get('enabled', True),
            condition_type = condition_type,
            params = one_condition
        )


def ruamel_to_action(one_action: Dict[str, Any], errors: List[Dict[str, Any]] = None) -> Action:
    if 'action' in one_action:
        one_action['service'] = one_action.pop('action')

    if 'service' in one_action:
        known_keys = {'alias', 'id', 'enabled', 'continue_on_error', 'service', 'target', 'data', 'data_template', 'response_variable', 'metadata', 'entity_id', 'message'}
        extra = {key: val for key, val in one_action.items() if key not in known_keys}
        return Service_action(
            id = one_action.get('id'),
            alias = one_action.get('alias'),
            enabled = one_action.get('enabled', True),
            continue_on_error = one_action.get('continue_on_error', False),
            service = one_action.get('service', ''),
            target = one_action.get('target'),
            data = one_action.get('data'),
            data_template = one_action.get('data_template'),
            response_variable = one_action.get('response_variable'),
            metadata=one_action.get('metadata'),
            extra_params=extra
        )
    elif 'scene' in one_action:
        return Scene_action(
            id = one_action.get('id'),
            alias = one_action.get('alias'),
            enabled = one_action.get('enabled', True),
            continue_on_error = one_action.get('continue_on_error', False),
            scene = one_action.get('scene', ''),
            metadata=one_action.get('metadata')
        )
    elif 'variables' in one_action:
        return Variable_action(
            id = one_action.get('id'),
            alias = one_action.get('alias'),
            enabled = one_action.get('enabled', True),
            continue_on_error = one_action.get('continue_on_error', False),
            variables = one_action.get('variables', {}),
            metadata=one_action.get('metadata')
        )
    elif 'condition' in one_action:
        return Condition_action(
            id = one_action.get('id'),
            alias = one_action.get('alias'),
            enabled = one_action.get('enabled', True),
            continue_on_error = one_action.get('continue_on_error', False),
            conditions = [ruamel_to_condition(condition) for condition in condition_to_list(one_action.get('condition', []))],
            metadata=one_action.get('metadata')
        )
    elif 'delay' in one_action:
        return Delay_action(
            id = one_action.get('id'),
            alias = one_action.get('alias'),
            enabled = one_action.get('enabled', True),
            continue_on_error = one_action.get('continue_on_error', False),
            delay = one_action.get('delay', ''),
            metadata=one_action.get('metadata')
        )
    elif 'wait_template' in one_action:
        return Wait_template_action(
            id = one_action.get('id'),
            alias = one_action.get('alias'),
            enabled = one_action.get('enabled', True),
            continue_on_error = one_action.get('continue_on_error', False),
            wait_template = one_action.get('wait_template', ''),
            timeout = one_action.get('timeout', "None"),
            continue_on_timeout = one_action.get('continue_on_timeout', True),
            response_variable = one_action.get('response_variable'),
            metadata=one_action.get('metadata')
        )
    elif 'wait_for_trigger' in one_action:
        return Wait_trigger_action(
            id = one_action.get('id'),
            alias = one_action.get('alias'),
            enabled = one_action.get('enabled', True),
            continue_on_error = one_action.get('continue_on_error', False),
            wait_for_trigger = [ruamel_to_trigger(trigger) for trigger in one_action.get('wait_for_trigger', [])],
            timeout = one_action.get('timeout'),
            continue_on_timeout = one_action.get('continue_on_timeout', True),
            response_variable = one_action.get('response_variable'),
            metadata=one_action.get('metadata')
        )
    elif 'event' in one_action:
        return Event_action(
            id = one_action.get('id'),
            alias = one_action.get('alias'),
            enabled = one_action.get('enabled', True),
            continue_on_error = one_action.get('continue_on_error', False),
            event = one_action.get('event', ''),
            event_data = one_action.get('event_data'),
            metadata=one_action.get('metadata')
        )
    elif 'repeat' in one_action:
        repeat_data = one_action.get('repeat', {})
        return Repeat_action(
            id = one_action.get('id'),
            alias = one_action.get('alias'),
            enabled = one_action.get('enabled', True),
            continue_on_error = one_action.get('continue_on_error', False),
            count = one_action.get('count'),
            for_each = one_action.get('for_each'),
            while_=[ruamel_to_condition(condition) for condition in condition_to_list(repeat_data.get('while', []))],
            until=[ruamel_to_condition(condition) for condition in condition_to_list(repeat_data.get('until', []))],
            sequence=[ruamel_to_action(action, errors) for action in repeat_data.get('sequence', [])],
            metadata=one_action.get('metadata')
        )
    elif 'if' in one_action:
        return If_action(
            id = one_action.get('id'),
            alias = one_action.get('alias'),
            enabled = one_action.get('enabled', True),
            continue_on_error = one_action.get('continue_on_error', False),
            if_ = [ruamel_to_condition(c) for c in condition_to_list(one_action.get('if', []))],
            then = [ruamel_to_action(action) for action in one_action.get('then', [])],
            else_ = [ruamel_to_action(action, errors) for action in one_action.get('else', [])],
            metadata=one_action.get('metadata')
        )
    elif 'choose' in one_action:
        choices = []
        for choice_dict in one_action.get('choose', []):
            choice = {
                'conditions': [ruamel_to_condition(condition) for condition in condition_to_list(choice_dict.get('conditions', []))],
                'sequence': [ruamel_to_action(action, errors) for action in choice_dict.get('sequence', [])]
            }
            #if not choice['sequence']:
            #    errors.append({
            #        'type': 'structural',
            #       'message': "Indentation error for 'sequence:' in 'choose' action. For each 'conditions' there must be an equally indented 'sequence'."
            #    })
            choices.append(choice)
        return Choose_action(
            id = one_action.get('id'),
            alias = one_action.get('alias'),
            enabled = one_action.get('enabled', True),
            continue_on_error = one_action.get('continue_on_error', False),
            choose = choices,
            default = [ruamel_to_action(action, errors) for action in one_action.get('default', [])],
            metadata=one_action.get('metadata')
        )
    elif 'sequence' in one_action:
        return Sequence_action(
            id = one_action.get('id'),
            alias = one_action.get('alias'),
            enabled = one_action.get('enabled', True),
            continue_on_error = one_action.get('continue_on_error', False),
            sequence = [ruamel_to_action(action, errors) for action in one_action.get('sequence', [])],
            metadata=one_action.get('metadata')
        )
    elif 'parallel' in one_action:
        parallels = []
        for seq in one_action.get('parallel', []):
            parallels.append([ruamel_to_action(action, errors) for action in seq])
        return Parallel_action(
            id = one_action.get('id'),
            alias = one_action.get('alias'),
            enabled = one_action.get('enabled', True),
            continue_on_error = one_action.get('continue_on_error', False),
            parallel = parallels,
            metadata=one_action.get('metadata')
        )
    elif 'stop' in one_action:
        return Stop_action(
            id = one_action.get('id'),
            alias = one_action.get('alias'),
            enabled = one_action.get('enabled', True),
            continue_on_error = one_action.get('continue_on_error', False),
            stop = one_action.get('stop', ''),
            error = one_action.get('error', False),
            metadata=one_action.get('metadata')
        )
    elif 'set_conversation_response' in one_action:
        return Set_conversation_response_action(
            id = one_action.get('id'),
            alias = one_action.get('alias'),
            enabled = one_action.get('enabled', True),
            continue_on_error = one_action.get('continue_on_error', False),
            set_conversation_response = one_action.get('set_conversation_response'),
            metadata=one_action.get('metadata')
        )
    elif 'device_id' in one_action or 'domain' in one_action:
        return Device_action(
            id = one_action.get('id'),
            alias = one_action.get('alias'),
            enabled = one_action.get('enabled', True),
            continue_on_error = one_action.get('continue_on_error', False),
            params = one_action,
            metadata=one_action.get('metadata')
        )
    else:
        return Unknown_action(
            id = one_action.get('id'),
            alias = one_action.get('alias'),
            enabled = one_action.get('enabled', True),
            continue_on_error = one_action.get('continue_on_error', False),
            params = one_action,
            metadata=one_action.get('metadata')
        )