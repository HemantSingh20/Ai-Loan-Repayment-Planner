import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import pandas as pd

class AIAdvisor:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.trained = False
        self.feature_columns = None  # Store the feature columns from training
    
    def train_advisor(self, training_data=None):
        """Train AI model with sample data or provided data"""
        if training_data is None:
            # Generate synthetic training data
            np.random.seed(42)
            n_samples = 1000
            
            training_data = pd.DataFrame({
                'loan_amount': np.random.uniform(10000, 500000, n_samples),
                'interest_rate': np.random.uniform(2, 15, n_samples),
                'loan_term': np.random.randint(1, 30, n_samples),
                'credit_score': np.random.randint(300, 850, n_samples),
                'monthly_income': np.random.uniform(2000, 20000, n_samples),
                'monthly_expenses': np.random.uniform(1000, 10000, n_samples),
                'risk_level': np.random.choice(['low', 'medium', 'high'], n_samples)
            })
            
            # Calculate target variable (optimal extra payment)
            training_data['optimal_extra_payment'] = training_data.apply(
                lambda x: self._calculate_optimal_extra_payment(x), axis=1
            )
        
        # Prepare features - define the exact column order
        numeric_features = ['loan_amount', 'interest_rate', 'loan_term', 
                           'credit_score', 'monthly_income', 'monthly_expenses']
        
        # Convert categorical variables
        risk_dummies = pd.get_dummies(training_data['risk_level'], prefix='risk')
        
        # Ensure all risk columns are present
        for risk in ['risk_high', 'risk_low', 'risk_medium']:
            if risk not in risk_dummies.columns:
                risk_dummies[risk] = 0
        
        # Combine features in specific order
        features = pd.concat([training_data[numeric_features], risk_dummies], axis=1)
        
        # Store the feature columns for consistent transformation
        self.feature_columns = features.columns.tolist()
        
        target = training_data['optimal_extra_payment']
        
        # Scale features
        features_scaled = self.scaler.fit_transform(features)
        
        # Train model
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(features_scaled, target)
        self.trained = True
        
        return self.model
    
    def _calculate_optimal_extra_payment(self, row):
        """Calculate optimal extra payment based on financial parameters"""
        disposable_income = row['monthly_income'] - row['monthly_expenses']
        max_affordable = disposable_income * 0.3  # Don't recommend more than 30% of disposable income
        
        # Higher interest rates warrant higher extra payments
        interest_factor = min(row['interest_rate'] / 5, 3)  # Cap at 3x
        
        # Lower credit scores might need more conservative recommendations
        credit_factor = max(row['credit_score'] / 850, 0.5)
        
        optimal = min(max_affordable * interest_factor * credit_factor, 
                     row['loan_amount'] * 0.1)  # Cap at 10% of loan amount
        
        return optimal
    
    def get_recommendations(self, loan_data):
        """Get AI-powered recommendations for loan repayment"""
        if not self.trained:
            self.train_advisor()
        
        # Prepare input data with consistent feature order
        input_features = pd.DataFrame([{
            'loan_amount': loan_data['principal'],
            'interest_rate': loan_data['annual_rate'],
            'loan_term': loan_data['years'],
            'credit_score': loan_data.get('credit_score', 700),
            'monthly_income': loan_data.get('monthly_income', 5000),
            'monthly_expenses': loan_data.get('monthly_expenses', 3000),
            'risk_level': loan_data.get('risk_level', 'medium')
        }])
        
        # Add risk level dummies
        risk_dummies = pd.get_dummies(input_features['risk_level'], prefix='risk')
        
        # Ensure all risk columns are present in the same order as training
        for risk in ['risk_high', 'risk_low', 'risk_medium']:
            if risk not in risk_dummies.columns:
                risk_dummies[risk] = 0
        
        # Combine features
        numeric_features = ['loan_amount', 'interest_rate', 'loan_term', 
                           'credit_score', 'monthly_income', 'monthly_expenses']
        
        input_features_combined = pd.concat([input_features[numeric_features], risk_dummies], axis=1)
        
        # Ensure the columns are in the same order as during training
        input_features_combined = input_features_combined[self.feature_columns]
        
        # Scale features
        input_scaled = self.scaler.transform(input_features_combined)
        
        # Get prediction
        recommended_extra = self.model.predict(input_scaled)[0]
        
        # Generate recommendations
        recommendations = self._generate_detailed_recommendations(loan_data, recommended_extra)
        
        return recommendations
    
    def _generate_detailed_recommendations(self, loan_data, recommended_extra):
        """Generate detailed repayment recommendations"""
        from loan_calculator import LoanCalculator
        calculator = LoanCalculator()
        
        # Calculate impact of recommended extra payment
        impact = calculator.calculate_early_payoff_impact(
            loan_data['principal'],
            loan_data['annual_rate'],
            loan_data['years'],
            recommended_extra
        )
        
        recommendations = {
            'recommended_extra_payment': round(recommended_extra, 2),
            'months_saved': impact['months_saved'],
            'interest_saved': round(impact['interest_saved'], 2),
            'strategy': self._get_repayment_strategy(loan_data, recommended_extra),
            'risk_assessment': self._assess_risk(loan_data),
            'timeline_improvement': f"Pay off {impact['months_saved']} months early"
        }
        
        return recommendations
    
    def _get_repayment_strategy(self, loan_data, extra_payment):
        """Determine optimal repayment strategy"""
        strategies = []
        
        if loan_data['annual_rate'] > 8:
            strategies.append("Aggressive repayment (high interest rate)")
        elif loan_data['annual_rate'] < 5:
            strategies.append("Consider investing excess funds (low interest rate)")
        
        if extra_payment > loan_data.get('monthly_income', 5000) * 0.2:
            strategies.append("Conservative extra payments recommended")
        else:
            strategies.append("Moderate extra payments sustainable")
        
        if loan_data.get('credit_score', 700) < 650:
            strategies.append("Focus on credit improvement alongside repayment")
        
        return strategies
    
    def _assess_risk(self, loan_data):
        """Assess financial risk of the loan"""
        from loan_calculator import LoanCalculator
        monthly_payment = LoanCalculator().calculate_monthly_payment(
            loan_data['principal'],
            loan_data['annual_rate'],
            loan_data['years']
        )
        
        debt_to_income = monthly_payment / loan_data.get('monthly_income', 5000)
        
        if debt_to_income > 0.4:
            return "High risk - debt exceeds 40% of income"
        elif debt_to_income > 0.3:
            return "Medium risk - monitor budget closely"
        else:
            return "Low risk - manageable debt level"