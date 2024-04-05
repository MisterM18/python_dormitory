from flask import Flask, render_template

app = Flask(__name__)

# Function to generate navigation bar HTML
def generate_navbar():
    return '''
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <a class="navbar-brand" href="#">My Website</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item active">
            <a class="nav-link" href="/">Home</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/about">About</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/contact">Contact</a>
          </li>
        </ul>
      </div>
    </nav>
    '''

@app.route('/')
def index():
    navbar = generate_navbar()
    return render_template('index.html', navbar=navbar)

@app.route('/about')
def about():
    navbar = generate_navbar()
    return render_template('about.html', navbar=navbar)

@app.route('/contact')
def contact():
    navbar = generate_navbar()
    return render_template('contact.html', navbar=navbar)

if __name__ == '__main__':
    app.run(debug=True)
