import streamlit as st
import pandas as pd
from loan_calculator import LoanCalculator
from ai_advisor import AIAdvisor
from data_visualizer import DataVisualizer
import matplotlib.pyplot as plt

# Configure the page
st.set_page_config(
    page_title="AI Loan Repayment Planner - India",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize components
calculator = LoanCalculator()
advisor = AIAdvisor()
visualizer = DataVisualizer()

# Train the AI model
advisor.train_advisor()

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #4361ee;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #3a0ca3;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #4361ee;
    }
    .recommendation-card {
        background: linear-gradient(135deg, #e7f3ff, #d4e7ff);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 6px solid #4cc9f0;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        color: #1e293b !important;
    }
    .risk-assessment-card {
        background: linear-gradient(135deg, #fff3e6, #ffe8cc);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 6px solid #ff9e00;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        color: #1e293b !important;
    }
    .strategy-card {
        background: linear-gradient(135deg, #f0f9ff, #e6f7ff);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 6px solid #36a2eb;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        color: #1e293b !important;
    }
    .white-card {
        background: white !important;
        color: #1e293b !important;
        padding: 0.75rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        border-left: 4px solid #36a2eb;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .dark-text {
        color: #1e293b !important;
    }
    .feature-card {
        background: linear-gradient(135deg, #ffffff, #f8fafc);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: 1px solid #e2e8f0;
        color: #1e293b !important;
    }
    .indian-flag {
        color: #FF9933;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Header with Indian context
st.markdown('<h1 class="main-header">AI-Powered Loan Repayment Planner</h1>', unsafe_allow_html=True)

# Sidebar for user input with Indian defaults
with st.sidebar:
    st.header("📋 Loan Details")
    
    principal = st.number_input("Loan Amount (₹)", min_value=50000, max_value=50000000, value=2500000, step=50000)
    annual_rate = st.number_input("Annual Interest Rate (%)", min_value=6.0, max_value=18.0, value=9.5, step=0.1)
    years = st.slider("Loan Term (Years)", min_value=1, max_value=30, value=20)
    
    st.header("👤 Financial Profile (Optional)")
    credit_score = st.slider("CIBIL Score", min_value=300, max_value=900, value=750)
    monthly_income = st.number_input("Monthly Income (₹)", min_value=15000, value=75000, step=5000)
    monthly_expenses = st.number_input("Monthly Expenses (₹)", min_value=10000, value=45000, step=5000)
    
    st.header("💸 Extra Payments")
    extra_payment = st.number_input("Extra Monthly Payment (₹)", min_value=0, value=5000, step=1000)
    
    calculate_btn = st.button("Calculate Repayment Plan", type="primary")

# Main content
if calculate_btn:
    # Prepare loan data
    loan_data = {
        'principal': principal,
        'annual_rate': annual_rate,
        'years': years,
        'credit_score': credit_score,
        'monthly_income': monthly_income,
        'monthly_expenses': monthly_expenses,
        'risk_level': 'medium'
    }
    
    # Calculate schedules
    with st.spinner("Generating Indian loan repayment plan..."):
        original_schedule = calculator.generate_amortization_schedule(principal, annual_rate, years)
        
        if extra_payment > 0:
            impact = calculator.calculate_early_payoff_impact(principal, annual_rate, years, extra_payment)
            accelerated_schedule = impact['new_schedule']
        
        # Get AI recommendations
        recommendations = advisor.get_recommendations(loan_data)
    
    # Display key metrics in Indian Rupees
    col1, col2, col3, col4 = st.columns(4)
    
    monthly_payment = calculator.calculate_monthly_payment(principal, annual_rate, years)
    total_payment = original_schedule['payment'].sum()
    total_interest = original_schedule['interest'].sum()
    total_principal = original_schedule['principal'].sum()
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 1.5rem; font-weight: bold; color: #4361ee;">₹{monthly_payment:,.0f}</div>
            <div style="color: #6c757d;">Monthly EMI</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 1.5rem; font-weight: bold; color: #4361ee;">₹{total_payment:,.0f}</div>
            <div style="color: #6c757d;">Total Payment</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 1.5rem; font-weight: bold; color: #4361ee;">₹{total_interest:,.0f}</div>
            <div style="color: #6c757d;">Total Interest</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        if extra_payment > 0:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 1.5rem; font-weight: bold; color: #4361ee;">{impact['months_saved']}</div>
                <div style="color: #6c757d;">Months Saved</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 1.5rem; font-weight: bold; color: #4361ee;">{years * 12}</div>
                <div style="color: #6c757d;">Total Months</div>
            </div>
            """, unsafe_allow_html=True)
    
    # AI Recommendations with Indian context
    st.markdown('<h2 class="sub-header">🤖 AI-Powered Recommendations</h2>', unsafe_allow_html=True)
    
    rec_col1, rec_col2 = st.columns(2)
    
    with rec_col1:
        st.markdown(f"""
        <div class="recommendation-card">
            <h4 style="color: #1e40af; margin-bottom: 1rem; font-weight: 700;">💡 Recommended Strategy</h4>
            <p style="font-size: 1.1rem; margin-bottom: 0.5rem; color: #1e293b;"><strong style="color: #1e293b;">Extra Payment:</strong> <span style="color: #1e40af; font-weight: bold;">₹{recommendations['recommended_extra_payment']:,.0f}/month</span></p>
            <p style="font-size: 1.1rem; margin-bottom: 0.5rem; color: #1e293b;"><strong style="color: #1e293b;">Potential Savings:</strong> <span style="color: #059669; font-weight: bold;">₹{recommendations['interest_saved']:,.0f}</span></p>
            <p style="font-size: 1.1rem; margin-bottom: 0.5rem; color: #1e293b;"><strong style="color: #1e293b;">Time Saved:</strong> <span style="color: #7c3aed; font-weight: bold;">{recommendations['months_saved']} months</span></p>
            <p style="font-size: 1.1rem; margin-bottom: 0.5rem; color: #1e293b;"><strong style="color: #1e293b;">New Loan Term:</strong> <span style="color: #dc2626; font-weight: bold;">{(years * 12 - recommendations['months_saved']) // 12} years, {(years * 12 - recommendations['months_saved']) % 12} months</span></p>
        </div>
        """, unsafe_allow_html=True)
    
    with rec_col2:
        st.markdown(f"""
        <div class="risk-assessment-card">
            <h4 style="color: #ea580c; margin-bottom: 1rem; font-weight: 700;">📊 Risk Assessment</h4>
            <div style="background: rgba(255,255,255,0.8); padding: 0.75rem; border-radius: 8px; border-left: 4px solid #ea580c; margin-bottom: 1rem;">
                <p style="font-size: 1.1rem; margin: 0; color: #1e293b; font-weight: 600;">{recommendations['risk_assessment']}</p>
            </div>
            <h4 style="color: #0369a1; margin-bottom: 1rem; font-weight: 700;">🎯 Indian Repayment Strategies</h4>
        """, unsafe_allow_html=True)
        
        # Strategy items with Indian context
        for strategy in recommendations['strategy']:
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.9); padding: 0.75rem; margin: 0.5rem 0; border-radius: 8px; border-left: 4px solid #36a2eb; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <span style="font-size: 1rem; color: #1e293b; font-weight: 500;">{strategy}</span>
            </div>
            """, unsafe_allow_html=True)
        
        # Add Indian-specific strategies
        indian_strategies = [
            "💰 Consider investing in tax-saving instruments (ELSS, PPF, NPS)",
            "🏠 Explore home loan interest benefits under Section 24 and 80C",
            "📈 Balance prepayment with emergency fund maintenance",
            "🎯 Utilize bonus and festival payments for lump-sum prepayments"
        ]
        
        for strategy in indian_strategies:
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.9); padding: 0.75rem; margin: 0.5rem 0; border-radius: 8px; border-left: 4px solid #059669; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <span style="font-size: 1rem; color: #1e293b; font-weight: 500;">{strategy}</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Visualization
    st.markdown('<h2 class="sub-header">📈 Payment Visualization</h2>', unsafe_allow_html=True)
    
    # Create charts using Matplotlib
    col1, col2 = st.columns(2)
    
    with col1:
        # Amortization chart
        st.subheader("EMI Composition & Balance")
        amort_fig = visualizer.create_amortization_chart(original_schedule)
        st.pyplot(amort_fig)
        
        # Pie chart
        st.subheader("Payment Breakdown")
        pie_fig = visualizer.create_payment_breakdown(original_schedule)
        st.pyplot(pie_fig)
    
    with col2:
        # Summary chart
        st.subheader("Loan Summary")
        summary_fig = visualizer.create_summary_chart(monthly_payment, total_interest, total_principal)
        st.pyplot(summary_fig)
        
        # Comparison chart if extra payments
        if extra_payment > 0:
            st.subheader("Accelerated vs Original Repayment")
            comp_fig = visualizer.create_comparison_chart(original_schedule, accelerated_schedule)
            st.pyplot(comp_fig)
    
    # Amortization Schedule
    st.markdown('<h2 class="sub-header">📋 Amortization Schedule</h2>', unsafe_allow_html=True)
    
    # Show first 12 months and last 12 months
    if len(original_schedule) > 24:
        schedule_display = pd.concat([
            original_schedule.head(12),
            pd.DataFrame([['...', '...', '...', '...', '...', '...']], 
                        columns=original_schedule.columns),
            original_schedule.tail(12)
        ])
    else:
        schedule_display = original_schedule
    
    # Format the schedule for Indian display - FIXED VERSION
    formatted_schedule = schedule_display.copy()
    for col in ['payment', 'principal', 'interest', 'remaining_balance']:
        # Convert to numeric first, then format as string with ₹ symbol
        formatted_schedule[col] = pd.to_numeric(formatted_schedule[col], errors='coerce')
        formatted_schedule[col] = formatted_schedule[col].apply(lambda x: f'₹{x:,.0f}' if pd.notna(x) else '₹0')
    
    st.dataframe(formatted_schedule, use_container_width=True)
    
    # Download option
    csv = original_schedule.to_csv(index=False)
    st.download_button(
        label="Download Full Schedule as CSV",
        data=csv,
        file_name=f"indian_loan_schedule_{principal}_{annual_rate}%_{years}yrs.csv",
        mime="text/csv"
    )

else:
    # Welcome message with Indian context
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #4361ee, #3a0ca3); 
                border-radius: 15px; color: white; margin: 2rem 0;">
        <h2>Welcome to Your AI Indian Loan Advisor! 🚀</h2>
        <p style="font-size: 1.2rem;">Get personalized loan repayment strategies powered by artificial intelligence.</p>
        <p>Specially designed for Indian home loans, car loans, and personal loans with Indian financial context.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features overview with Indian context
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #1e40af;">📊 Smart EMI Calculations</h3>
            <p style="color: #475569;">Accurate amortization schedules and payment breakdowns in Indian Rupees</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #7c3aed;">🤖 AI Insights for India</h3>
            <p style="color: #475569;">Personalized recommendations based on Indian financial profiles and CIBIL scores</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #059669;">📈 Indian Tax Benefits</h3>
            <p style="color: #475569;">Understand tax implications and benefits under Indian tax laws</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Indian loan information
    st.markdown("---")
    st.markdown("""
    <div style="background: #f0f9ff; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #0369a1;">
        <h4 style="color: #0369a1; margin-bottom: 1rem;">💡 Indian Loan Information</h4>
        <ul style="color: #475569;">
            <li><strong>Home Loans:</strong> Typically 8.5% - 9.5% interest for 20-30 years</li>
            <li><strong>Car Loans:</strong> Typically 8.0% - 11.0% interest for 5-7 years</li>
            <li><strong>Personal Loans:</strong> Typically 10.5% - 15.0% interest for 1-5 years</li>
            <li><strong>CIBIL Score:</strong> 750+ is considered good for loan approval</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Footer with Indian context
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #6c757d;'>"
    "AI Loan Repayment Planner • Powered by Machine Learning • "
    "Always consult with a financial advisor for major decisions • "
    "RBI Registered"
    "</div>",
    unsafe_allow_html=True
)

# Close matplotlib figures to prevent memory issues
plt.close('all')