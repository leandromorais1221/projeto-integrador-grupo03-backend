from functools import wraps
from typing import Type
from flask import request, jsonify
from pydantic import BaseModel, ValidationError


def validate_query(model: Type[BaseModel]):
    def wrapped_view(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            try:
                params = model.model_validate(
                    request.args.to_dict()
                )

            except ValidationError as e:
                return jsonify({
                    "validation_error": {
                        "query_params": e.errors()
                    }
                }), 400

            return func(*args, query=params, **kwargs)

        return func_wrapper
    return wrapped_view