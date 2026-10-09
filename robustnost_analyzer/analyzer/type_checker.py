from typing import List, Dict, Any
from classes.classes import (Automation, Trigger, Condition, Action,)
import re

# Main entry point for type validation of all automations
def validate_types(automatoion_ir: List[Automation], errors: List[Dict[str,Any]]):
    for index, auto in enumerate(automatoion_ir):
        alias = auto.alias or f"Automation #{index + 1}"
        for trig in auto.triggers:
            validate_trigger_type(trig, errors, alias, index)
        for cond in auto.conditions:
            validate_condition_type(cond, errors, alias, index)
        validate_action_type(auto.actions, errors, alias, index)

# Check if value is a valid number (int, float, or numeric string)
def is_number(val) -> bool:
    if val is None: 
        return True
    if isinstance(val,(int, float)):
        return True
    if isinstance(val, str):
        try:
            float(val.strip())
            return True
        except ValueError:
            return False
    return False

# Check if value is a valid duration string in format +-HH:MM:SS
def is_duration(val) -> bool:
    if not isinstance(val,str):
        return False
    val = val.strip()
    pattern = r'^[+-]?(\d{1,2}:)?\d{1,2}:\d{1,2}$'
    return bool(re.match(pattern, val))        

# Safely extract 'for' dictionary from trigger/condition/action
def get_for_dict(trig) -> dict:
    if hasattr(trig, 'for_loop') and trig.for_loop:
        return trig.for_loop
    if hasattr(trig, 'params') and isinstance(trig.params, dict):
        return trig.params.get('for') or {}
    return {}

# Safely extract params dictionary from Unknown objects
def get_params(obj) -> dict:
    """Pomocná funkcia na získanie params z Unknown objektov"""
    if hasattr(obj, 'params') and isinstance(obj.params, dict):
        return obj.params
    return {}

# Check if value is a valid time HH:MM:SS or 'sunrise'/'sunset'
def is_time_or_sun(val) -> bool:
    if not isinstance(val, str):
        return False
    val = val.strip().lower()
    if val in {'sunrise', 'sunset'}:
        return True
    return bool(re.match(r'^\d{1,2}:\d{2}(:\d{2})?$', val))

# Validate type correctness for all trigger types (including Unknown_trigger)
def validate_trigger_type(trig: Trigger, errors: List, alias: str, index: int):
    for_dict = get_for_dict(trig)
    for unit in ['hours', 'minutes', 'seconds']:
        val = for_dict.get(unit)
        if val is not None and not is_number(val):
            errors.append({
                'automation_index': index,'alias': alias,'type': 'semantic','rule': 'type_error',
                'message': f"Semantic error: '{unit}' v 'for:' needs to be a number (got {val})"
            })

    params = get_params(trig)
    above = getattr(trig, 'above', None) or params.get('above')
    below = getattr(trig, 'below', None) or params.get('below')

    if above is not None and not is_number(above):
        errors.append({
            'automation_index': index, 'alias': alias, 'type': 'semantic',
            'rule': 'type_error', 'message': f"Semantic error: 'above' needs to be a number"
        })
    if below is not None and not is_number(below):
        errors.append({
            'automation_index': index, 'alias': alias, 'type': 'semantic',
            'rule': 'type_error', 'message': f"Semantic error: 'below' needs to be a number"
        })

    offset = getattr(trig, 'offset', None) or params.get('offset')
    if offset and not is_duration(offset):
        errors.append({
            'automation_index': index,'alias': alias,'type': 'semantic','rule': 'type_error',
            'message': f"Semantic error: 'offset' needs to be in format +-HH:MM:SS (got '{offset}')"
        })

