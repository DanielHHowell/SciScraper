from flask import Flask, render_template, flash, request
from wtforms import Form, StringField, IntegerField, RadioField, validators
import Main

app = Flask(__name__)

app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'e5ac358c-f0bf-11e5-9e39-d3b532c10a28'


class InputForm(Form):
    topic = StringField('topic:', [validators.required()])
    queries = StringField('queries:')
    nResults = IntegerField('nResults:', [validators.required()])
    sortby = RadioField('Label',
                        choices=[('relevance', 'Relevance'), ('pubdate', 'Publication Date (low relevance warning)')],
                        default='relevance')


@app.route("/", methods=['GET', 'POST'])
def index():

    # If args were submitted right in the URL, sends straight to the Main.py report
    if request.args.get('topic'):
        topic = request.args.get('topic')
        queries = request.args.get('queries')
        nResults = request.args.get('nResults')
        sortby = request.args.get('sortby')

        mainDict, query, keywords = Main.sciscraper(topic, queries, nResults, sortby)
        return render_template('/report.html', reportdict=mainDict, searchtitle=query, nResults=nResults,
                               keywords=", ".join(keywords))

    # If not, uses the form POST request from index.html
    else:

        form = InputForm(request.form)
        if request.method == 'POST':
            topic = request.form['topic']
            queries = request.form['queries']
            nResults = request.form['nResults']
            sortby = request.form['sortby']

            if form.validate():
                mainDict, query, keywords = Main.sciscraper(topic, queries, nResults, sortby)
                keyword_links = ['https://www.google.com/search?q=' + i.replace(" ","+") for i in keywords]
                key_tuples = zip(keywords,keyword_links)
                return render_template('/report.html', reportdict=mainDict, searchtitle=query, nResults=nResults,
                                       key_tuples=key_tuples)

            else:
                flash('Error: Check to make sure you have submitted a main topic and number of results to search for~ ')

        return render_template('index.html', form=form, default_results='5')


@app.route("/testing.html")
def testing():
    return render_template('testing.html')


if __name__ == "__main__":
    app.run(threaded=True)
