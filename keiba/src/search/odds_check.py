import collections

from tqdm import tqdm
with open("../../data/race_result.txt") as f:
    allrace_list = [s.strip() for s in f.readlines()]

tansyou_list = []
hukusyou_list = []
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
        # print(race, event_date, event_venue)
        
        odds = [[float(v), i+1] for i, v in enumerate(race[3]) if v!="-"]
        
        odds_sorted = sorted(odds)
        ninki = [i for _, i in odds_sorted]
        
        try:
            tansyou_list.append(ninki.index(tansyou_win)+1)
            hukusyou_list.extend([ninki.index(i)+1 for i in hukusyou_win[:2]])
        except ValueError:
            ee += 1

print(len(tansyou_list))
t = collections.Counter(map(str, tansyou_list))
A = []
for k, v in t.items():
    A.append([int(k), 100*v/sum(t.values())])
for a in sorted(A):
    print(a)
print()
B = []
h = collections.Counter(map(str, hukusyou_list))
for k, v in h.items():
    B.append([int(k), 100*v/sum(t.values())])
for b in sorted(B):
    print(b)