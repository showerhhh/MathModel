import numpy as np
from gurobipy import *
from pandas import read_excel

df1 = read_excel('附件3-问题2数据.xlsx', sheet_name='发动机耗油速度', header=None)
request = np.array(np.array(df1)[94:4774, 1], dtype=float)
df2 = read_excel('附件3-问题2数据.xlsx', sheet_name='飞行器理想质心数据', header=None)
ideal_centroid = np.array(np.array(df2)[94:4774:, 1:], dtype=float)
M = 3000
rou = 850
volume = [10.865, 1.936, 2.376, 2.652, 2.64, 1.2]
x_p = [8.9130435, 6.9130435, -1.686957, 3.1130435, -5.286957, -2.086957]
y_p = [1.20652174, -1.39347826, 1.20652174, 0.60652174, -0.29347826, -1.49347826]
z_p = [0.61669004, 0.21669004, -0.28330996, -0.18330996, 0.41669004, 0.21669004]
x_len = [1.5, 2.2, 2.4, 1.7, 2.4, 2.4]
y_len = [0.9, 0.8, 1.1, 1.3, 1.2, 1]
z_len = [0.3, 1.1, 0.9, 1.2, 1, 0.5]
total = np.zeros(4680)
total[0] = request[0]
for i in range(1, 4680):
    total[i] = total[i - 1] + request[i]

model = Model("question")
k = model.addVars(4680, 6, vtype=GRB.BINARY, name='k')  # 某一时刻，某油箱是否加油
s = model.addVars(4680, 6, vtype=GRB.CONTINUOUS, name='s')  # 某一时刻，某油箱的加油速度
c = model.addVars(4680, 3, vtype=GRB.CONTINUOUS, name='c')  # 某一时刻，某油箱内油的质心位置
v = model.addVars(4680, 6, vtype=GRB.CONTINUOUS, name='v')  # 某一时刻，某油箱内油的体积
z = model.addVar(vtype=GRB.CONTINUOUS, name='z')
item_obj = model.addVars(7200, 3, vtype=GRB.CONTINUOUS, name='item_obj')
v_condition = model.addVars(7200, 2, vtype=GRB.CONTINUOUS, name='v_condition')

model.setObjective(z, GRB.MINIMIZE)
model.addConstrs(z >= item_obj[i, 0] + item_obj[i, 1] + item_obj[i, 2] for i in range(7200))

model.addConstr(v[0, 0] == 0.3)
model.addConstr(v[0, 1] == 1.5)
model.addConstr(v[0, 2] == 2.1)
model.addConstr(v[0, 3] == 1.9)
model.addConstr(v[0, 4] == 2.6)
model.addConstr(v[0, 5] == 0.8)

model.addConstrs(v[i, 0] == v[i - 1, 0] - (s[i - 1, 0] + s[i, 0]) / 2 * k[i - 1, 0] for i in range(1, 4680))
model.addConstrs(
    v_condition[i, 0] == v[i - 1, 1] - (s[i - 1, 1] + s[i, 1]) / 2 * k[i - 1, 1] + s[i - 1, 0] * k[i - 1, 0] for i in
    range(1, 4680))
model.addConstrs(v[i, 2] == v[i - 1, 2] - (s[i - 1, 2] + s[i, 2]) / 2 * k[i - 1, 2] for i in range(1, 4680))
model.addConstrs(v[i, 3] == v[i - 1, 3] - (s[i - 1, 3] + s[i, 3]) / 2 * k[i - 1, 3] for i in range(1, 4680))
model.addConstrs(
    v_condition[i, 1] == v[i - 1, 4] - (s[i - 1, 4] + s[i, 4]) / 2 * k[i - 1, 4] + (s[i - 1, 5] + s[i, 5]) / 2 * k[
        i - 1, 5] for i in range(1, 4680))
model.addConstrs(v[i, 1] == min_(v_condition[i, 0], 1.98) for i in range(1, 4680))
model.addConstrs(v[i, 4] == min_(v_condition[i, 0], 1.98) for i in range(1, 4680))
model.addConstrs(v[i, 5] == v[i - 1, 5] - (s[i - 1, 5] + s[i, 5]) * k[i - 1, 5] for i in range(1, 4680))
model.addConstrs(s[i, j] <= v[i, j] for i in range(4680) for j in range(6))
model.addConstrs(
    (s[i - 1, 1] + s[i, 1]) / 2 * k[i, 1] + (s[i - 1, 1] + s[i, 1]) / 2 * k[i, 2] + (s[i - 1, 3] + s[i, 3]) / 2 * k[
        i, 3] + (s[i - 1, 4] + s[i, 4]) / 2 * k[i, 4] * rou >= request[i] for i in range(1, 4680))
