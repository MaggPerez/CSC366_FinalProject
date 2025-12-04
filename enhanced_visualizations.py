"""
Enhanced Visualization Module with Interpretations

This module creates all visualizations with proper context, interpretations,
and statistical annotations. Visualizations are designed to tell a cohesive
story about NBA player and team performance.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Set style for professional-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10


"""Create visualizations directory if it doesn't exist"""
def ensure_viz_directory():
    os.makedirs('visualizations', exist_ok=True)


"""
Convert height like '6-6' to total inches
Returns None for invalid values
"""
def height_to_inches(h):

    if pd.isna(h):
        return None
    if isinstance(h, (int, float)):
        return h
    h = str(h)
    if "-" not in h:
        return None
    try:
        feet, inches = h.split("-")
        return int(feet) * 12 + int(inches)
    except Exception:
        return None


"""
Create comprehensive player analysis visualizations

Visualizations:
1. Height distribution histogram
2. Weight distribution histogram
3. Position frequency bar chart
4. Players per team bar chart
5. Average height by position
6. Average weight by position
"""
def create_player_visualizations():

    df_players = pd.read_csv("cleaned_csv/ACTIVE_PLAYERS_CLEANED.csv")

    # Convert height and weight
    df_players["height_in"] = df_players["height"].apply(height_to_inches)
    df_players["weight"] = pd.to_numeric(df_players["weight"], errors="coerce")



    # 1. HEIGHT DISTRIBUTION
    plt.figure(figsize=(12, 6))
    heights = df_players["height_in"].dropna()
    plt.hist(heights, bins=25, edgecolor='black', alpha=0.7, color='steelblue')
    plt.axvline(heights.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {heights.mean():.1f}"')
    plt.axvline(heights.median(), color='green', linestyle='--', linewidth=2, label=f'Median: {heights.median():.1f}"')
    
    
    # Adding labels and title
    plt.xlabel("Height (inches)", fontsize=12, fontweight='bold')
    plt.ylabel("Number of Players", fontsize=12, fontweight='bold')
    plt.title("Distribution of NBA Player Heights\n(Approximately Normal with Slight Right Skew)",
              fontsize=14, fontweight='bold', pad=20)
    plt.legend()
    plt.grid(axis='y', alpha=0.3)


    # Add interpretation text box
    interpretation = (f"Mean: {heights.mean():.1f}\" | Median: {heights.median():.1f}\" | Std: {heights.std():.1f}\"\n"
                     f"Range: {heights.min():.0f}\" to {heights.max():.0f}\" ({heights.max()-heights.min():.0f}\" spread)")
    
    
    
    plt.text(0.02, 0.98, interpretation, transform=plt.gca().transAxes,
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
             verticalalignment='top', fontsize=10, family='monospace')

    plt.tight_layout()
    
    
    # saving the figure
    plt.savefig('visualizations/1_height_distribution.png', dpi=300, bbox_inches='tight')
    print("Saved: visualizations/1_height_distribution.png")
    plt.close()









    # 2. WEIGHT DISTRIBUTION
    plt.figure(figsize=(12, 6))
    weights = df_players["weight"].dropna()
    plt.hist(weights, bins=25, edgecolor='black', alpha=0.7, color='coral')
    plt.axvline(weights.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {weights.mean():.1f} lbs')
    plt.axvline(weights.median(), color='green', linestyle='--', linewidth=2, label=f'Median: {weights.median():.1f} lbs')
    
    
    # Adding labels and title
    plt.xlabel("Weight (lbs)", fontsize=12, fontweight='bold')
    plt.ylabel("Number of Players", fontsize=12, fontweight='bold')
    plt.title("Distribution of NBA Player Weights\n(Bell-Shaped with Some Heavier Outliers)",
              fontsize=14, fontweight='bold', pad=20)
    plt.legend()
    plt.grid(axis='y', alpha=0.3)



    # Add interpretation text box
    interpretation = (f"Mean: {weights.mean():.1f} lbs | Median: {weights.median():.1f} lbs | Std: {weights.std():.1f}\n"
                     f"Range: {weights.min():.0f} to {weights.max():.0f} lbs")
    plt.text(0.02, 0.98, interpretation, transform=plt.gca().transAxes,
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
             verticalalignment='top', fontsize=10, family='monospace')

    plt.tight_layout()
    
    
    
    # saving the figure
    plt.savefig('visualizations/2_weight_distribution.png', dpi=300, bbox_inches='tight')
    print("Saved: visualizations/2_weight_distribution.png")
    plt.close()








    # 3. POSITION FREQUENCY
    plt.figure(figsize=(10, 6))
    position_counts = df_players["position"].value_counts().sort_values(ascending=False)
    colors = sns.color_palette("husl", len(position_counts))
    
    
    # Create bar chart
    bars = plt.bar(position_counts.index, position_counts.values, color=colors, edgecolor='black')

    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontweight='bold')


    # Adding labels and title
    plt.xlabel("Position", fontsize=12, fontweight='bold')
    plt.ylabel("Number of Players", fontsize=12, fontweight='bold')
    plt.title("Active NBA Players by Position\n(Relatively Balanced Distribution Across Positions)",
              fontsize=14, fontweight='bold', pad=20)
    
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    
    
    
    # saving the figure
    plt.savefig('visualizations/3_position_distribution.png', dpi=300, bbox_inches='tight')
    print("Saved: visualizations/3_position_distribution.png")
    plt.close()



    # 4. PLAYERS PER TEAM
    plt.figure(figsize=(14, 7))
    team_counts = df_players["team.full_name"].value_counts().sort_values(ascending=False)
    plt.bar(range(len(team_counts)), team_counts.values, color='teal', edgecolor='black', alpha=0.7)
    
    
    
    # the labels and title
    plt.xlabel("Teams (sorted by player count)", fontsize=12, fontweight='bold')
    plt.ylabel("Number of Players", fontsize=12, fontweight='bold')
    plt.title("Active Players per Team\n(Most Teams Maintain ~13-17 Player Rosters)",
              fontsize=14, fontweight='bold', pad=20)
    plt.axhline(team_counts.mean(), color='red', linestyle='--', linewidth=2,
                label=f'Average: {team_counts.mean():.1f} players')
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    
    # Hide x-tick labels for clarity
    plt.xticks([])  
    plt.tight_layout()
    
    
    
    # saving the figure
    plt.savefig('visualizations/4_players_per_team.png', dpi=300, bbox_inches='tight')
    print("Saved: visualizations/4_players_per_team.png")
    plt.close()



    # 5. AVERAGE HEIGHT BY POSITION
    plt.figure(figsize=(10, 6))
    height_by_pos = (df_players.dropna(subset=['height_in'])
                     .groupby('position')['height_in']
                     .agg(['mean', 'std']))
    height_by_pos = height_by_pos.sort_values('mean', ascending=False)

    # Replace NaN std with 0 for positions with only 1 player
    height_by_pos['std'] = height_by_pos['std'].fillna(0)


    # Create bar chart with error bars
    bars = plt.bar(height_by_pos.index, height_by_pos['mean'],
                   yerr=height_by_pos['std'], capsize=5,
                   color='skyblue', edgecolor='black', alpha=0.8)

    # Add value labels
    for i, (pos, row) in enumerate(height_by_pos.iterrows()):
        # For positions with std=0 (only 1 player), use fixed offset; otherwise use std + offset
        if row['std'] == 0:
            y_position = row['mean'] + 2.0  # Fixed offset for single-player positions
        else:
            y_position = row['mean'] + row['std'] + 0.5
        plt.text(i, y_position, f"{row['mean']:.1f}\"",
                ha='center', fontweight='bold')



    # titles and labels
    plt.xlabel("Position", fontsize=12, fontweight='bold')
    plt.ylabel("Average Height (inches)", fontsize=12, fontweight='bold')
    plt.title("Average Height by Position with Standard Deviation\n(Clear Hierarchical Pattern: Centers Tallest, Guards Shortest)",
              fontsize=14, fontweight='bold', pad=20)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    
    
    # saving the figure
    plt.savefig('visualizations/5_height_by_position.png', dpi=300, bbox_inches='tight')
    print("Saved: visualizations/5_height_by_position.png")
    plt.close()



    # 6. AVERAGE WEIGHT BY POSITION
    plt.figure(figsize=(10, 6))
    
    
    # Calculate average weight and std dev by position
    weight_by_pos = (df_players.dropna(subset=['weight']).groupby('position')['weight'].agg(['mean', 'std']))
    
    
    # Sort by mean weight
    weight_by_pos = weight_by_pos.sort_values('mean', ascending=False)

    # Replace NaN std with 0 for positions with only 1 player
    weight_by_pos['std'] = weight_by_pos['std'].fillna(0)



    # Create bar chart with error bars
    bars = plt.bar(weight_by_pos.index, weight_by_pos['mean'], yerr=weight_by_pos['std'], capsize=5, color='salmon', 
                   edgecolor='black', alpha=0.8)

    # Add value labels
    for i, (pos, row) in enumerate(weight_by_pos.iterrows()):
        # For positions with std=0 (only 1 player), use fixed offset; otherwise use std + offset
        if row['std'] == 0:
            y_position = row['mean'] + 10  # Fixed offset for single-player positions
        else:
            y_position = row['mean'] + row['std'] + 2
        plt.text(i, y_position, f"{row['mean']:.0f} lbs",
                ha='center', fontweight='bold')


    # titles and labels
    plt.xlabel("Position", fontsize=12, fontweight='bold')
    plt.ylabel("Average Weight (lbs)", fontsize=12, fontweight='bold')
    plt.title("Average Weight by Position with Standard Deviation\n(Weight Correlates with Position Requirements)",
              fontsize=14, fontweight='bold', pad=20)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    
    
    
    # saving the figure
    plt.savefig('visualizations/6_weight_by_position.png', dpi=300, bbox_inches='tight')
    print("Saved: visualizations/6_weight_by_position.png")
    plt.close()