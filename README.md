# Financial_Agent_Simulation
This project implements an AI-powered personal finance simulator that provides actionable insights into spending, savings, and financial goals. The simulation uses multiple agents that handle different aspects of financial management, such as identifying wasteful spending, tracking goal progress, and simulating emotional spending behaviors.

# Project Overview

This project focuses on building a modular AI-powered financial agent simulation system aimed at personal finance management. The system includes various AI agents that simulate different aspects of financial behavior such as budgeting, goal tracking, emotional spending, and mentorship. The goal is to help users improve their financial management skills and optimize their spending while achieving long-term financial goals.

# Core Features
	•	Spending Advisor: An AI budget coach that analyzes spending patterns and suggests strategies to optimize savings without compromising lifestyle.
	•	Goal Tracker: Monitors progress toward personal savings and investment goals, offering actionable insights and projections.
	•	Emotional Bias Agent: Simulates emotional triggers that may lead to impulsive spending, such as retail therapy or guilt-driven splurging.
	•	Mentor Agent: Offers reflective guidance based on past financial decisions, encouraging long-term growth and discipline.

# Architecture
	•	Crew AI Framework: This modular system is built using the Crew AI framework, which allows for easy management of agents, tasks, and processes.
	•	Agent-based Design: The system comprises different agents (Spending Advisor, Goal Tracker, etc.), each responsible for a specific aspect of the financial simulation.
	•	Tasks and Simulations: Tasks such as simulating cash flow, evaluating spending patterns, and tracking financial goals are executed by individual agents. These tasks rely on configurable YAML files to ensure flexibility and adaptability.

# Structure

FINANCIAL_AGENT_SIMULATION/
└── src/
    └── financial_crew/
        ├── config/                      
        │   ├── agents.yaml
        │   └── tasks.yaml
        │
        ├── output/                      
        │   └── report.md
        │   └── goal_tracking.md
        │   └── spending_review.md
        │   └── simulated_cashflow.json
        ├── tools/                       
        │   ├── _init_.py
        ├── _init_.py                  
        ├── crew.py                     
        ├── main.py                   
        ├── streamlit_app.py             
        ├── short_report.md           
        ├── requirements.txt             
        ├── pyproject.toml              
        ├── .env                        
        ├── README.md                  
        ├── tests/                       
        ├── venv/                        
        └── _pycache_/                 

# SetUp Instructions

1.⁠ ⁠Clone the repository:
    git clone https://github.com/mbohra07/Financial_Agent_Simulation.git


2.⁠ ⁠pip install -r requirements.txt

3.⁠ ⁠Set up environment variables (e.g., API keys, model paths) by creating a .env file.

4.⁠ ⁠Create and Activate a virtual environment
    python3 -m venv venv
    source venv/bin/activate  # macOS/Linux
    # OR
    venv\Scripts\activate     # Windows

5.⁠ ⁠To start the financial simulation, run:
    python -m streamlit run src/financial_crew/streamlit_app.py

# Output Files

The simulation generates several output files, including:
	•	simulate_cash_flow.json: Contains detailed cash flow simulations for the specified months.
	•	spending_review.md: Summarizes inefficiencies in spending and provides actionable advice.
	•	goal_tracking.md: Tracks the user’s progress toward their financial goals.
	•	monthly_summary.md: A comprehensive summary of the user’s financial behavior, including emotional influences and overall    goal progress.
