# WeAreCars – Car Rental Booking System

A desktop application for a car rental company, built with **Python, Tkinter and SQLite**. Staff sign in, register customers, book a car and see the price calculated instantly, then review all current rentals in a searchable dashboard.

Designed and developed end to end by Sophiya Chhetri (GUI, business logic and database) as part of the CET131 assessment.

## Features

- **Staff login** with a splash screen and a clean dashboard
- **Booking form** for customer details, car type, fuel type and rental length (1–28 days)
- **Live price calculator** that updates as options change
- **Optional extras:** unlimited mileage and breakdown cover
- **Input validation** for names, address, age (18+), licence and rental days
- **Booking summary** screen with a full price breakdown before confirming
- **Rented cars dashboard** with search, colour-coded rows, details view, rental count and revenue total
- **SQLite database** created automatically on first run (customers, cars, bookings)

## Pricing

| Item | Price |
|---|---|
| Base rate | £25 per day |
| Car type surcharge | City £0 · Family £50 · Sports £75 · SUV £65 |
| Fuel surcharge | Petrol/Diesel £0 · Hybrid £30 · Full electric £50 |
| Unlimited mileage | £10 per day |
| Breakdown cover | £2 per day |

## Tech stack

- Python 3.8+
- Tkinter / ttk (GUI)
- SQLite (`sqlite3`)
- Pillow (images)

## Getting started

```bash
git clone https://github.com/sophiyachhetri781116-bit/WeAreCars.git
cd WeAreCars
pip install -r requirements.txt
python main.py
```

**Demo login:** username `sta001` · password `givemethekeys123`

## Project structure

```
main.py                 Application entry point and theme
controllers/
  auth.py               Login check
  database.py           SQLite setup and data access
  pricing.py            Price calculator
  validation.py         Input validation
views/
  splash_screen.py      Animated welcome screen
  login_screen.py       Staff login
  main_dashboard.py     Tabbed main window
  booking_screen.py     Booking form
  summary_screen.py     Booking confirmation summary
  car_list.py           Rented cars table
assets/                 Logos and icons
```

## Planned improvements

- Save confirmed bookings and car availability permanently in the database
- Secure staff accounts with hashed passwords
- Export and print reports from the rented cars list
