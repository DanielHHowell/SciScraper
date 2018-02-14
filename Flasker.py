from flask import Flask, render_template, flash, request
from wtforms import Form, validators, StringField, SubmitField
import Main

# App config.
DEBUG = True
app = Flask(__name__)
#app.config.from_object(__name__)
#app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


class InputForm(Form):
    topic = StringField('Name:')
    queries = StringField('Email:')
    nResults = StringField('Password:')


@app.route("/index.html", methods=['GET', 'POST'])
def index():
    form = InputForm(request.form)

    print(form.errors)
    if request.method == 'POST':
        topic = request.form['topic']
        queries = request.form['queries']
        nResults = request.form['nResults']

        if form.validate():
            resultdict = Main.sciscraper(topic,queries,nResults)
            return render_template('/report.html', reportdict=resultdict)

        else:
            flash('Error: All the form fields are required. ')

    return render_template('index.html', form=form)

if __name__ == '__main__':
   app.run(debug = True)