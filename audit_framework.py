import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set visual style
sns.set_style("whitegrid")

def simulate_data():
    """
    Simulates A/B test logs with engineered bias to represent a 'nudge' test.
    
    Returns:
        pd.DataFrame: Simulated audit data.
    """
    print("Simulating Audit Data...")
    
    # --- A/B Test Results Simulation ---
    n_users = 1000
    df_ab = pd.DataFrame({
        'UserID': range(1000, 1000 + n_users),
        'Test_Group': np.random.choice(['A', 'B'], size=n_users, p=[0.5, 0.5]),
        # Platform Goal: 25% base rate
        'Platform_Goal_Achieved': np.random.choice([0, 1], size=n_users, p=[0.75, 0.25]),
        # Comprehension: Base average of 7/10
        'User_Comprehension_Score': np.random.normal(loc=7, scale=1.5, size=n_users),
        # Feature scores (1-10 scale)
        'OptOut_Difficulty_Score': np.random.randint(1, 10, size=n_users),
        'Urgency_Messaging_Score': np.random.randint(1, 10, size=n_users),
    })

    # Inject bias for Test B (the 'nudge' test)
    # Test B has higher goal achievement and lower comprehension (the ethical cost)
    mask_b = df_ab['Test_Group'] == 'B'
    df_ab.loc[mask_b, 'Platform_Goal_Achieved'] = np.random.choice([0, 1], size=mask_b.sum(), p=[0.65, 0.35])
    df_ab.loc[mask_b, 'User_Comprehension_Score'] -= 1.0 
    df_ab.loc[mask_b, 'Urgency_Messaging_Score'] = df_ab.loc[mask_b, 'Urgency_Messaging_Score'].clip(1, 8) + 2.0
    
    # Clean up scores
    df_ab['User_Comprehension_Score'] = df_ab['User_Comprehension_Score'].clip(1, 10).round(1)
    df_ab['Urgency_Messaging_Score'] = df_ab['Urgency_Messaging_Score'].clip(1, 10)
    
    return df_ab

def calculate_autonomy_deficit(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the Nudge Autonomy Deficit (NAD) score based on weighted interface features.
    """
    print("Calculating Nudge Autonomy Deficit (NAD) Scores...")
    
    # Customizable Weights (The ethical framework)
    WEIGHTS = {
        'OptOut_Difficulty_Score': 0.4, 
        'Urgency_Messaging_Score': 0.5, # Combined weight for urgency and default bias
    }

    # NAD Score: Higher score = less user autonomy
    df['NAD_Score'] = (
        df['OptOut_Difficulty_Score'] * WEIGHTS['OptOut_Difficulty_Score'] +
        df['Urgency_Messaging_Score'] * WEIGHTS['Urgency_Messaging_Score']
    )
    
    # Normalize for easier comparison (1.0 = Max theoretical coercion)
    max_possible_score = (10 * 0.4) + (10 * 0.5) 
    df['NAD_Score_Normalized'] = (df['NAD_Score'] / max_possible_score)
    
    return df

def generate_visualization(df: pd.DataFrame):
    """
    Generates a chart quantifying the ethical trade-off (Platform Gain vs. User Cost).
    """
    print("Generating Ethical Trade-Off Visualization...")

    # 1. Calculate Core Metrics by Test Group
    group_metrics = df.groupby('Test_Group').agg(
        Goal_Rate=('Platform_Goal_Achieved', 'mean'),
        Comprehension_Avg=('User_Comprehension_Score', 'mean'),
    ).reset_index()

    # Calculate the difference (Test B - Test A)
    # Platform Gain (Nudge Effect)
    nudge_effect = (group_metrics.loc[group_metrics['Test_Group'] == 'B', 'Goal_Rate'].iloc[0] - 
                    group_metrics.loc[group_metrics['Test_Group'] == 'A', 'Goal_Rate'].iloc[0]) * 100

    # User Cost (Ethical Cost)
    ethical_cost = (group_metrics.loc[group_metrics['Test_Group'] == 'A', 'Comprehension_Avg'].iloc[0] - 
                    group_metrics.loc[group_metrics['Test_Group'] == 'B', 'Comprehension_Avg'].iloc[0])

    # Prepare data for the chart
    tradeoff_data = pd.DataFrame({
        'Metric': ['Platform Goal Increase (%)', 'User Comprehension Drop (Points)'],
        'Value': [nudge_effect, ethical_cost],
        'Type': ['Platform Gain (Desired)', 'User Cost (Ethical Concern)']
    })

    # Create the visualization
    plt.figure(figsize=(10, 6))
    chart = sns.barplot(
        x='Metric', 
        y='Value', 
        hue='Type', 
        data=tradeoff_data, 
        palette={'Platform Gain (Desired)': 'g', 'User Cost (Ethical Concern)': 'r'},
        dodge=False
    )
    
    # Add value labels
    for p in chart.patches:
        chart.annotate(f'{p.get_height():.2f}', 
                       (p.get_x() + p.get_width() / 2., p.get_height()), 
                       ha='center', va='center', xytext=(0, 9), textcoords='offset points')

    plt.title('Ethical Trade-Off: Platform Optimization vs. User Autonomy', fontsize=14)
    plt.ylabel('Magnitude of Change', fontsize=12)
    plt.xlabel('Metric', fontsize=12)
    plt.legend(title='Impact Type')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    # 1. Load or Simulate Data
    audit_data = simulate_data()
    
    # 2. Score Autonomy
    scored_data = calculate_autonomy_deficit(audit_data)
    
    # Display average NAD scores for comparison
    print("\n--- Average Nudge Autonomy Deficit (NAD) Scores ---")
    print(scored_data.groupby('Test_Group')['NAD_Score'].mean().round(2))
    
    # 3. Visualize Ethical Trade-off
    generate_visualization(scored_data)
    
    print("\nAudit Complete.")
