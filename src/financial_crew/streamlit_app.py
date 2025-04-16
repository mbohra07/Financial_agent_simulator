import time
import streamlit as st
import os
import json
from litellm import RateLimitError
from crew import FinancialCrew
from datetime import date
import pandas as pd

# Streamlit configuration
st.set_page_config(
    page_title="🧠 Financial Agent Simulator", 
    layout="centered",
    initial_sidebar_state="expanded"
)
st.title("📈 Financial Agent Simulation")

st.markdown("""
Welcome to your **Personal Financial Simulation**. Simulate months of financial life, get guidance, 
and improve your money habits with AI agents!
""")

# Sidebar for navigation
with st.sidebar:
    st.header("Simulation Navigation")
    display_option = st.radio(
        "View Results",
        options=["📋 Monthly Summary", "💰 Cash Flow", "💡 Spending Review", "🎯 Goal Tracking","📊 Wellness Score"],
        index=0
    )
    st.markdown("---")
    st.caption("ℹ️ Run a new simulation to update all reports")

# Collecting user profile details
with st.form("user_profile_form"):
    st.subheader("👤 Basic User Profile")

    col1, col2 = st.columns(2)
    with col1:
        user_name = st.text_input("Name")
        age = st.slider("Age", min_value=18, max_value=70)
        occupation = st.selectbox("Occupation", ["Student", "Salaried", "Freelancer", "Business Owner", "Unemployed"])
    with col2:
        income_level = st.selectbox("Monthly Income Level (₹)", ["<10,000", "10,000–30,000", "30,000–70,000", "70,000+"])
        starting_balance = st.number_input("Starting Bank Balance (₹)", min_value=0)
        simulation_months = st.slider("Simulate how many months?", min_value=1, max_value=12)
    
    financial_goal = st.text_input("What's your financial goal? (e.g., 'Save ₹50,000 for emergency fund')")
    submit = st.form_submit_button("💡 Run Financial Simulation")

