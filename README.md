# Petri Nets Recognizer — FastAPI Service
### REST API for Automatic Petri Net Recognition from Images


## Description

petri-recognizer-api is a **REST API service** designed to:
- Accept Petri net images (`.png`, `.jpg`);
- Process a YAML configuration describing recognition parameters;
- Return results in one of several formats:
  - **PNML file** (Petri Net Markup Language);
  - **Java method** (for Petri net generation).

## Requirements

### System

* Windows 10 / 11
* Linux
* MacOS

### Python dependencies

* ultralytics
* opencv-python
* supervision
* fastapi
* uvicorn
* pyyaml
* numpy

## Project Structure

```
petri-recognizer-api/
│
├── app/
│   ├── controllers/        
│   ├── domain/             
│   ├── infrastructure/     
│   ├── pipeline/           
│   ├── services/           
│   ├── utils/           
│   └── main.py
│
├── config/
│   ├── algorithm_config/           
│   └── path_config.py
│
├── data/
│   ├── demos/           
│   └── templates/
│
├── model/
│   └── arrow-detection-weights.pt
│
├── .gitignore
├── README.md
└── requirements.txt
```

## Getting Started

### Installing

1. Clone petri-recognizer-api project

```bash
git clone https://github.com/bodkaGR/petri-recognizer-api.git
cd petri-recognizer-controllers
```

2. Create and activate a virtual environment

- On macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```

- On Windows (PowerShell)
```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run the FastAPI server
```bash
uvicorn app.main:app --reload 
```

The server should now be running at:
```
http://localhost:8000
```
You can check the interactive API documentation at:
```
http://localhost:8000/docs
```