# FinanceAI – AI-Powered Finance SQL Analyst

FinanceAI is an AI-driven analytics application that allows users to query financial data using natural language.  
The system classifies user intent, safely generates SQL queries, and returns real-time insights.

---

## Features
- Natural language → SQL conversion
- Intent-based query routing
- Role-based access control (RBAC)
- Secure query execution
- Streamlit dashboard

---

## Tech Stack
- Python
- Streamlit
- SQLite
- Pandas
- Custom AI intent classifier

---

## Project Architecture
app/ → UI layer (Streamlit)
core/ → AI logic (intent classification, SQL generation)
services/ → Business logic
infra/ → Database, logging, security
config/ → Environment configuration

## How to Run Locally

```bash
git clone https://github.com/InshaNaaz/FinanceAI.git
cd FinanceAI
pip install -r requirements.txt
streamlit run app/main.py
## Live Demo
https://financeai.streamlit.app

## Tech Stack
- Python
- Streamlit
- AI Intent Classification
- SQL Generation
- Role-Based Access Control

## Features
- Natural language financial queries
- Secure SQL execution
- Modular enterprise architecture
- Cloud deployment


