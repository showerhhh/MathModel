import copy
import pandas as pd

from cal import cal_centroid

M = 3000


def func1():
    m_nowi = [0.3 * 850, 1.5 * 850, 2.1 * 850, 1.9 * 850, 2.6 * 850, 0.8 * 850]
    cost_ti = pd.read_excel("附件2-问题1数据.xlsx", sheet_name="油箱供油曲线")
    m_ti = []  # 在t时刻下i油箱中油的质量

    for index, row in cost_ti.iterrows():
        cost_nowi = list(row[1:7])
        temp = []
        for k in range(6):
            temp.append(m_nowi[k] - cost_nowi[k])
        m_nowi = copy.deepcopy(temp)
        m_ti.append(copy.deepcopy(temp))

    angle_t = pd.read_excel("附件2-问题1数据.xlsx", sheet_name="飞行器俯仰角")
    angle_t = list(angle_t["飞行器俯仰角(度)"])  # t时刻下飞行器俯仰角
    return m_ti, angle_t


def func2():
    m_ti, angle_t = func1()
    centroid_ti = []  # 在t时刻下i油箱中油的质心位置(x, y, z)
    for now in range(7200):
        m_nowi = m_ti[now]
        angle_now = angle_t[now]
        centroid_nowi = []
        for i in range(6):
            centroid_nowi.append(cal_centroid(i, m_nowi[i] / 850, angle_now))
        centroid_ti.append(copy.deepcopy(centroid_nowi))
    return centroid_ti


def func3():
    m_ti, _ = func1()
    centroid_ti = func2()
    result_centroid_t = []  # 在t时刻下飞行器质心位置[x, y, z]
    for now in range(7200):
        centroid_nowi = centroid_ti[now]
        m_nowi = m_ti[now]

        X_fenzi = 0
        X_fenmu = M
        for i in range(6):
            X_fenzi += centroid_nowi[i][0] * m_nowi[i]
            X_fenmu += m_nowi[i]
        X = X_fenzi / X_fenmu

        Y_fenzi = 0
        Y_fenmu = M
        for i in range(6):
            Y_fenzi += centroid_nowi[i][1] * m_nowi[i]
            Y_fenmu += m_nowi[i]
        Y = Y_fenzi / Y_fenmu

        Z_fenzi = 0
        Z_fenmu = M
        for i in range(6):
            Z_fenzi += centroid_nowi[i][2] * m_nowi[i]
            Z_fenmu += m_nowi[i]
        Z = Z_fenzi / Z_fenmu
        result_centroid_t.append([X, Y, Z])

    return result_centroid_t


def func4():
    """
    将func3的结果写入excel
    :return:
    """
    df = pd.DataFrame(columns=('时间(s)', '质心x坐标', '质心y坐标', '质心z坐标'))
    result_centroid_t = func3()
    for i in range(len(result_centroid_t)):
        result_centroid_t[i].insert(0, i + 1)
        df.loc[i, :] = result_centroid_t[i]
    df.to_excel("测试.xlsx", sheet_name="第一问结果")


if __name__ == '__main__':
    func4()
