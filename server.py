from flask import Flask, render_template, redirect, request, flash
from mysqlconnection import connectToMySQL

app = Flask(__name__)
app.secret_key = 'keep it a secret'


@app.route('/')
def main():
    mySql = connectToMySQL('dojo_survey')
    lang = mySql.query_db('select * from languages')
    mySql = connectToMySQL('dojo_survey')
    loc = mySql.query_db('select * from locations')
    return render_template('index.html', lang=lang, locations=loc)


@app.route('/process', methods=['POST'])
def process():
    print('*'*50)
    print(request.form)
    print('*'*50)
    is_valid = True
    if len(request.form['name']) < 1:
        is_valid = False
        flash("Please enter in your name")
        # display validation error
    if 'location' not in request.form or int(request.form['location']) < 1:
        is_valid = False
        flash("Please select your location")
    if 'language' not in request.form or int(request.form['language']) < 1:
        is_valid = False
        flash("Please select your favorite computer language")
        # display validation error
    if 'comments' in request.form and len(request.form['comments']) > 120:
        is_valid = False
        flash({'comment': "Your comment is too long, do not exceed 120 characters"})

    if is_valid:
        mySql = connectToMySQL('dojo_survey')
        query = 'INSERT INTO surveys (name, location_id, language_id, comments, created_on, updated_on) VALUES(%(na)s, %(loc)s, %(lang)s, %(com)s, now(), now())'
        data = {'na': request.form['name'], 'loc':  request.form['location'],
                'lang': request.form['language'], 'com': request.form['comments']}
        mySql.query_db(query, data)
        flash("Sucess! Your survey was recorded.")
        return redirect('/results')
    else:
        return redirect('/')


@app.route('/results')
def results():
    mySql = connectToMySQL('dojo_survey')
    query = 'SELECT surveys.name as "name", locations.name as "location", languages.name as "language", comments FROM surveys ' +\
        'LEFT JOIN locations ON surveys.location_id = locations.id ' +\
        'LEFT JOIN languages ON surveys.language_id = languages.id ' +\
        'ORDER BY surveys.id DESC ' +\
        'LIMIT 1'
    results = mySql.query_db(query)
    print(results)
    return render_template('results.html', results=results[0])


if __name__ == '__main__':
    app.run(debug=True)
