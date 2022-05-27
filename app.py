from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import DataRequired
from data import GENRES
from modules import get_genre, eval_model
from werkzeug.utils import secure_filename


app = Flask(__name__)

app.config['SECRET_KEY'] = 'audioclassificationkey@#'

Bootstrap(app)


class UploadForm(FlaskForm):
    file = FileField('Upload an audio file i.e xyz.wav', validators=[DataRequired()])
    submit = SubmitField('Predict')

# Routes

@app.route('/', methods=['GET', 'POST'])
def index():
    form = UploadForm()
    
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        form.file.data.save('uploads/' + filename)
        id = eval_model(filename)

        return redirect(url_for('genre', id=id))

    return render_template('index.html', form=form)


@app.route('/genre/<id>')
def genre(id):
    id, name, desc = get_genre(GENRES, id)
    return render_template('genre.html', id=id, name=name, desc=desc)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)