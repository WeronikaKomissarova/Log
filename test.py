from flask import Flask, render_template
from render import RenderFile
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
df=RenderFile(path).file_to_dataframe().to_pickle('uploads\%s.pkl' %'dism.log'.split('.')[0])
