# Situational-Aware Zero Trust (SAZT)

A dynamic, context-aware Zero Trust security system designed for healthcare environments.

## Overview

Traditional access control systems are static and fail to adapt to real-time clinical urgency.  
This project introduces a **Situational-Aware Zero Trust (SAZT)** model that dynamically evaluates access requests based on multiple factors.

## Key Features

- Dynamic Trust Scoring
- Context-Aware Access (Emergency vs Normal)
- Behavioral Risk Analysis
- Policy-Based Decision Engine
- Explainable Security Decisions
- Interactive Web Interface (Streamlit)

## System Architecture

The system consists of two layers:

### 1. Core Engine (Automatic)
- Dataset-driven simulation
- Trust score computation
- Decision generation
- Attack detection

### 2. Interactive UI
- Real-time simulation tool
- User-controlled testing interface

## How It Works

The system calculates a **Trust Score** using:

- User Role
- Behavior Score
- Context (Emergency / Normal)
- Resource Sensitivity

Based on this score, access is:
- Allowed instantly
- Allowed with authentication
- Blocked

## System Modes

- **Automated Mode**: Runs complete SAZT pipeline using synthetic dataset (`main.py`)
- **Interactive Mode**: Allows manual simulation via UI (`app.py`)

## How to Run

### Run Automatic System

```bash
python main.py

### Run Interactive UI

```bash
streamlit run app.py

### Run Interactive UI

```bash
streamlit run app.py

## Screenshots

### User Interface
![UI](ui.png)

### System Execution (Terminal)
![Terminal](terminal.png)

### Performance Visualization
![Charts](charts.png)

### Live Security Stream
![Logs](logs.png)
