def rate_limit(limit: int, key=None):

    def wrapper(func):
        setattr(func, 'throttling_rate_limit', limit)
        if key:
            setattr(func, 'throttling_key', key)
        return func

    return wrapper
