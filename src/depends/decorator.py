from collections.abc import Callable
from functools import wraps
from typing import Any, _AnnotatedAlias, get_type_hints


def inject_dependencies(func: Callable) -> Callable:
    """_summary_

    Args:
        func (Callable): _description_

    Returns:
        Callable: _description_
    """

    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        type_hints = get_type_hints(func, include_extras=True)
        params = {}
        for key in kwargs:
            params[key] = kwargs[key]
            del type_hints[key]

        if len(args) <= len(type_hints):
            for ind, i in enumerate(type_hints):
                if ind >= len(args):
                    break
                params[i] = args[ind]

        for param_name, param in type_hints.items():
            if isinstance(param, _AnnotatedAlias):
                depend_func = param.__metadata__[0]
                try:
                    params[param_name] = await depend_func()
                except TypeError:
                    params[param_name] = depend_func()

        return await func(**params)

    return wrapper
