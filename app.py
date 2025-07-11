from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Handle uploaded image or model (placeholder)
        image = request.files.get('image')
        model = request.files.get('model')
        # Process and return result
        return render_template('index.html', prediction="Bird", time="23ms")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
