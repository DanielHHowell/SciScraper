from flask import Flask, render_template, flash, request
from wtforms import Form, StringField
import Main


DEBUG = True
app = Flask(__name__)



class InputForm(Form):
    topic = StringField('topic:')
    queries = StringField('queries:')
    nResults = StringField('nResults:')


@app.route("/index.html", methods=['GET', 'POST'])
def index():
    form = InputForm(request.form)

    print(form.errors)
    if request.method == 'POST':
        topic = request.form['topic']
        queries = request.form['queries']
        nResults = request.form['nResults']

        if form.validate():
            mainDict, query = Main.sciscraper(topic,queries,nResults,'relevance')
            return render_template('/report.html', reportdict=mainDict, searchtitle = query, nResults = nResults)

        else:
            flash('Error: All the form fields are required. ')

    return render_template('index.html', form=form)

@app.route("/testing.html")
def testing():
    return render_template('testing.html')

@app.route("/testingindex.html")
def testingindex():
    return render_template('testingindex.html')

if __name__ == '__main__':
   app.run(debug = True)