# Validate type correctness for all condition types (including composite)
def validate_condition_type(cond: Condition, errors: List, alias: str, index: int):
    params = get_params(cond)

    above = getattr(cond, 'above', None) or params.get('above')
    below = getattr(cond, 'below', None) or params.get('below')

    if above is not None and not is_number(above):
        errors.append({
            'automation_index': index, 'alias': alias, 'type': 'semantic',
            'rule': 'type_error', 'message': f"Semantic error: 'above' needs to be a number"
        })
    if below is not None and not is_number(below):
        errors.append({
            'automation_index': index, 'alias': alias, 'type': 'semantic',
            'rule': 'type_error', 'message': f"Semantic error: 'below' needs to be a number"
        })

    for field in ['after_offset', 'before_offset']:
        val = getattr(cond, field, None) or params.get(field)
        if val and not is_duration(val):
            errors.append({
                'automation_index': index, 'alias': alias, 'type': 'semantic',
                'rule': 'type_error', 'message': f"Semantic error: '{field}' needs to have format +-HH:MM:SS"
            })

    after = getattr(cond, 'after', None) or params.get('after')
    before = getattr(cond, 'before', None) or params.get('before')

    if after and not is_time_or_sun(after):
        errors.append({
            'automation_index': index, 'alias': alias, 'type': 'semantic',
            'rule': 'type_error', 'message': f"Semantic error: 'after' needs to be time 'HH:MM:SS' or sunrise/sunset"
        })
    if before and not is_time_or_sun(before):
        errors.append({
            'automation_index': index, 'alias': alias, 'type': 'semantic',
            'rule': 'type_error', 'message': f"Semantic error: 'before' needs to be time 'HH:MM:SS' or sunrise/sunset"
        })

    #recursive 
    if hasattr(cond, 'conditions') and cond.conditions:
        for subcond in cond.conditions:
            validate_condition_type(subcond, errors, alias, index)

# Validate type correctness for all actions (including nested actions)
def validate_action_type(actions: List[Action], errors: List, alias: str, index: int):
    for action in actions:
        params = get_params(action)

        service_field = getattr(action, 'service', None) or params.get('service')
        service_check = False
        
        if isinstance(service_field, list) and len(service_field) > 0 and isinstance(service_field[0], dict):
            bad_data = service_field[0]
            timeout = bad_data.get('timeout')
            if timeout and isinstance(timeout, str) and not is_duration(timeout):
                service_check = True
                errors.append({
                    'automation_index': index,'alias': alias,'type': 'semantic','rule': 'type_error',
                    'message': f"Semantic error: 'timeout' need to have a format HH:MM:SS (got '{timeout}')"
                })

        timeout = (getattr(action, 'timeout', None) or 
                  params.get('timeout') or 
                  (service_field[0].get('timeout') if isinstance(service_field, list) and service_field else None))
        
        if timeout and isinstance(timeout, str) and not is_duration(timeout):
            if not service_check:
                errors.append({
                    'automation_index': index,'alias': alias,'type': 'semantic','rule': 'type_error',
                    'message': f"Semantic error: 'timeout' needs to have a format HH:MM:SS (got '{timeout}')"
                })
            else:
                service_check = False
        # delay
        delay = getattr(action, 'delay', None) or params.get('delay')
        if delay:
            if isinstance(delay, dict):
                for_dict = delay
            else:
                for_dict = get_for_dict(action)
            for unit in ['hours', 'minutes', 'seconds']:
                val = for_dict.get(unit)
                if val is not None and not is_number(val):
                    errors.append({
                        'automation_index': index,'alias': alias,'type': 'semantic','rule': 'type_error',
                        'message': f" Semantic error: delay.{unit} needs to be a number"
                    })
            if isinstance(delay, str) and not is_duration(delay):
                errors.append({
                    'automation_index': index, 'alias': alias, 'type': 'semantic',
                    'rule': 'type_error', 'message': f"Semantic error: delay needs to have a format HH:MM:SS"
                })

        data = getattr(action, 'data', None) or params.get('data') or {}
        if isinstance(data, dict):
            numeric_fields = {'brightness_pct', 'transition', 'volume', 'volume_level',
                              'critical', 'brightness', 'percentage', 'level'}
            for field, val in data.items():
                if field in numeric_fields and val is not None and not is_number(val):
                    errors.append({
                        'automation_index': index,'alias': alias,'type': 'semantic','rule': 'type_error',
                        'message': f"Semantic error: Parameter '{field}' in data in action needs to be a number ({val})"
                    })

        #recursive
        for attr_name in ['sequence', 'then', 'else_', 'default', 'actions']:
            nested = getattr(action, attr_name, None) or params.get(attr_name)
            if isinstance(nested, list):
                validate_action_type(nested, errors, alias, index)           