def run_simulation_with_retries(inputs, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            result = FinancialCrew().crew().kickoff(inputs=inputs)
            return result
        except RateLimitError:
            st.warning(f"Rate limit hit. Retrying in 10 seconds... (Attempt {attempt + 1}/{max_attempts})")
            time.sleep(10)
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
            break
    return None

def display_cash_flow():
    try:
        cashflow_path = "output/simulated_cashflow.json"
        if os.path.exists(cashflow_path):
            with open(cashflow_path, "r") as f:
                cashflow_data = json.load(f)
            
            st.subheader("💰 Daily Cash Flow Simulation")
            
            # Calculate summary metrics
            total_inflows = sum(sum(day["inflows"].values()) for day in cashflow_data)
            total_outflows = sum(sum(day["outflows"].values()) for day in cashflow_data)
            net_savings = total_inflows - total_outflows
            starting_balance = cashflow_data[0]["balance"] - sum(cashflow_data[0]["inflows"].values()) + sum(cashflow_data[0]["outflows"].values())
            ending_balance = cashflow_data[-1]["balance"]
            
            # Display summary metrics
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Inflows", f"₹{total_inflows:,.2f}")
            col2.metric("Total Outflows", f"₹{total_outflows:,.2f}")
            col3.metric("Net Savings", f"₹{net_savings:,.2f}", 
                       delta=f"{((ending_balance - starting_balance)/starting_balance*100 if starting_balance != 0 else 0):.1f}%")
            
            # Display transactions in an expandable table
            with st.expander("📅 View Detailed Transactions"):
                # Convert to DataFrame for better display
                df = pd.DataFrame([{
                    "Date": day["date"],
                    "Inflows": sum(day["inflows"].values()),
                    "Outflows": sum(day["outflows"].values()),
                    "Balance": day["balance"],
                    "Notes": ", ".join([f"{k}: ₹{v}" for k, v in {**day["inflows"], **day["outflows"]}.items()])
                } for day in cashflow_data])
                
                st.dataframe(df.style.format({
                    "Inflows": "₹{:.2f}",
                    "Outflows": "₹{:.2f}",
                    "Balance": "₹{:.2f}"
                }))
            
            # Display spending distribution
            st.subheader("📊 Spending Distribution")
            
            # Aggregate spending categories
            spending = {}
            for day in cashflow_data:
                for category, amount in day["outflows"].items():
                    spending[category] = spending.get(category, 0) + amount
            
            if spending:
                spending_df = pd.DataFrame({
                    "Category": list(spending.keys()),
                    "Amount": list(spending.values())
                }).sort_values("Amount", ascending=False)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.bar_chart(spending_df.set_index("Category"))
                with col2:
                    st.dataframe(spending_df.style.format({"Amount": "₹{:.2f}"}))
            
            # Display notable events (days with notes)
            notable_days = [day for day in cashflow_data if "note" in day]
            if notable_days:
                st.subheader("🌟 Notable Events")
                for day in notable_days:
                    st.markdown(f"**{day['date']}**: {day['note']}")
            
        else:
            st.warning("Cash flow data not found. Please run the simulation first.")
            
    except json.JSONDecodeError:
        st.error("Error: The cash flow file contains invalid JSON data.")
    except KeyError as e:
        st.error(f"Error: Missing expected data field - {str(e)}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")

def display_spending_review():
    try:
        review_path = "output/spending_review.md"
        if os.path.exists(review_path):
            with open(review_path, "r") as f:
                review_content = f.read()
            st.subheader("💡 Spending Review & Suggestions")
            st.markdown(review_content)
        else:
            st.warning("Spending review not found. Please run the simulation first.")
    except Exception as e:
        st.error(f"Error reading spending review data: {e}")

def display_goal_tracking():
    try:
        goal_path = "output/goal_tracking.md"
        if os.path.exists(goal_path):
            with open(goal_path, "r") as f:
                goal_content = f.read()
            st.subheader("🎯 Goal Progress Tracking")
            st.markdown(goal_content)
            
            # Add visual progress indicator if available in the content
            if "Achieved:" in goal_content:
                try:
                    progress_text = goal_content.split("Achieved:")[1].split("%")[0].strip()
                    progress = float(progress_text) / 100
                    st.progress(progress)
                except:
                    pass
        else:
            st.warning("Goal tracking data not found. Please run the simulation first.")
    except Exception as e:
        st.error(f"Error reading goal tracking data: {e}")

def display_monthly_summary():
    try:
        report_path = "output/report.md"
        if os.path.exists(report_path):
            with open(report_path, "r") as f:
                report_content = f.read()
            st.subheader("📋 Monthly Financial Summary")
            st.markdown(report_content)
        else:
            st.warning("Monthly summary not found. Please run the simulation first.")
    except Exception as e:
        st.error(f"Error reading monthly summary data: {e}")

def calculate_wellness_score(cashflow_data, goal_data):
    """Calculate a comprehensive financial wellness score"""
    try:
        # Extract key metrics
        total_inflows = sum(sum(day["inflows"].values()) for day in cashflow_data)
        total_outflows = sum(sum(day["outflows"].values()) for day in cashflow_data)
        savings_rate = (total_inflows - total_outflows) / total_inflows if total_inflows > 0 else 0
        
        # Count impulse spending occurrences
        impulse_spends = sum(1 for day in cashflow_data if "impulse_spending" in day["outflows"])
        
        # Goal progress (extract from goal tracking or calculate)
        goal_percent = 0
        if "Achieved:" in goal_data:
            try:
                goal_text = goal_data.split("Achieved:")[1].split("%")[0].strip()
                goal_percent = float(goal_text) / 100
            except:
                pass

        savings_rate = (total_inflows - total_outflows) / total_inflows if total_inflows > 0 else 0
        
        # Count impulse spending occurrences
        impulse_spends = sum(1 for day in cashflow_data if "impulse_spending" in day["outflows"])
        
        # Goal progress (extract from goal tracking or calculate)
        goal_percent = 0
        if "Achieved:" in goal_data:
            try:
                goal_text = goal_data.split("Achieved:")[1].split("%")[0].strip()
                goal_percent = float(goal_text) / 100
            except:
                pass
        
        # Calculate score components (0-100 scale)
        savings_score = min(100, savings_rate * 200)  # 50% savings rate = 100 score
        impulse_score = max(0, 100 - (impulse_spends * 5))  # -5 points per impulse spend
        goal_score = goal_percent * 100
        consistency_score = 80  # Placeholder for more advanced calculation
        
        # Weighted final score
        wellness_score = (
            0.3 * savings_score +
            0.25 * impulse_score +
            0.3 * goal_score +
            0.15 * consistency_score
        )
        
        return {
            "wellness_score": round(wellness_score),
            "savings_rate": round(savings_rate * 100, 1),
            "impulse_spends": impulse_spends,
            "goal_progress": round(goal_percent * 100, 1),
            "categories": {
                "Savings": savings_score,
                "Discipline": impulse_score,
                "Goals": goal_score,
                "Consistency": consistency_score
            }
        }
    except Exception as e:
        st.error(f"Error calculating wellness score: {str(e)}")
        return None

def display_wellness_score():
    try:
        # Load required data
        cashflow_path = "output/simulated_cashflow.json"
        goal_path = "output/goal_tracking.md"
        
        if not os.path.exists(cashflow_path) or not os.path.exists(goal_path):
            st.warning("Please run the simulation first to generate wellness metrics")
            return
            
        with open(cashflow_path, "r") as f:
            cashflow_data = json.load(f)
            
        with open(goal_path, "r") as f:
            goal_data = f.read()
        
        # Calculate score
        wellness = calculate_wellness_score(cashflow_data, goal_data)
        if not wellness:
            return
            
        st.subheader("📊 Financial Wellness Score")
        
        # Main score display
        col1, col2, col3 = st.columns(3)
        col1.metric("Overall Score", f"{wellness['wellness_score']}/100", 
                   delta=f"{'Excellent' if wellness['wellness_score'] >= 80 else 'Good' if wellness['wellness_score'] >= 60 else 'Needs Improvement'}")
        col2.metric("Savings Rate", f"{wellness['savings_rate']}%")
        col3.metric("Impulse Spends", wellness['impulse_spends'], 
                   delta=f"{'Low' if wellness['impulse_spends'] <= 3 else 'High'}")
        
        # Score breakdown
        st.subheader("Score Breakdown")
        categories = wellness['categories']
        df = pd.DataFrame({
            "Category": categories.keys(),
            "Score": categories.values()
        })
        st.bar_chart(df.set_index("Category"))
        
        # Recommendations based on score
        st.subheader("Recommendations")
        if wellness['wellness_score'] >= 80:
            st.success("""
            🎉 Excellent financial health! Keep up these habits:
            - Continue your savings discipline
            - Consider investment opportunities
            - Share your strategies with others
            """)
        elif wellness['wellness_score'] >= 60:
            st.info("""
            👍 Good progress! Areas to improve:
            - Review discretionary spending
            - Increase savings rate by 5%
            - Track progress weekly
            """)
        else:
            st.warning("""
            ⚠️ Needs improvement. Focus on:
            - Creating a strict budget
            - Reducing impulse purchases
            - Setting smaller milestone goals
            """)
            
    except Exception as e:
        st.error(f"Error displaying wellness score: {str(e)}")

if submit:
    with st.spinner("🔍 Simulating your financial journey..."):
        user_inputs = {
            'user_name': user_name,
            'age': age,
            'occupation': occupation,
            'income_level': income_level,
            'goal': financial_goal,
            'starting_balance': starting_balance,
            'months': simulation_months
        }

        os.makedirs("output", exist_ok=True)
        result = run_simulation_with_retries(inputs=user_inputs)

        if result:
            st.success("✅ Simulation Complete!")
            st.balloons()
        else:
            st.error("Simulation failed after multiple attempts.")

# Display the selected content based on navigation
if display_option == "📋 Monthly Summary":
    display_monthly_summary()
elif display_option == "💰 Cash Flow":
    display_cash_flow()
elif display_option == "💡 Spending Review":
    display_spending_review()
elif display_option == "🎯 Goal Tracking":
    display_goal_tracking()
elif display_option == "📊 Wellness Score":
    display_wellness_score()

# Add footer
st.markdown("---")
st.caption("""
ℹ️ This is a simulation tool. Actual financial results may vary based on real-world circumstances.
Use the insights to inform your decisions, but consult a financial advisor for personalized advice.
""")