MAX_HALF_SCORE = 20 * 60


def getMultiplier(seconds: float) -> float:
    if seconds <= 15 * 60:
        return 1

    elif seconds <= MAX_HALF_SCORE:
        return 0.5

    return 0
