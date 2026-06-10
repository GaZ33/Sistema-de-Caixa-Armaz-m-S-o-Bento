from datetime import date, datetime
from decimal import Decimal
from enum import Enum


def serialize_value(value):
    if isinstance(value, Decimal):
        return float(value)

    if isinstance(value, datetime):
        if value.tzinfo is None:
            return value.isoformat() + 'Z'
        return value.isoformat()
    elif isinstance(value, date):
        return value.isoformat()

    if isinstance(value, Enum):
        return value.value

    return value


def model_to_dto(model):
    if model is None:
        return None

    if hasattr(model, 'to_dict'):
        return model.to_dict()

    if hasattr(model, '__table__'):
        return {
            column.name: serialize_value(getattr(model, column.name))
            for column in model.__table__.columns
        }

    return model


def models_to_dtos(models):
    return [model_to_dto(model) for model in models]
