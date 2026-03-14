🛡️ SafeGuard - Personal Safety & Emergency Response System

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-2.0+-green.svg)

**SafeGuard** is a comprehensive safety platform designed to empower users with real-time emergency tools and data-driven risk awareness. This project features a seamless integration between a high-performance frontend and a data-rich backend.

##  Key Features

- **🆘 Emergency SOS**: One-tap SOS button with 3-second countdown and automatic GPS location sharing
- **🗺️ Hotspot Mapping**: Visual heatmap of high-risk areas using Leaflet.js, identifying incident clusters
- **📊 Risk Calculator**: Predictive tool that calculates risk scores (0-100) based on historical incident data and location
- **🏥 Medical Profile**: Secure storage of blood group, allergies, and medications for first responders
- **📞 Contact Management**: CRUD functionality for up to 10 emergency contacts
- **📈 Analytics Dashboard**: Real-time overview of incident distributions and severity levels

## Tech Stack

### Frontend
- HTML5, CSS3 (Modern UI/UX)
- JavaScript (ES6+)
- Leaflet.js (Interactive mapping)

### Backend
- Python 3.8+
- Flask (REST API)
- SQLAlchemy (ORM)
- Flask-CORS (Cross-origin support)

### Database
- SQLite (Development)
- Simulated dataset of 500+ incident records

##  Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Backend Setup

1. **Clone the repository**
```bash
git clone https://github.com/votre-username/safeguard-app.git
cd safeguard-app
```

2. **Install dependencies**
```bash
pip install flask flask-sqlalchemy flask-cors
```

3. **Initialize the database** (Optional - database already included)
```bash
python seed_incidents.py
```

4. **Start the Flask server**
```bash
python app.py
```

The API will be available at `http://127.0.0.1:5000`

### Frontend Setup

Simply open `index.html` in your browser, or use a local development server:
```bash
# Using Python
python -m http.server 8080

# Or use VS Code Live Server extension
```

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/contacts` | Retrieve all emergency contacts |
| POST | `/api/contacts` | Add new emergency contact |
| GET | `/api/medical` | Get medical profile |
| POST | `/api/medical` | Update medical profile |
| POST | `/api/sos` | Trigger SOS alert |
| GET | `/api/analytics/overview` | Get incident statistics |
| GET | `/api/analytics/hotspots` | Get high-risk areas |
| POST | `/api/analytics/risk-score` | Calculate location risk score |

## 📂 Project Structure
```
safeguard-app/
├── app.py                    # Flask backend
├── seed_incidents.py         # Database seeding script
├── safety_app.db            # SQLite database
├── index.html               # Main landing page
├── sos.html                 # SOS emergency page
├── contacts.html            # Contact management
├── hotspots.html            # Risk heatmap
├── risk.html                # Risk calculator
├── medical.html             # Medical profile
├── style.css                # Global styles
├── app.js                   # Frontend JavaScript
└── frontend/                # Additional frontend assets
```

## 🎯 Usage

1. **Emergency SOS**: Click the SOS button on the main page for immediate help
2. **View Hotspots**: Navigate to the hotspot map to see high-risk areas
3. **Check Risk Score**: Enter a location to get a safety risk assessment
4. **Manage Contacts**: Add up to 10 emergency contacts
5. **Medical Info**: Store critical medical information for emergencies

##  Team

- **Frontend Developer**: Chaitanya Vardhan
- **Backend Developer**: Oumaima Sahli

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔒 Privacy & Security

- All location data is processed locally
- No personal data is stored on external servers
- Medical information is encrypted

## 📧 Contact

For questions or support, please open an issue in this repository.

## 🙏 Acknowledgments

- Leaflet.js for mapping functionality
- Flask community for excellent documentation
- All contributors and testers

---

** If you find this project useful, please consider giving it a star!**
