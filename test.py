from flask import Flask, render_template
import pandas as pd
from render import RenderFile
import datetime
#app =  Flask(__name__)
path=r'C:\Windows\Logs\DISM\DISM.log'
"""@app.route('/')
def index():
    df=RenderFile(path)
    DF=df.file_to_dataframe()
    return render_template(DF.to_html('download.html'))
if __name__=='__main__':
    app.run()
"""
df=RenderFile(path).file_to_dataframe()
"""
list=['', '']
timeline=['2020-05-11','2020-05-15']
print(len(list))
dd=df.loc[df['Type'].isin(list)]
dk=df.iloc[ df[df.Day == timeline[0]]: df[df.Day == timeline[1]]]
df['Day'][0]='2020-05-11'
df['Day']=pd.to_datetime(df['Day'])
dk=df[(df.Day >= (timeline[0])) & (df.Day <=(timeline[1]))]
print(dk)
"""
str='logging'
dk=df[df['Message'].str.contains(str, regex=False)]
dk.to_html()
