# Python FastAPI + PostgreSQL API

Basic production-oriented structure using FastAPI, SQLAlchemy and PostgreSQL.

## Prerequisite

Verify version of Python 3.12.10 using

    python --version

## Setup

Create and activate a virtual environment

    python -m venv .venv

Activate the Virtual Environment

    ## Windows
        venv\Scripts\activate
    ## macOS / Linux
        source venv/bin/activate

Upgrade Core Packaging Tools

    python -m pip install --upgrade pip setuptools wheel

Install dependencies:

    pip install -r requirements.txt

Copy `.env.example` to `.env` and update the PostgreSQL connection string.

## Run

    uvicorn app.main:app --reload
    .\venv\Scripts\python.exe -m uvicorn app.main:app --reload

API:
- http://127.0.0.1:8000/health
- http://127.0.0.1:8000/docs


# Project Structure & Features Included:


1. PostgreSQL Database Schema (schema.sql)

    Tables for Workers, Training Modules (with multi-language title support for Hindi and Santali), Assessments, Certifications (with UUID-based QR payload generation), Offline Sync Logs, and Admin Users.

2. FastAPI Backend Project (ar_safety_backend/)

    app/main.py: FastAPI entry point with CORS middleware configuration.

    app/database.py: SQLAlchemy session configuration and connection utility.

    app/models.py: Database models mapped with PostgreSQL JSONB and UUID types.

    app/schemas.py: Pydantic validation models for request/response payloads.

    Routers:
        workers.py: Worker registration and retrieval endpoints.
        modules.py: AR training module fetch endpoints.
        assessments.py: Assessment submission and offline batch sync endpoints with automatic certificate issuance upon passing.
        certificates.py: QR code verification endpoints.
        admin.py: Compliance and workforce tracking analytics endpoint.

    Configuration Files: requirements.txt and .env template.