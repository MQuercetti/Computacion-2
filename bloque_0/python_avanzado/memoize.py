"""Decorador de memoización manual con estadísticas y limpieza."""

from __future__ import annotations

from collections import namedtuple
from functools import wraps


CacheInfo = namedtuple("CacheInfo", "hits misses size")
KW_MARKER = object()


def _make_key(args, kwargs):
    if not kwargs:
        return args
    return args + (KW_MARKER,) + tuple(sorted(kwargs.items()))


def memoize(funcion):
    """Cachea resultados por argumentos posicionales y keyword."""
    cache = {}
    hits = 0
    misses = 0

    @wraps(funcion)
    def wrapper(*args, **kwargs):
        nonlocal hits, misses
        key = _make_key(args, kwargs)
        if key in cache:
            hits += 1
            return cache[key]
        misses += 1
        resultado = funcion(*args, **kwargs)
        cache[key] = resultado
        return resultado

    def cache_info():
        return CacheInfo(hits=hits, misses=misses, size=len(cache))

    def clear_cache():
        nonlocal hits, misses
        cache.clear()
        hits = 0
        misses = 0

    wrapper.cache = cache
    wrapper.cache_info = cache_info
    wrapper.clear_cache = clear_cache
    return wrapper


if __name__ == "__main__":
    @memoize
    def fibonacci(n):
        if n < 2:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)

    print(fibonacci(10))
    print(fibonacci.cache_info())
