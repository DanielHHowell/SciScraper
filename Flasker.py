from flask import Flask, render_template, flash, request
from wtforms import Form, StringField, IntegerField, RadioField, validators
import Main


DEBUG = True
app = Flask(__name__)

app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'e5ac358c-f0bf-11e5-9e39-d3b532c10a28'

class InputForm(Form):
    topic = StringField('topic:', [validators.required()])
    queries = StringField('queries:')
    nResults = IntegerField('nResults:', [validators.required()])
    sortby = RadioField('Label', choices=[('relevance','Relevance'),('pubdate','Publication Date')])


@app.route("/", methods=['GET', 'POST'])
def index():
    form = InputForm(request.form)


    if request.method == 'POST':
        topic = request.form['topic']
        queries = request.form['queries']
        nResults = request.form['nResults']
        sortby = request.form['sortby']

        if form.validate():
            mainDict, query = Main.sciscraper(topic,queries,nResults,sortby)
            return render_template('/report.html', reportdict=mainDict, searchtitle = query, nResults = nResults)

        else:
            print("testing")
            flash('Error: Check to make sure you have submitted a main topic and number of results to search for~ ')

    return render_template('index.html', form=form, default_results='5')

@app.route("/testing.html")
def testing():
    return render_template('testing.html')

if __name__ == "__main__":
    app.run(debug=True)