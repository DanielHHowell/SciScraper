from flask import Flask, render_template, flash, request
from wtforms import Form, StringField, validators
import Main


DEBUG = True
app = Flask(__name__)

app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'e5ac358c-f0bf-11e5-9e39-d3b532c10a28'

class InputForm(Form):
    topic = StringField('topic:', [validators.required()])
    queries = StringField('queries:')
    nResults = StringField('nResults:', [validators.required()])


@app.route("/", methods=['GET', 'POST'])
def index():
    form = InputForm(request.form)


    if request.method == 'POST':
        topic = request.form['topic']
        queries = request.form['queries']
        nResults = request.form['nResults']

        if form.validate():
            mainDict, query = Main.sciscraper(topic,queries,nResults,'relevance')
            return render_template('/report.html', reportdict=mainDict, searchtitle = query, nResults = nResults)

        else:
            print("testing")
            flash('Error: Check to make sure you have submitted a main topic and number of results to search for~. ')

    return render_template('index.html', form=form)

@app.route("/testing.html")
def testing():
    return render_template('testing.html')

if __name__ == "__main__":
    app.run(debug=True)