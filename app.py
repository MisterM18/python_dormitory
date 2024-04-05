from flask import Flask, render_template, session

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Set a secret key for session management

@app.route('/')
def index():
    if 'id' not in session:
        return render_template('index.html', logged_in=False)
    else:
        return render_template('index.html', logged_in=True, username=session['username'])

if __name__ == '__main__':
    app.run(debug=True)
