import os
import json
from dotenv import load_dotenv

import streamlit as st
from llama_index.llms.openai import OpenAI
from tinydb import TinyDB, Query

from src.prompts import (
    EXTRACT_COMPANY_NAME,
    EXTRACT_REPORTING_PERIOD,
    EXTRACT_SHAREHOLDERS
)

load_dotenv()

llm = OpenAI(model=os.getenv("OPENAI_MODEL"))
db = TinyDB(os.getenv("TINY_DB_PATH"))
response_query = Query()

def extract_name(file):
    csv_text = file.to_csv(index=False)
    response = llm.complete(
        EXTRACT_COMPANY_NAME.format(csv_text=csv_text)
    )

    response_dict = json.loads(response.text)

    if not db.search(response_query.name == response_dict["company_name"]):  # Assuming 'name' is the field in the db
        db.insert({'name': response_dict["company_name"]})

    return response_dict["company_name"]

def extract_reporting_period(file, company_name):
    csv_text = file.to_csv(index=False)
    response = llm.complete(
        EXTRACT_REPORTING_PERIOD.format(csv_text=csv_text)
    )

    response_dict = json.loads(response.text)

    existing_entry = db.search(response_query.name == company_name)

    if existing_entry:
        # If reporting_period exists, append the new period
        current_periods = existing_entry[0].get('reporting_periods', [])
        
        # Make sure reporting_period is a list
        if isinstance(current_periods, list):
            if not any(period.get(response_dict["reporting_period"]) for period in current_periods):
                current_periods.append({response_dict["reporting_period"]: []})
        else:
            current_periods = [{response_dict["reporting_period"]: []}]  # If it's not a list, create one with the new period
        
        # Update the company with the new reporting_period
        db.update({'reporting_periods': current_periods}, response_query.name == company_name)
        
    return response_dict["reporting_period"]

def extract_shareholders(file, company_name, reporting_period):
    # Extract shareholder data from the file
    csv_text = file.to_csv(index=False)
    response = llm.complete(
        EXTRACT_SHAREHOLDERS.format(csv_text=csv_text)
    )

    shareholders = json.loads(response.text)  # Assuming the response is a list of dicts

    # Search for the company and its reporting period in the database
    existing_entry = db.search(response_query.name == company_name)

    if existing_entry:
        # Get the reporting period entry for this company
        company_data = existing_entry[0]
        reporting_periods = company_data.get('reporting_periods', [])
        
        # Find the correct reporting period entry
        reporting_period_entry = next(
            (period for period in reporting_periods if reporting_period in period), 
            None
        )
        
        if reporting_period_entry:
            # Get the period key (which is the reporting period)
            period_key = list(reporting_period_entry.keys())[0]
            current_shareholders = reporting_period_entry[period_key]

            # If there are already shareholders, stop and do not insert
            if current_shareholders:
                st.info(f"Shareholders already exist for reporting period {reporting_period}. No new shareholders will be added.")
                return shareholders  # Exit the function
            
            # Otherwise, append each shareholder individually
            for shareholder in shareholders:
                current_shareholders.append(shareholder)
            
            # Update the company entry with the new shareholder data
            db.update({'reporting_periods': reporting_periods}, response_query.name == company_name)
        else:
            st.warning(f"Reporting period {reporting_period} not found for {company_name}.")
    else:
        st.warning(f"Company {company_name} not found in the database.")
    
    return shareholders