# hello flask project simple
from flask import Flask, render_template, request

app = Flask(__name__)
app.secret_key = 'mysecretkey'


@app.route("/", methods=["GET", "POST"])
def register():
    error = None

    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        email = request.form.get("email")

        if not name or not email:
            error = "Name and Email are required."
        elif not age.isdigit():
            error = "Age must be a number."
        else:
            return render_template(
                "result.html",
                name=name,
                age=age,
                email=email
            )

    return render_template("register.html", error=error)


if __name__ == '__main__':
    app.run(debug=True)
