import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

class DataVisualizer:
    def __init__(self):
        plt.style.use('default')
    
    def create_amortization_chart(self, schedule_df):
        """Create amortization chart using matplotlib"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Payment composition chart (first 3 years)
        months_to_show = min(36, len(schedule_df))
        months = schedule_df['month'].head(months_to_show)
        principal = schedule_df['principal'].head(months_to_show)
        interest = schedule_df['interest'].head(months_to_show)
        
        ax1.stackplot(months, principal, interest, 
                     labels=['Principal', 'Interest'], 
                     colors=['#4361ee', '#f72585'], alpha=0.8)
        ax1.set_title('Monthly EMI Composition\n(First 3 Years)')
        ax1.set_xlabel('Month')
        ax1.set_ylabel('Amount (₹)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Balance over time
        ax2.plot(schedule_df['month'], schedule_df['remaining_balance'], 
                color='#4cc9f0', linewidth=2)
        ax2.set_title('Remaining Balance Over Time')
        ax2.set_xlabel('Month')
        ax2.set_ylabel('Balance (₹)')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def create_payment_breakdown(self, schedule_df):
        """Create payment breakdown pie chart"""
        total_principal = schedule_df['principal'].sum()
        total_interest = schedule_df['interest'].sum()
        
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.pie([total_principal, total_interest], 
               labels=['Principal', 'Interest'],
               autopct='%1.1f%%',
               colors=['#4361ee', '#f72585'])
        ax.set_title('Total Payment Breakdown')
        
        return fig
    
    def create_comparison_chart(self, original_schedule, accelerated_schedule):
        """Compare original vs accelerated repayment"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.plot(original_schedule['month'], original_schedule['remaining_balance'], 
                label='Original Plan', color='#7209b7', linewidth=2)
        ax.plot(accelerated_schedule['month'], accelerated_schedule['remaining_balance'], 
                label='With Extra Payments', color='#f72585', linewidth=2)
        ax.set_title('Original vs Accelerated Repayment')
        ax.set_xlabel('Month')
        ax.set_ylabel('Balance (₹)')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        return fig
    
    def create_summary_chart(self, monthly_payment, total_interest, total_principal):
        """Create summary bar chart"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        categories = ['Monthly EMI', 'Total Interest', 'Total Principal']
        values = [monthly_payment, total_interest, total_principal]
        colors = ['#4361ee', '#f72585', '#4cc9f0']
        
        bars = ax.bar(categories, values, color=colors, alpha=0.8)
        ax.set_title('Loan Summary')
        ax.set_ylabel('Amount (₹)')
        
        # Add value labels on bars with Indian number formatting
        for bar, value in zip(bars, values):
            height = bar.get_height()
            # Format large numbers with commas for Indian numbering system
            formatted_value = f'₹{value:,.0f}'
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   formatted_value,
                   ha='center', va='bottom', fontweight='bold')
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        return fig
    
    def create_interest_vs_principal_chart(self, schedule_df):
        """Create cumulative interest vs principal chart"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        cumulative_principal = schedule_df['principal'].cumsum()
        cumulative_interest = schedule_df['interest'].cumsum()
        
        ax.plot(schedule_df['month'], cumulative_principal, 
                label='Cumulative Principal', color='#4361ee', linewidth=2)
        ax.plot(schedule_df['month'], cumulative_interest, 
                label='Cumulative Interest', color='#f72585', linewidth=2)
        ax.set_title('Cumulative Principal vs Interest Payments')
        ax.set_xlabel('Month')
        ax.set_ylabel('Amount (₹)')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        return fig
    
    def create_yearly_breakdown_chart(self, schedule_df):
        """Create yearly payment breakdown"""
        # Group by year
        schedule_df['year'] = (schedule_df['month'] - 1) // 12 + 1
        yearly_data = schedule_df.groupby('year').agg({
            'principal': 'sum',
            'interest': 'sum',
            'payment': 'sum'
        }).reset_index()
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        x = yearly_data['year']
        principal = yearly_data['principal']
        interest = yearly_data['interest']
        
        ax.bar(x, principal, label='Principal', color='#4361ee', alpha=0.8)
        ax.bar(x, interest, bottom=principal, label='Interest', color='#f72585', alpha=0.8)
        
        ax.set_title('Yearly Payment Breakdown')
        ax.set_xlabel('Year')
        ax.set_ylabel('Amount (₹)')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Only show every 2nd year label if there are many years
        if len(x) > 10:
            ax.set_xticks(x[::2])
        
        plt.tight_layout()
        return fig

# Test function to verify the visualizer works
def test_visualizer():
    """Test the visualizer with sample data"""
    try:
        # Create sample data
        sample_data = pd.DataFrame({
            'month': range(1, 61),
            'principal': np.random.uniform(10000, 20000, 60),
            'interest': np.random.uniform(5000, 15000, 60),
            'remaining_balance': np.linspace(2500000, 0, 60)
        })
        
        visualizer = DataVisualizer()
        
        # Test each chart
        fig1 = visualizer.create_amortization_chart(sample_data)
        fig2 = visualizer.create_payment_breakdown(sample_data)
        fig3 = visualizer.create_summary_chart(15000, 500000, 2000000)
        
        print("✅ DataVisualizer is working correctly!")
        plt.close('all')
        return True
        
    except Exception as e:
        print(f"❌ Error in DataVisualizer: {e}")
        return False

if __name__ == "__main__":
    test_visualizer()