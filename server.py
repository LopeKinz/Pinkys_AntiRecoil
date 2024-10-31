from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)

# Beispiel-Pfad zur JSON-Datei, die die Lizenzen speichert
license_file_path = "licenses.json"

# Funktion, um die Lizenzdatei zu laden
def load_licenses():
    if not os.path.exists(license_file_path):
        with open(license_file_path, "w") as file:
            json.dump({}, file)
    with open(license_file_path, "r") as file:
        return json.load(file)

# Funktion, um die Lizenzdatei zu speichern
def save_licenses(licenses):
    with open(license_file_path, "w") as file:
        json.dump(licenses, file, default=str)

@app.route('/check_license', methods=['POST'])
def check_license():
    data = request.get_json()
    license_key = data.get('license_key')
    
    licenses = load_licenses()
    
    if license_key in licenses:
        license_info = licenses[license_key]
        if license_info["valid"]:
            # Wenn die Lizenz noch nicht aktiviert wurde, aktiviere sie jetzt
            if license_info["activation_date"] is None:
                license_info["activation_date"] = datetime.now().isoformat()
                save_licenses(licenses)
                return jsonify({"valid": True, "remaining_days": license_info["duration_days"]})
            else:
                # Überprüfe, ob die Lizenz abgelaufen ist
                activation_date = datetime.fromisoformat(license_info["activation_date"])
                duration = timedelta(days=license_info["duration_days"])
                if datetime.now() <= activation_date + duration:
                    remaining_days = (activation_date + duration - datetime.now()).days
                    return jsonify({"valid": True, "remaining_days": remaining_days})
                else:
                    # Lizenz ist abgelaufen
                    license_info["valid"] = False
                    save_licenses(licenses)
                    return jsonify({"valid": False, "message": "Lizenz abgelaufen."})
    return jsonify({"valid": False, "message": "Ungültiger Lizenzschlüssel."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
