import pandas as pd
import re

path=r'C:\Windows\Logs\DISM\DISM.log'

timestampPattern = r"[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}, "
pattern = re.compile(timestampPattern)
list=[]

with open(path, 'r') as file:
    for line in file:
        if re.search(pattern, line):
            res = line.split(" ", maxsplit=3)
            res[-1] = res[-1].lstrip()
            list.append(res)

dfLog = pd.DataFrame(list)
dfLog.columns = ['Day', "Time", 'Type', 'Message']
print(dfLog)
