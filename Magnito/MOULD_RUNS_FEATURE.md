# Mould Runs Feature

## Overview
Added a new feature to track active mould runs with setter information directly from the dashboard.

## What's New

### 1. MouldRun Model
Tracks:
- Which mould is running
- Machine number
- Setter name
- Start time
- When setter completed the setup
- End time (when stopped)
- Active status
- Notes

### 2. Dashboard Integration
The "Active Moulds" card now includes:
- Link to start a new run
- Display of all active mould runs with:
  - Mould and machine information
  - Setter name
  - Start time and setter completion time
  - Running duration (auto-calculated)
  - Stop button for each run
  - Pulsing "ACTIVE" badge
  - Color-coded cards with green accent

### 3. New Pages

**Start Mould Run** (`/mould-runs/create/`)
- Select mould
- Enter machine number
- Enter setter name
- Set start time
- Set setter completion time
- Add optional notes

**Mould Runs List** (`/mould-runs/`)
- View all active runs
- View completed runs history
- Stop active runs
- See duration for each run

### 4. Navigation
Added "Mould Runs" link to main navigation menu

## Usage

### Starting a New Run
1. Click "➕ Start New Run" on the Active Moulds card
2. Or click "Mould Runs" in navigation → "🚀 Start New Run"
3. Fill in the form:
   - Select the mould
   - Enter machine number
   - Enter setter's name
   - Set start time (defaults to now)
   - Set when setter completed setup
   - Add any notes
4. Click "🏁 Start Run"

### Viewing Active Runs
- Dashboard shows all active runs in colorful cards
- Each card displays:
  - Mould and machine info
  - Setter details
  - Timing information
  - Running duration
  - Stop button

### Stopping a Run
- Click "⏹️ Stop Run" button on any active run
- Run will be marked as completed
- End time is automatically recorded

## Features
- ✅ Real-time duration calculation
- ✅ Funky modern design with gradients
- ✅ Pulsing active indicator
- ✅ Easy-to-use interface
- ✅ Complete run history
- ✅ Admin panel integration

## Database
New table: `moulding_mouldrun`
- Tracks all mould runs (active and completed)
- Linked to Mould and User models
- Automatically calculates duration

## Access
- Dashboard: http://localhost:8000/
- Mould Runs: http://localhost:8000/mould-runs/
- Start Run: http://localhost:8000/mould-runs/create/