# model.addConstrs(v[i, j] >= 0 for i in range(4680) for j in range(6))

model.addConstrs(s[i, 0] * k[i, 0] <= 1.1 / rou for i in range(4680))
model.addConstrs(s[i, 1] * k[i, 1] <= 1.8 / rou for i in range(4680))
model.addConstrs(s[i, 2] * k[i, 2] <= 1.7 / rou for i in range(4680))
model.addConstrs(s[i, 3] * k[i, 3] <= 1.5 / rou for i in range(4680))
model.addConstrs(s[i, 4] * k[i, 4] <= 1.6 / rou for i in range(4680))
model.addConstrs(s[i, 5] * k[i, 5] <= 1.1 / rou for i in range(4680))
# model.addConstrs(s[i, j] - k[i, j]*2<=0 for i in range(4680) for j in range(6))
# model.addConstrs(s[i, j] + k[i, j]>=0 for i in range(4680) for j in range(6))

# model.addConstrs((s[i, j] == 0) >> (k[i, j] == 0) for i in range(4680) for j in range(6))
# model.addConstrs((k[i, j] == 0) >> (s[i, j] == 0) for i in range(4680) for j in range(6))
# model.addConstrs((k[i-1, j] and k[i, j]) >> (k[i+m, j] == 1 for m in range(60)) for i in range(2, 7140) for j in range(6))
for i in range(1, 4620):
    for j in range(6):
        for m in range(1, 60):
            model.addConstr(k[i + m, j] >= k[i - 1, j] - k[i, j])

for i in range(4680):
    model.addGenConstrPow(item_obj[i, 0], c[i, 0], 2)

for i in range(4680):
    model.addGenConstrPow(item_obj[i, 1], c[i, 1], 2)

for i in range(4680):
    model.addGenConstrPow(item_obj[i, 2], c[i, 2], 2)

'''for i in range(4680):
    model.addConstr(c[i, 0]+ideal_centroid[i, 0] == (rou * (v[i, 0]*x_p[0]+v[i,1]*x_p[1]+v[i,2]*x_p[2]+v[i,3]*x_p[3]+v[i,4]*x_p[4]+v[i,5]*x_p[5])) / (10826-total[i]))
    model.addConstr(c[i, 1]+ideal_centroid[i, 1] == (rou * (v[i, 0]*y_p[0]+v[i,1]*y_p[1]+v[i,2]*y_p[2]+v[i,3]*y_p[3]+v[i,4]*y_p[4]+v[i,5]*y_p[5])) / (10826-total[i]))
    model.addConstr(c[i, 2]+ideal_centroid[i, 2] == (rou * (v[i, 0]*z_p[0]*v[i,0]/volume[0]+v[i,1]*z_p[1]*v[i,1]/volume[1]+v[i,2]*z_p[2]*v[i,2]/volume[2]+v[i,3]*z_p[3]*v[i,3]/volume[3]+v[i,4]*z_p[4]*v[i,4]/volume[4]+v[i,5]*z_p[5]*v[i,5]/volume[5])) / (10826-total[i]))'''
for i in range(4680):
    model.addConstr(c[i, 0] + ideal_centroid[i, 0] == (rou * (
            v[i, 0] * x_p[0] + v[i, 1] * x_p[1] + v[i, 2] * x_p[2] + v[i, 3] * x_p[3] + v[i, 4] * x_p[4] + v[i, 5] *
            x_p[5])) / (10826 - total[i]))
    model.addConstr(c[i, 1] + ideal_centroid[i, 1] == (rou * (
            v[i, 0] * y_p[0] + v[i, 1] * y_p[1] + v[i, 2] * y_p[2] + v[i, 3] * y_p[3] + v[i, 4] * y_p[4] + v[i, 5] *
            y_p[5])) / (10826 - total[i]))
    model.addConstr(c[i, 2] + ideal_centroid[i, 2] == (rou * (
            v[i, 0] * z_p[0] + v[i, 1] * z_p[1] + v[i, 2] * z_p[2] + v[i, 3] * z_p[3] + v[i, 4] * z_p[4] + v[i, 5] *
            z_p[5])) / (10826 - total[i]))
model.write("question1.lp")
# model.setParam("NonConvex", 2)
model.update()
model.optimize()
print(model.status)
print(model.ObjVal)
sx = model.getAttr('x', s)
data1 = open('s.txt', 'w+')
for i in range(4680):
    for j in range(6):
        print(sx[(i, j)], file=data1)
    print('\n', file=data1)

kx = model.getAttr('x', k)
data2 = open('k.txt')
for i in range(4680):
    for j in range(6):
        print(kx[(i, j)], file=data1)
    print('\n', file=data2)
