lines = list()
import  csv
lines = list()
# with open("lich_cham_cong.csv", "r") as f:
#     data = list(csv.reader(f))
#     for row in data:
#         lines.append(row)
#     print(len(lines))


with open("lich_cham_cong", "w", newline='') as f:
    writer = csv.writer(f)
    for row in data:
        writer.writerow(row)

