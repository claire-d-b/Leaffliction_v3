#!/usr/bin/env python3

def minimize_cost(m: int, theta_0: float, theta_1: float, real_score: float,
                  real_house: float, learning_rate: float) -> tuple:
    """Test with a slope value between -0.01 and 0.01, update y-interceipt
    value, take the smallest square error and return corresponding w and b"""
    limit = float("inf")
    w = 0.0
    b = 0.0

    minimum = int(- 1 / learning_rate)
    maximum = int(1 / learning_rate)

    for i in range(minimum, maximum, 1):
        theta_1 = float(i / ((2 * m) / learning_rate))

        # real_house = theta_1 * real_score + theta_0
        # real_house - theta_0 = theta_1 * real_score
        # -theta_0 = theta_1 * real_score - real_house
        # theta_0 = -(theta_1 * real_score - real_house)
        theta_0 = -theta_1 * real_score + real_house
        se = ((theta_1 * real_score + theta_0) -
              real_house) ** 2
        # print("square error", se)

        if se < limit:

            limit = se
            b = theta_0
            w = theta_1

    return b, w, limit
