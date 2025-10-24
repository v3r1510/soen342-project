# Rail Network System

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [Team](#team)

## Overview
This is an academic project for the class SOEN342 - Software Requirements and Deployment, taught by  Constantinos Constantinides in Fall 2025. The Railway Network System is a web application allowing users to book their train trips accross Europe - they can search for train connections and book them.

## Features
### For Users
- Search for connections between cities
- View train connections and details
- Book and view trips and reservations
### For Administrators
- Load connections from .csv file
- Manage databases

## Technologies Used
- **Frontend**: HTML, CSS, JavaScript, React
- **Backend**: Python
- **Database**: Python Arrays

## Getting Started

### Prerequisites

Having virtual environment in python : python -m *venv* venv
*replace the first venv by the name you want your virtual environment to have* 
PS never commit the venv to your repo
### Installation

Activate your virtual environment : 
    venv/Script/activate
Once the environment is active, install the requirements:
    pip install -r requirements.txt 

## Start the backend 
Go to your backend folder: 
    cd backend
Start the flask app:
    flask --run

## Usage
### For Users
#### Searching for Routes
1. Navigate to the homepage
2. Enter at least one search criterion (e.g. departure city and/or duration, etc.)
3. Click "Search Connections"
5. Browse the results

#### Booking a Trip
*TBD*

### For Administrators
#### Loading available connections
*TBD*

## Project Structure
```
rail-network-system/
├── .idea/              # *Auto generated code*
│  
├── software-artifacts/ # Diagrams and Models for each iteration
│   ├── iteration1/
│   └── iteration2/
├── frontend/           # Frontend code
│   └── public/         # Helper functions
│     ├── index.html/   # Main page file
│     ├── search.css/   # CSS file
│     └── search.js/    # JavaScript file
├── backend/            # Backend code
│   ├── models/         # *This folder will contain the models, in other words, our objects*
│   └── controllers/    # *This folder will contain the controllers, it will be the link between the frontend and backend*
├── .gitignore
├── Procfile            # *This is an honcho file that will let the user start both the backend and the frontend simultaneously*
├── README.md
├── requirements.txt    # *This file contains the required python module to download in your venv, these module are essential to run your code*
└── test_backend.py     # *backend tests*
```
## Contributing
1. Create an issue for the feature/bug
2. Create a new branch from `main`
```bash
git checkout -b feature/issue-number-description
```

3. Make your changes, stage them and commit
```bash
git add .
git commit -m "Add feature X, fixes #123"
```

4. Push to GitHub
```bash
git push origin feature/issue-number-description
```

5. Create a Pull Request
6. Wait for code review and approval
7. Merge after approval

## Team
| Name               | Role                   | GitHub             | StudentID |
|--------------------|------------------------|--------------------|-----------|
| [Valeria Rosca]    | Project Lead, Frontend | [v3r1510]          | 40297230  |
| [Karan Kumar]      | Backend                | [zekaran30]        | 40277342  |
| [Mohammed Janoudi] | Backend                | [Mohammed-Janoudi] | 40252594  |
