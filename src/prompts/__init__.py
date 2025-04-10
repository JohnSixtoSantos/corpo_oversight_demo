from llama_index.core.prompts import RichPromptTemplate

EXTRACT_COMPANY_NAME=RichPromptTemplate("""
# Task
Extract the reporting company's full name from a given CSV text.
Do not give additional commentary

# CSV Text
{{csv_text}}

# Output Format
Respond by giving raw text JSON using this format:

{
    "company_name": ...
}

If no company is found, "company_name" should be a blank string.
                                        
# Output
""")

EXTRACT_REPORTING_PERIOD=RichPromptTemplate("""
# Task
Extract the last date of the reporting period described in a given CSV text.
Do not give additional commentary.

# CSV Text
{{csv_text}}

# Output Format
Respond by giving raw text JSON using this format:

{
    "reporting_period": ...
}

The reporting period must be expressed as a string in YYYY-MM-DD format.
If no reporting period is found, "reporting_period" should be a blank string.
                                        
# Output
""")

EXTRACT_SHAREHOLDERS=RichPromptTemplate("""
# Task
Extract the list of shareholders with their associated percent of ownership from CSV text.
There may be many shareholders.
Do not give additional commentary.
                                        
# CSV Text
{{csv_text}}

# Output Format
Respond by giving raw text JSON using this format:

[
    {
        "shareholder_name": ...,
        "entity_type": ...,
        "percent_of_ownership": ...
    },
    {
        "shareholder_name": ...,
        "entity_type": ...,
        "percent_of_ownership": ...
    },
    ...
]

"shareholder_name" must be a complete name.
"entity_type" must be either "individual" or "corporate".
"percent_of_ownership" must be in percentage between 0% and 100%, inclusive.

Ensure that your output is valid JSON in raw text.
                                                                   
# Output
Do not use any markdown. Output the raw text.
""")