import os

HONEY_FIRST_TRY = 5
HONEY_AFTER_HINT = 3
HONEY_REVEALED = 0
NORMAL_CAP = 50
DEMO_CAP = 15


def daily_cap():
    if os.getenv("PERCEPTRON_DEMO") == "1":
        return DEMO_CAP
    return NORMAL_CAP
