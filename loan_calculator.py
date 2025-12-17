import numpy as np
import pandas as pd
from datetime import datetime, timedelta

class LoanCalculator:
    def __init__(self):
        self.payment_history = []
    
    def calculate_monthly_payment(self, principal, annual_rate, years):
        """Calculate monthly payment using amortization formula"""
        monthly_rate = annual_rate / 12 / 100
        n_payments = years * 12
        
        if monthly_rate == 0:
            return principal / n_payments
        
        monthly_payment = (principal * monthly_rate * 
                         (1 + monthly_rate) ** n_payments) / \
                         ((1 + monthly_rate) ** n_payments - 1)
        return monthly_payment
    
    def generate_amortization_schedule(self, principal, annual_rate, years, start_date=None):
        """Generate complete amortization schedule"""
        if start_date is None:
            start_date = datetime.now()
        
        monthly_payment = self.calculate_monthly_payment(principal, annual_rate, years)
        monthly_rate = annual_rate / 12 / 100
        balance = principal
        schedule = []
        
        for month in range(1, years * 12 + 1):
            interest_payment = balance * monthly_rate
            principal_payment = monthly_payment - interest_payment
            balance -= principal_payment
            
            payment_date = start_date + timedelta(days=30 * month)
            
            schedule.append({
                'month': month,
                'date': payment_date.strftime('%Y-%m-%d'),
                'payment': round(monthly_payment, 2),
                'principal': round(principal_payment, 2),
                'interest': round(interest_payment, 2),
                'remaining_balance': abs(round(balance, 2))
            })
            
            if balance <= 0:
                break
        
        return pd.DataFrame(schedule)
    
    def calculate_early_payoff_impact(self, principal, annual_rate, years, extra_payment):
        """Calculate impact of extra payments on loan term"""
        schedule = self.generate_amortization_schedule(principal, annual_rate, years)
        monthly_payment = self.calculate_monthly_payment(principal, annual_rate, years)
        total_payment = monthly_payment + extra_payment
        
        monthly_rate = annual_rate / 12 / 100
        balance = principal
        months_saved = 0
        new_schedule = []
        month = 1
        
        while balance > 0:
            interest_payment = balance * monthly_rate
            principal_payment = total_payment - interest_payment
            
            if principal_payment > balance:
                principal_payment = balance
                total_payment = principal_payment + interest_payment
            
            balance -= principal_payment
            
            new_schedule.append({
                'month': month,
                'payment': round(total_payment, 2),
                'principal': round(principal_payment, 2),
                'interest': round(interest_payment, 2),
                'remaining_balance': abs(round(balance, 2))
            })
            
            month += 1
        
        original_months = years * 12
        new_months = len(new_schedule)
        months_saved = original_months - new_months
        
        return {
            'months_saved': months_saved,
            'interest_saved': schedule['interest'].sum() - pd.DataFrame(new_schedule)['interest'].sum(),
            'new_schedule': pd.DataFrame(new_schedule)
        }