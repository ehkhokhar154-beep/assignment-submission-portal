import re
from flask import Flask, render_template, request

app = Flask(__name__)
submissions = []

URL_REGEX = re.compile(
    r'^(?:http|ftp)s?://'
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
    r'localhost|'
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    r'(?::\d+)?'
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        reg_num = request.form.get('reg_num', '').strip()
        title = request.form.get('title', '').strip()
        url = request.form.get('url', '').strip()

        if not name or not reg_num or not title or not url:
            error = "All fields are required, including Registration Number."
        elif not URL_REGEX.match(url):
            error = "Invalid submission URL format."
        else:
            submissions.append({
                'name': name,
                'reg_num': reg_num,
                'title': title,
                'url': url
            })

    return render_template('index.html', submissions=submissions, error=error)

if __name__ == '__main__':
    app.run(debug=True, port=5000)