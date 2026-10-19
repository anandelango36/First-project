from flask import Flask, render_template_string, request

app = Flask(__name__)

PETROL_CO2_PER_LITRE = 2.31   # kg CO2 per litre of petrol
GRID_CO2_PER_KWH = 0.71       # kg CO2 per kWh (approx. grid average)

DEFAULTS = {
    "km_per_day": 40,
    "years": 8,
    "petrol_price": 105,
    "electricity_price": 8,
    "petrol_car_price": 1000000,
    "ev_price": 1500000,
    "petrol_mileage": 18,
    "ev_efficiency": 6,
    "petrol_maint": 0.8,
    "ev_maint": 0.3,
}


def read_inputs(form):
    """Read numbers from the form. Use defaults for anything missing."""
    values = {}
    for key, default in DEFAULTS.items():
        try:
            values[key] = float(form.get(key, default))
        except ValueError:
            values[key] = float(default)
    return values


def calculate(v):
    km_year = v["km_per_day"] * 365

    petrol_cost_km = v["petrol_price"] / v["petrol_mileage"] + v["petrol_maint"]
    ev_cost_km = v["electricity_price"] / v["ev_efficiency"] + v["ev_maint"]

    petrol_running = petrol_cost_km * km_year * v["years"]
    ev_running = ev_cost_km * km_year * v["years"]

    petrol_total = v["petrol_car_price"] + petrol_running
    ev_total = v["ev_price"] + ev_running

    yearly_saving = (petrol_cost_km - ev_cost_km) * km_year
    extra_price = v["ev_price"] - v["petrol_car_price"]
    if extra_price <= 0:
        break_even = 0
    elif yearly_saving > 0:
        break_even = extra_price / yearly_saving
    else:
        break_even = None

    return {
        "km_year": km_year,
        "petrol_cost_km": petrol_cost_km,
        "ev_cost_km": ev_cost_km,
        "petrol_running": petrol_running,
        "ev_running": ev_running,
        "petrol_total": petrol_total,
        "ev_total": ev_total,
        "petrol_co2": km_year / v["petrol_mileage"] * PETROL_CO2_PER_LITRE,
        "ev_co2": km_year / v["ev_efficiency"] * GRID_CO2_PER_KWH,
        "break_even": break_even,
        "winner": "EV" if ev_total < petrol_total else "Petrol",
        "difference": abs(petrol_total - ev_total),
    }


@app.template_filter("money")
def money(value):
    return f"Rs. {value:,.0f}"


PAGE = """
<!doctype html>
<html>
<head>
<title>Petrol vs EV</title>
<style>
  body { font-family: Arial, sans-serif; max-width: 900px; margin: 30px auto; padding: 0 15px; background: #f4f6f8; }
  h1 { text-align: center; }
  .card { background: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 1px 4px rgba(0,0,0,.1); }
  .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
  label { font-size: 14px; color: #333; }
  input { width: 100%; padding: 8px; margin-top: 4px; box-sizing: border-box; }
  button { margin-top: 15px; padding: 10px 24px; background: #0b6e4f; color: white; border: none; border-radius: 6px; font-size: 16px; cursor: pointer; }
  table { width: 100%; border-collapse: collapse; }
  th, td { padding: 10px; border-bottom: 1px solid #ddd; text-align: left; }
  th { background: #eef1f4; }
  .winner { background: #e3f6e8; padding: 12px; border-radius: 8px; font-size: 18px; text-align: center; }
  .bar { height: 22px; border-radius: 4px; color: white; font-size: 13px; line-height: 22px; padding-left: 8px; margin: 4px 0 12px; white-space: nowrap; }
</style>
</head>
<body>
<h1>Petrol car vs EV comparison</h1>

<form method="post" class="card">
  <div class="grid">
    <label>Distance driven per day (km)<input type="number" step="any" name="km_per_day" value="{{ v.km_per_day }}"></label>
    <label>Years of ownership<input type="number" step="any" name="years" value="{{ v.years }}"></label>
    <label>Petrol price (Rs. per litre)<input type="number" step="any" name="petrol_price" value="{{ v.petrol_price }}"></label>
    <label>Electricity price (Rs. per kWh)<input type="number" step="any" name="electricity_price" value="{{ v.electricity_price }}"></label>
    <label>Petrol car price (Rs.)<input type="number" step="any" name="petrol_car_price" value="{{ v.petrol_car_price }}"></label>
    <label>EV price (Rs.)<input type="number" step="any" name="ev_price" value="{{ v.ev_price }}"></label>
    <label>Petrol mileage (km per litre)<input type="number" step="any" min="0.1" name="petrol_mileage" value="{{ v.petrol_mileage }}"></label>
    <label>EV efficiency (km per kWh)<input type="number" step="any" min="0.1" name="ev_efficiency" value="{{ v.ev_efficiency }}"></label>
    <label>Petrol maintenance (Rs. per km)<input type="number" step="any" name="petrol_maint" value="{{ v.petrol_maint }}"></label>
    <label>EV maintenance (Rs. per km)<input type="number" step="any" name="ev_maint" value="{{ v.ev_maint }}"></label>
  </div>
  <button type="submit">Compare</button>
</form>

<div class="card">
  <div class="winner">
    Over {{ v.years|int }} years, <b>{{ r.winner }}</b> is cheaper by <b>{{ r.difference|money }}</b>
  </div>
  <p>
    {% if r.break_even == 0 %}
      The EV costs no more than the petrol car to buy, so it is cheaper from day one.
    {% elif r.break_even is none %}
      The EV never pays back its higher price with these numbers.
    {% else %}
      The EV pays back its higher price in about <b>{{ "%.1f"|format(r.break_even) }} years</b>.
    {% endif %}
  </p>

  <table>
    <tr><th>Item</th><th>Petrol</th><th>EV</th></tr>
    <tr><td>Purchase price</td><td>{{ v.petrol_car_price|money }}</td><td>{{ v.ev_price|money }}</td></tr>
    <tr><td>Running cost per km</td><td>Rs. {{ "%.2f"|format(r.petrol_cost_km) }}</td><td>Rs. {{ "%.2f"|format(r.ev_cost_km) }}</td></tr>
    <tr><td>Running cost ({{ v.years|int }} years)</td><td>{{ r.petrol_running|money }}</td><td>{{ r.ev_running|money }}</td></tr>
    <tr><td><b>Total cost of ownership</b></td><td><b>{{ r.petrol_total|money }}</b></td><td><b>{{ r.ev_total|money }}</b></td></tr>
    <tr><td>CO2 per year (tailpipe + grid)</td><td>{{ "%.0f"|format(r.petrol_co2) }} kg</td><td>{{ "%.0f"|format(r.ev_co2) }} kg</td></tr>
  </table>
</div>

<div class="card">
  <b>Total cost comparison</b>
  {% set top = [r.petrol_total, r.ev_total]|max %}
  <div class="bar" style="width: {{ r.petrol_total / top * 100 }}%; background: #c0392b;">Petrol: {{ r.petrol_total|money }}</div>
  <div class="bar" style="width: {{ r.ev_total / top * 100 }}%; background: #0b6e4f;">EV: {{ r.ev_total|money }}</div>
</div>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    values = read_inputs(request.form) if request.method == "POST" else dict(DEFAULTS)
    # avoid division by zero
    for key in ("petrol_mileage", "ev_efficiency"):
        if values[key] <= 0:
            values[key] = DEFAULTS[key]
    return render_template_string(PAGE, v=values, r=calculate(values))


if __name__ == "__main__":
    app.run(debug=True)
