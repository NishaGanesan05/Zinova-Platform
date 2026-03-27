# Zinova – AI-Based Food Optimization Platform

Zinova is a full-stack application designed to optimize food resource management using AI. It includes an OTP-based authentication system and a dashboard interface. Google Sheets integration will be added for lightweight data storage.

## Features

- OTP-based authentication using Brevo SMTP
- Login and verification system
- Dashboard interface
- FastAPI backend
- React (Vite + TypeScript) frontend
- Clean and beginner-friendly structure

## Tech Stack

Frontend: React (Vite + TypeScript)
Backend: FastAPI
Email Service: Brevo (SMTP)
Authentication: OTP-based login

## Project Structure

zinova/

backend/
  main.py
  requirements.txt
  .env.example

frontend/
  src/
  package.json
  vite.config.ts

README.md

## Setup Instructions

### Clone the repository

git clone https://github.com/your-username/zinova.git
cd zinova

### Backend setup

cd backend
pip install -r requirements.txt

Create a `.env` file with:

BREVO_SMTP_SERVER=smtp-relay.brevo.com
BREVO_SMTP_PORT=587
BREVO_EMAIL=your_smtp_login
BREVO_PASSWORD=your_smtp_key

Run backend:

uvicorn main:app --reload

### Frontend setup

cd frontend
npm install
npm run dev

## How It Works

1. User enters email
2. OTP is sent via Brevo
3. User verifies OTP
4. User gets access to dashboard

## Upcoming Features

- Google Sheets integration
- Data analytics features
- Deployment