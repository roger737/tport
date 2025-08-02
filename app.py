from flask import Flask, render_template_string
from labs import register_all, get_lab_info

app = Flask(__name__)
app.secret_key = 'dev'

register_all(app)


@app.route('/')
def index():
    labs = get_lab_info()
    template = """
    <h1>Vulnerability Labs</h1>
    <ul>
    {% for lab in labs %}
      <li><a href="{{ lab.path }}">{{ lab.name }}</a> ({{ lab.difficulty }}) - {{ lab.description }}</li>
    {% endfor %}
    </ul>
    """
    return render_template_string(template, labs=labs)


if __name__ == '__main__':
    app.run(debug=True)
