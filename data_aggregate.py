from pathlib import Path
import csv


data_dir = Path("./result")

date_list = []
d = {}
id2title = {}
for file_ in sorted(data_dir.iterdir(), key=lambda x: x.name, reverse=True):

    date = file_.stem
    date_list.append(date)

    with file_.open('r') as f:
        reader = csv.reader(f, delimiter='\t')
        for record in reader:
            # print(record)
            if record[0] in d:
                d[record[0]].append(record[2])
            else:
                d[record[0]] = [record[2]]
                
                id2title[record[0]] = record[1]

for id_, pv_list in d.items():
    print(id2title[id_], d[id_][::-1])
