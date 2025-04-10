# AI-Assisted Corporate Oversight

This application demonstrates how AI can support corporate oversight by processing and analyzing shareholder data to detect suspicious activity.

## Overview

The app consists of two main components:

1. **Ingestion Interface**  
   Upload `.xls` or `.xlsx` files containing shareholder information.  
   - Uses OpenAI GPT-4o-mini to extract metadata such as company names and reporting periods.
   - Processes and stores shareholder data into a TinyDB document store.

2. **Analytics Dashboard**  
   Visualize the stored data and detect anomalies.  
   - Select a company to view its shareholder activity.
   - Highlights suspicious behavior using AI-assisted logic.

## Tech Stack

- Python (>= 3.13)
- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [LlamaIndex](https://llamaindex.ai/)
- [Plotly](https://plotly.com/python/)
- [TinyDB](https://tinydb.readthedocs.io/)
- [OpenAI (GPT-4o-mini)](https://platform.openai.com/)
- [Poetry](https://python-poetry.org/)

## Installation

### 1. Install Python >= 3.13

Make sure your system has Python 3.13 or later installed.

#### (Optional) Using a Virtual Environment

To isolate dependencies and avoid conflicts, it's recommended to use a virtual environment.

##### Option 1: Using `venv`

```bash
python3.13 -m venv .venv
source .venv/bin/activate
```

##### Option 2: Using conda
Install conda by following these [instructions](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html).

Create a new conda environment with Python 3.13:

```bash
conda create -n ai-oversight python=3.13
conda activate ai-oversight
```

### 2. Install Poetry

Follow the instructions at [https://python-poetry.org/docs/#installation](https://python-poetry.org/docs/#installation)

You can also try running `pip install poetry`

### 3. Install Dependencies

```bash
poetry install
```

### 4. Setup the Python Path
Before running the Streamlit apps, set the `PYTHONPATH`:
```bash
export PYTHONPATH=./
```

### 5. Setup the `.env` File
Rename `.env-sample` to `.env` then supply your OpenAI API Key inside.
Remember to keep this file secret from now on.

## Running Apps

### Ingesting Files

Use this to upload and process shareholder files:

```bash
streamlit run src/app.py
```

## Viewing Analytics

Use this to explore the processed data and detect suspicious activity:

```bash
streamlit run src/admin.py
```