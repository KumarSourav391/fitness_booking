## Fitness Booking

### Setup Instructions

1. Clone the repo or unzip files.
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   python run.py
   ```

### API Endpoints

#### Get All Classes
cURL:
``` 
curl --location 'http://127.0.0.1:5000/classes?timezone=UTC'
```

#### Book a Class
cURL:
```
curl --location 'http://127.0.0.1:5000/book' \
--header 'Content-Type: application/json' \
--data-raw '{
  "class_id": 3,
  "client_name": "Sourav Kumar",
  "client_email": "sourav@example.com"
}'
```

#### Get Bookings by Email
cURL:
```
curl --location 'http://127.0.0.1:5000/bookings?email=sourav%40example.com'
```

---

### Seed Data
The app will auto-create three classes (Yoga, Zumba, HIIT) on first run.

---

### Notes
- Timezone can be passed as query param to `/classes`.
- Error handling included for overbooking and invalid data.# fitness_booking