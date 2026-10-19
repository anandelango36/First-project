from flask import Flask, request

app = Flask(__name__)

PAGE = """
<h1>Hello from Python on localhost!</h1>
<form method="post">
    <input name="name" placeholder="Enter your name">
    <button type="submit">Greet me</button>
</form>
<p>{message}</p>
<a href="/about">About</a>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    message = ""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if name:
            message = f"Welcome, {name}!"
    return PAGE.format(message=message)


@app.route("/about")
def about():
    return "<h2>This is my first Flask app.</h2><a href='/'>Back</a>"


if __name__ == "__main__":
    app.run(debug=True)