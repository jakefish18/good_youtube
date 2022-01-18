import datetime

dates = []
day_nums = []
day_num = 0

for i in range(1, 100000 + 1):
    for j in range(1, 12 + 1):
        for d in range(1, 31 + 1):
            try:
                date = datetime.date(i, j, d)
                s_i = str(i)
                if j < 10:
                    s_j = f"0{j}"
                else:
                    s_j = str(j)
                if d < 10:
                    s_d = f"0{d}"
                else:
                    s_d = str(d)
            
                s = s_d + s_j + s_i
            
                day_num += 1

                if len(s) % 2 == 0:
                    f = len(s) // 2
                    if s[0: f] == s[f: len(s)][::-1]:
                        day_nums.append(day_num)
            
                else:
                    f = len(s) // 2
                    if s[0: f + 1] == s[f: len(s)][::-1]:
                        day_nums.append(day_num)
            except:
                pass

print(day_num)
with open('dates.txt', 'w') as file:
    for i in day_nums:
        file.write(f"{i}, ")
