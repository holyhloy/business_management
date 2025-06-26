from typing import Optional
from urllib.parse import urlparse

from fastapi.requests import Request
from fastapi.responses import Response


def cache_key_builder(
    func,
    namespace: Optional[str] = "",
    request: Request = None,
    response: Response = None,
    *args,
    **kwargs,
) -> str:
    """
    Creates a key for a cache note in Redis, making it unique.
    Solves an adding a note in Redis when it already exists problem.

    :param func: function to wrap
    :param namespace: a name for a note in Redis
    :param request: request object
    :param response: response object
    :param args: unnamed args of the wrapped function
    :param kwargs: keyword args of the wrapped function

    :return: string cache key used for name a note in Redis
    """
    kwargs_copy = kwargs.copy()
    kwargs_copy["kwargs"].pop("session", None)
    if request:
        parsed = urlparse(str(request.url))
        cache_key = f"{namespace}:{func.__module__}:{func.__name__}:{parsed.path}:{args}:{kwargs_copy}"
    else:
        cache_key = f"{namespace}:{func.__module__}:{func.__name__}:{args}:{kwargs_copy}"  # pragma: no cover
    return cache_key
