# Pinky's AntiRecoil V1

Pinky's AntiRecoil V1 is a tool for automating mouse movements with a user-friendly GUI. It includes a licensing system for managing usage rights and a server-side component for verifying licenses.

This is a Proof of Concept. This can be used for a Anti Recoil for games like Call of Duty Blackops 6 or any other FPS!
This Project is powered by users, who programm and maintain the presets for mouse movements!
Feel free to Email me your Presets!

## Features

- **Mouse Automation**: Create custom presets to control mouse movements.
- **Easy GUI**: User-friendly interface for managing presets.
- **Licensing System**: License verification via a Flask server to ensure that the program runs only with valid licenses.
- **GitHub Integration**: Download presets directly from a GitHub repository.

## Installation

### Requirements
- Python 3.6 or higher
- Flask (for the license server)

### Step-by-Step Guide

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/LopeKinz/mouseflow_presets.git
   cd mouseflow_presets
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the License Server**:
   Run the license server locally on your machine:
   ```bash
   python server.py
   ```

4. **Start the Main Program**:
   ```bash
   python recoil.py
   ```

## Usage

### Automating Mouse Movements
- Create a new preset by clicking `Create Preset` and enter mouse movement commands in the editor.
- Load a preset to automatically control the mouse based on the saved commands.

### Licensing
- The program requires a valid license key. Enter the license key when prompted to activate the license.
- The license server checks whether the license is valid and how much time is remaining.

### Download Presets from GitHub
- Click `Download Presets from GitHub` to import available presets directly from the repository.

## License Management

Licenses are stored in a JSON file (`licenses.json`). This file contains license keys, activation dates, and license duration. Licenses can be edited directly in this file to modify the validity duration.

Example `licenses.json`:
```json
{
    "ABCDE-12345-FGHIJ-67890": {
        "valid": true,
        "activation_date": null,
        "duration_days": 1
    },
    "KLMNO-12345-PQRST-67890": {
        "valid": true,
        "activation_date": null,
        "duration_days": 7
    },
    "UVWXY-12345-ZABCD-67890": {
        "valid": true,
        "activation_date": null,
        "duration_days": 30
    }
}
```

## Security Notes
- The license server should be properly secured for public use, e.g., using HTTPS and firewall.
- Use secure license keys to prevent misuse.

## Requirements
- **Python 3.6+**: The project is developed in Python.
- **Flask**: For license management and server integration.

## Contributing
Contributions are welcome! Create an issue or a pull request to propose changes.

## License
This project is licensed under the MIT License. For more information, see the `LICENSE` file.
