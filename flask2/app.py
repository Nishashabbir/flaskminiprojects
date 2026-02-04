from flask import Flask, render_template, request
app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def calculate():
    if request.method == "POST":
        rent=float(request.form.get("rent"))
        food= float(request.form.get("food"))
        people= int(request.form.get("people"))
        units=float(request.form.get("units"))
        charge_per=float(request.form.get("charge_per"))
        electricity_bill= units * charge_per
        total_bill= rent + food + electricity_bill
        per_person= total_bill / people
        return render_template('result.html', electricity_bill=electricity_bill, total_bill=total_bill, per_person=per_person)
    
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)

