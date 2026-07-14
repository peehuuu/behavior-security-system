# app/services/validation.py
from marshmallow import Schema, fields, validate, ValidationError

class SessionSchema(Schema):
    wpm = fields.Float(required=True, validate=validate.Range(min=0, max=400))
    avg_dwell = fields.Float(required=True, validate=validate.Range(min=0, max=5))
    avg_flight = fields.Float(required=True, validate=validate.Range(min=0, max=5))
    std_dwell = fields.Float(required=True, validate=validate.Range(min=0, max=5))
    std_flight = fields.Float(required=True, validate=validate.Range(min=0, max=5))
    backspace_rate = fields.Float(load_default=0, validate=validate.Range(min=0, max=1))
    longest_pause = fields.Float(load_default=0, validate=validate.Range(min=0, max=30))
    source = fields.Str(load_default="live", validate=validate.OneOf(["live", "simulated", "baseline"]))
    true_label = fields.Str(load_default=None, allow_none=True, validate=validate.OneOf(["legitimate", "attack", None]))

session_schema = SessionSchema()


def validate_session_payload(json_data):
    try:
        return session_schema.load(json_data or {}), None
    except ValidationError as err:
        return None, err.messages