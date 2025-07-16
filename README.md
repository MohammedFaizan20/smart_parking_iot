# 🚗 Smart Parking System using FastAPI & IoT

A modular **Smart Parking System** that combines **FastAPI**, **RESTful APIs**, and **IoT hardware** (Arduino + HC-SR04 Ultrasonic Sensor) to manage parking slots in real-time. Users can view live slot availability, reserve slots, and receive email confirmations — while IoT sensors update slot occupancy status automatically.

---

##  **Key Features**

-  **FastAPI** backend with RESTful endpoints for booking, authentication, and IoT updates.
-  **Arduino/ESP32 + HC-SR04** ultrasonic sensor detects vehicle presence and updates slot status automatically.
-  **User Authentication** with hashed passwords using bcrypt.
-  **Email notifications** sent via SMTP using FastAPI `BackgroundTasks` (non-blocking).
-  **Asynchronous endpoints** for better performance and scalability.
-  **MySQL database** with SQLAlchemy ORM for storing user data and parking slots.
-  **CORS** setup for secure frontend-backend communication.

---

##  **Tech Stack**

- **Backend:** FastAPI, SQLAlchemy, Pydantic
- **Database:** MySQL
- **Hardware:** Arduino Microcontroller, ESP8266 Wi-Fi Module, HC-SR04 Ultrasonic Sensor
- **Languages:** Python, C++ (Arduino Sketch)
- **Other Tools:** Uvicorn, Gunicorn, Render for deployment, SMTP for emails

---

## 📂 **Project Structure**

project-root/
├── main.py
├── api/
│ ├── user/app.py
│ ├── auth_app/app.py
│ ├── schema.py
├── db/
│ ├── config.py
│ ├── database.py
├── .env
├── README.md


---

##  **How it Works**

1. **IoT Module:**  
   - Arduino/ESP32 runs C++ code to read distance from the HC-SR04 sensor.
   - Determines if a slot is `occupied` or `free` based on distance threshold.
   - Sends a POST request every few seconds with `api_key` and `value` to the FastAPI `/send_parking_data` endpoint.

2. **FastAPI Backend:**  
   - Receives IoT data, validates the `api_key`, parses the data, and updates the slot status in PostgreSQL.
   - Provides RESTful endpoints for:
     - `/signup/` → New user registration
     - `/login` → Secure user login
     - `/parking_lot` → View all slots and availability
     - `/reserve_parking_slot/{slot_number}` → Check slot availability
     - `/send_email/` → Send booking confirmation email
   - Uses `bcrypt` to securely hash passwords.
   - Sends emails asynchronously using `BackgroundTasks` to keep API responses fast.

3. **Frontend:**  
   - The frontend (not in this repo) calls these endpoints to display slots on a dashboard and handle user actions.

---

##  **Hardware Circuit Overview**

- **Microcontroller:** Arduino + ESP8266 WiFi module.
- **Sensor:** HC-SR04 connected to GPIO pins (`Trig` & `Echo`).
- **WiFi:** Connects to local WiFi and hits backend API directly.

---

##  **Arduino Sketch Example**

Sample logic:
```cpp
#include <WiFi.h>
#include <HTTPClient.h>
// Setup WiFi credentials, pins, measure distance, decide occupied/free
// Send POST request: api_key=#54321&value=1

(See arduino/parking_sensor.ino for full code.)

**Environment Variables**

SQL_DB_URL=mysql+pymysql://root:password123@localhost:3306/parking_db

**Setup Instructions**

1)Clone Repo

git clone https://github.com/MohammedFaizan/smart_parking_iot.git
cd smart-parking-system

2)Install Python Dependencies
pip install fastapi uvicorn[standard] SQLAlchemy pydantic psycopg2-binary python-dotenv bcrypt

3)Set up .env

SQL_DB_URL=
SENDER_EMAIL=
SENDER_PASSWORD=

4)Initialize Database
# In Python shell or DB GUI:
# Create database manually or with SQLAlchemy Base.metadata.create_all()

5)Run Server
uvicorn main:app --reload

Access:
  Docs: http://localhost:8000/docs
  Health check: /health

**Run Arduino Code**

1) Open Arduino IDE.

2) Connect your ESP32 or NodeMCU.

3) Flash the sketch (check repo).

4) Make sure WiFi SSID, password, and backend URL are correct.

5) Open Serial Monitor to see distance and API POST status.

**API Endpoints Summary**

| Endpoint                       | Method | Description                           |
| ------------------------------ | ------ | ------------------------------------- |
| `/signup/`                     | POST   | Register new users                    |
| `/login`                       | POST   | Authenticate user credentials         |
| `/parking_lot`                 | GET    | Get all slots with current status     |
| `/reserve_parking_slot/{slot}` | GET    | Check if a specific slot is available |
| `/send_parking_data`           | POST   | IoT POST: updates slot status         |
| `/send_email/`                 | POST   | Sends booking confirmation email      |
| `/health`                      | GET    | Health check                          |


**Contact**

Developed and maintained by [Your Name]  
[LinkedIn](https://www.linkedin.com/in/mohammedfaizan20/)) | [GitHub] (https://github.com/MohammedFaizan20)
[Portfolio] (https://mohdfaizn.netlify.app)

For any questions or collaboration opportunities, feel free to connect.
