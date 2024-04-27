import collections
import matplotlib.pyplot as plt

from tqdm import tqdm
with open("../../data/race_result.txt") as f:
    allrace_list = [s.strip() for s in f.readlines()]

return_money_list = []

e = 0
ee = 0
for race_list in tqdm(allrace_list):
    try:
        race_list = eval(race_list)
    except TypeError:
        e += 1
        continue
    event_date, event_venue, race_data_list = race_list[0], race_list[1], race_list[2:]
    race_data_list = race_data_list[0]
    for race in race_data_list:
        race_name = race[0]
        try:
            tansyou_win = int(race[1][0])
            hukusyou_win = [int(i) for i in race[2]]
        except ValueError:
            continue
        
        try:
            return_money_list.append(float(race[3][tansyou_win-1]))
        except IndexError:
            continue


return_money_list = sorted(return_money_list)
return_money_dict = {1: 0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0}
for i, v in collections.Counter(return_money_list).items():
    if int(i) <= 10:
        return_money_dict[int(i)] += v
    else:
        return_money_dict[11] += v
print(return_money_dict)
print("1倍", return_money_dict[1]/sum(return_money_dict.values()))
print("2倍", return_money_dict[2]/sum(return_money_dict.values()))
print("3倍", return_money_dict[3]/sum(return_money_dict.values()))
print("4倍", return_money_dict[4]/sum(return_money_dict.values()))
print("5倍", return_money_dict[5]/sum(return_money_dict.values()))
print("6倍", return_money_dict[6]/sum(return_money_dict.values()))
print("7倍", return_money_dict[7]/sum(return_money_dict.values()))
print("8倍", return_money_dict[8]/sum(return_money_dict.values()))
print("9倍", return_money_dict[9]/sum(return_money_dict.values()))
print("10倍", return_money_dict[10]/sum(return_money_dict.values()))
print("10倍以上", return_money_dict[11]/sum(return_money_dict.values()))
print((return_money_dict[1] + return_money_dict[2] + return_money_dict[3])/sum(return_money_dict.values()))