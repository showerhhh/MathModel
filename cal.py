import math

volume = [10.865, 1.936, 2.376, 2.652, 2.64, 1.2]
x_p = [8.9130435, 6.9130435, -1.686957, 3.1130435, -5.286957, -2.086957]
y_p = [1.20652174, -1.39347826, 1.20652174, 0.60652174, -0.29347826, -1.49347826]
z_p = [0.61669004, 0.21669004, -0.28330996, -0.18330996, 0.41669004, 0.21669004]
x_len = [1.5, 2.2, 2.4, 1.7, 2.4, 2.4]
y_len = [0.9, 0.8, 1.1, 1.3, 1.2, 1]
z_len = [0.3, 1.1, 0.9, 1.2, 1, 0.5]


def cal_centroid(flag, v, angle):
    """
    :param flag: 第几个油箱
    :param v: 当前油箱中油的容积
    :param angle: 飞行器当前角度
    :return: (x, y, z)质心位置
    """
    x0 = x_len[flag]
    y0 = y_len[flag]
    z0 = z_len[flag]
    v0 = volume[flag]
    TAN = math.fabs(math.tan(angle))
    if angle == 0:
        return x_p[flag] / 2, y_p[flag] / 2, (v * z0) / (2 * v0) + z_p[flag] / 2 - z0 / 2
    elif angle > 0:
        if TAN < z0 / x0:
            if v < y0 * x0 ** 2 * TAN / 2:
                return math.sqrt((2 * v) / (9 * y0 * TAN)) + x_p[flag] / 2 - x0 / 2, y_p[flag] / 2, math.sqrt(
                    (2 * v * TAN) / (9 * y0)) + z_p[flag] / 2 - z0 / 2
            elif (y0 * x0 ** 2 * TAN) / 2 < v < v0 - (y0 * x0 ** 2 * TAN) / 2:
                return x0 ** 3 * TAN * y0 / (12 * v) + x_p[flag] / 2, y_p[flag] / 2, v / (2 * x0 * y0) + (
                        y0 * x0 ** 3 * TAN ** 2) / (24 * v) + z_p[flag] / 2 - z0 / 2
            else:
                return x0 / 2 + math.sqrt(2 * (v0 - v) ** 3 / (9 * v ** 2)) - x0 * y0 / (2 * v) + x_p[flag] / 2, y_p[
                    flag] / 2, z0 / 2 - v0 * z0 / (2 * v) + TAN * math.sqrt((v0 - v) ** 3 / (9 * v ** 2)) + z_p[
                           flag] / 2
        else:
            if v < y0 * x0 ** 2 / (2 * TAN):
                return math.sqrt((2 * v) / (y0 * TAN * 9)) + x_p[flag] / 2 - x0 / 2, y_p[flag] / 2, math.sqrt(
                    (2 * v * TAN) / (y0 * 9)) + z_p[flag] / 2 - z0 / 2
            elif y0 * x0 ** 2 / (2 * TAN) < v < v0 - (y0 * z0 ** 2) / (2 * TAN):
                return v / (2 * z0 * y0) + (y0 * z0 ** 3) / (24 * TAN ** 2) + x_p[flag] / 2 - x0 / 2, y_p[flag] / 2, (
                        z0 ** 3 * y0) / (12 * v * TAN) + z_p[flag] / 2
            else:
                return x0 / 2 - (v0 * x0) / (2 * v) + TAN * math.sqrt((v0 - v) ** 3) / (3 * v) + x_p[flag] / 2, y_p[
                    flag] / 2, z0 / 2 + math.sqrt((v0 - v) ** 3) / (3 * v) + z_p[flag] / 2
    else:
        angle = -angle
        if TAN < z0 / x0:
            if v < y0 * x0 ** 2 * TAN / 2:
                return x0 / 2 - 1 * math.sqrt((2 * v) / (9 * y0 * TAN)) + x_p[flag] / 2, y_p[flag] / 2, math.sqrt(
                    (2 * v * TAN) / (9 * y0)) + z_p[flag] / 2 - z0 / 2
            elif (y0 * x0 ** 2 * TAN) / 2 < v < v0 - (y0 * x0 ** 2 * TAN) / 2:
                return -1 * x0 + x0 ** 3 * TAN * y0 / (12 * v) + x_p[flag] / 2, y_p[flag] / 2, v / (2 * x0 * y0) + (
                        y0 * x0 ** 3 * TAN ** 2) / (24 * v) + z_p[flag] / 2 - v0 / 2
            else:
                return -1 * math.sqrt(2 * (v0 - v) ** 3 / (9 * v ** 2)) + x0 * y0 / (2 * v) + x_p[flag] / 2 - x0 / 2, \
                       y_p[flag] / 2, z0 / 2 - v0 * z0 / (2 * v) + TAN * math.sqrt((v0 - v) ** 3 / (9 * v ** 2)) + z_p[
                           flag] / 2
        else:
            if v < y0 * x0 ** 2 / (2 * TAN):
                return x0 / 2 - math.sqrt((2 * v) / (y0 * TAN * 9)) + x_p[flag] / 2, y_p[flag] / 2, math.sqrt(
                    (2 * v * TAN) / (y0 * 9)) + z_p[flag] / 2 - z0 / 2
            elif y0 * x0 ** 2 / (2 * TAN) < v < v0 - (y0 * z0 ** 2) / (2 * TAN):
                return x0 / 2 - v / (2 * z0 * y0) - (y0 * z0 ** 3) / (24 * TAN ** 2) + x_p[flag] / 2, y_p[flag] / 2, - (
                        z0 ** 3 * y0) / (12 * v * TAN) + z_p[flag] / 2
            else:
                return (v0 * x0) / (2 * v) - TAN * math.sqrt((v0 - v) ** 3) / (3 * v) + x_p[flag] / 2 - x0 / 2, y_p[
                    flag] / 2, z0 / 2 + math.sqrt((v0 - v) ** 3) / (3 * v) + z_p[flag] / 2


if __name__ == '__main__':
    print(cal_centroid(0, 0.3, 0.00046845))
