
import pandas as pd
import re
#читает файл по пути  и сохраняет DataFrame из него

class RenderFile():
    def __init__(self, path):
        self.filepath= path

    def file_to_dataframe(self):
        list = []
        timestampPattern = r"[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}, "
        pattern = re.compile(timestampPattern)

        with open(self.filepath, 'r') as file:
            for line in file:
                if re.search(pattern, line):
                    res = line.split(" ", maxsplit=3)
                    res[-1] = res[-1].lstrip()
                    list.append(res)

        dfLog = pd.DataFrame(list)
        dfLog.columns = ['Day', "Time", 'Type', 'Message']
        return dfLog
