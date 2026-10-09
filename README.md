# HA-Automation-Robustness

Bachelor's Thesis
**Home Assistant: A Tool for Improving Automation Reliability**  
*(Work in Progress)*

---

## Description

This project implements a tool for analyzing Home Assistant automations.

The goal is to identify semantic errors and potential issues that may lead to unreliable behavior in smart home automations.

The tool processes YAML configurations, converts them into an internal representation (IR), and performs a set of semantic checks based on predefined rules.

---

## Requirements

- Python 3.10+ (tested on 3.10 and 3.12)
- Virtual environment (recommended)
- Operating system: Linux / Windows / macOS

---

## Installation

### 1. Create a Virtual Environment
``` bash
python -m venv venv
```

### 2. Activate the Virtual Environment

#### Linux 
```bash
source venv/bin/activate
```

#### Windows
``` bash
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Tool
#### To analyze an automation:
``` bash
python main.py
```

#### Default input file:
```
automatizacia.yaml
```

#### Analysis results are saved to:
```
parsed_output.txt
```
### 5. Run Tests
```bash
pytest -v
```


