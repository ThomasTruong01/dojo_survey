from flask import Flask, render_template, redirect, Flash

app = Flask(__name__)
app.secret_key = 'keep it a secret'

if __name__ == '__main__':
    app.run(debug=True)
