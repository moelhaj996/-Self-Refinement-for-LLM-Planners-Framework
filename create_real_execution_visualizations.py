"""
Create visualizations from real SRLP framework execution results.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Set style for professional plots
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

# Create output directory
os.makedirs('results/real_execution_visualizations', exist_ok=True)

def load_real_data():
    """Load the real execution results."""
    data_file = 'results/real_execution/combined_real_execution_results.csv'
    return pd.read_csv(data_file)

def create_scenario_performance_chart():
    """Create scenario performance comparison from real data."""
    df = load_real_data()
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('SRLP Framework - Real Execution Results', fontsize=20, fontweight='bold', y=0.98)
    
    # 1. Initial vs Final Quality by Scenario
    scenarios = df['scenario'].str.capitalize()
    x_pos = np.arange(len(scenarios))
    width = 0.35
    
    bars1 = ax1.bar(x_pos - width/2, df['initial_quality'], width, 
                   label='Initial Quality', color='lightcoral', alpha=0.8, edgecolor='black')
    bars2 = ax1.bar(x_pos + width/2, df['final_quality'], width,
                   label='Final Quality', color='lightblue', alpha=0.8, edgecolor='black')
    
    ax1.set_title('Quality Scores by Scenario', fontsize=14, fontweight='bold', pad=20)
    ax1.set_xlabel('Scenario', fontsize=12)
    ax1.set_ylabel('Quality Score', fontsize=12)
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(scenarios, rotation=45)
    ax1.legend()
    ax1.set_ylim(0, 1)
    
    # Add value labels
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{height:.3f}', ha='center', va='bottom', fontsize=9)
    for bar in bars2:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{height:.3f}', ha='center', va='bottom', fontsize=9)
    
    # 2. Quality Improvement by Scenario
    colors = ['green' if x > 0 else 'red' if x < 0 else 'gray' for x in df['improvement']]
    bars3 = ax2.bar(scenarios, df['improvement'], color=colors, alpha=0.7, edgecolor='black')
    
    ax2.set_title('Quality Improvement by Scenario', fontsize=14, fontweight='bold', pad=20)
    ax2.set_xlabel('Scenario', fontsize=12)
    ax2.set_ylabel('Quality Improvement', fontsize=12)
    ax2.tick_params(axis='x', rotation=45)
    ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    
    # Add value labels
    for bar, value in zip(bars3, df['improvement']):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + (0.001 if height >= 0 else -0.002),
                f'{value:+.3f}', ha='center', va='bottom' if height >= 0 else 'top', 
                fontweight='bold', fontsize=10)
    
    # 3. Processing Time Analysis
    bars4 = ax3.bar(scenarios, df['time_seconds'], color='lightgreen', alpha=0.8, edgecolor='black')
    
    ax3.set_title('Processing Time by Scenario', fontsize=14, fontweight='bold', pad=20)
    ax3.set_xlabel('Scenario', fontsize=12)
    ax3.set_ylabel('Time (seconds)', fontsize=12)
    ax3.tick_params(axis='x', rotation=45)
    
    # Add value labels
    for bar, value in zip(bars4, df['time_seconds']):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 0.001,
                f'{value:.3f}s', ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # 4. Quality Change Distribution
    quality_dist = df['quality_change_category'].value_counts()
    colors_pie = ['lightgreen', 'lightcoral', 'lightgray']
    wedges, texts, autotexts = ax4.pie(quality_dist.values, labels=quality_dist.index, 
                                      autopct='%1.1f%%', colors=colors_pie, startangle=90)
    
    ax4.set_title('Quality Change Distribution', fontsize=14, fontweight='bold', pad=20)
    
    # Make percentage text bold
    for autotext in autotexts:
        autotext.set_fontweight('bold')
        autotext.set_fontsize(11)
    
    plt.tight_layout()
    plt.savefig('results/real_execution_visualizations/scenario_performance_real.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print("✅ Created: scenario_performance_real.png")

def create_framework_performance_summary():
    """Create overall framework performance summary."""
    df = load_real_data()
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('SRLP Framework Performance Summary - Real Execution', 
                 fontsize=18, fontweight='bold', y=0.98)
    
    # 1. Quality Metrics Summary
    metrics = ['Initial Quality', 'Final Quality', 'Average Improvement']
    values = [df['initial_quality'].mean(), df['final_quality'].mean(), df['improvement'].mean()]
    colors = ['lightblue', 'lightgreen', 'orange']
    
    bars1 = ax1.bar(metrics, values, color=colors, alpha=0.8, edgecolor='black')
    ax1.set_title('Overall Quality Metrics', fontsize=14, fontweight='bold', pad=20)
    ax1.set_ylabel('Score', fontsize=12)
    ax1.tick_params(axis='x', rotation=45)
    
    # Add value labels
    for bar, value in zip(bars1, values):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.005,
                f'{value:.3f}', ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    # 2. Scenario Complexity vs Performance
    ax2.scatter(df['scenario_complexity'], df['final_quality'], 
               s=200, c=df['improvement'], cmap='RdYlGn', alpha=0.8, 
               edgecolors='black', linewidth=2)
    
    # Add scenario labels
    for i, scenario in enumerate(df['scenario']):
        ax2.annotate(scenario.capitalize(), 
                    (df.iloc[i]['scenario_complexity'], df.iloc[i]['final_quality']),
                    xytext=(5, 5), textcoords='offset points', fontsize=9,
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))
    
    ax2.set_title('Scenario Complexity vs Final Quality', fontsize=14, fontweight='bold', pad=20)
    ax2.set_xlabel('Scenario Complexity', fontsize=12)
    ax2.set_ylabel('Final Quality Score', fontsize=12)
    ax2.grid(True, alpha=0.3)
    
    # Add colorbar
    cbar = plt.colorbar(ax2.collections[0], ax=ax2)
    cbar.set_label('Quality Improvement', fontsize=10)
    
    # 3. Efficiency Analysis
    efficiency = df['quality_per_second']
    bars3 = ax3.bar(df['scenario'].str.capitalize(), efficiency, 
                   color='lightcoral', alpha=0.8, edgecolor='black')
    
    ax3.set_title('Quality per Second (Efficiency)', fontsize=14, fontweight='bold', pad=20)
    ax3.set_xlabel('Scenario', fontsize=12)
    ax3.set_ylabel('Quality/Second', fontsize=12)
    ax3.tick_params(axis='x', rotation=45)
    
    # Add value labels
    for bar, value in zip(bars3, efficiency):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{value:.1f}', ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # 4. Framework Statistics
    ax4.axis('off')
    
    # Calculate key statistics
    total_evaluations = len(df)
    avg_improvement = df['improvement'].mean()
    improvement_rate = (df['improvement'] > 0).sum() / len(df) * 100
    avg_time = df['time_seconds'].mean()
    best_scenario = df.loc[df['final_quality'].idxmax(), 'scenario'].capitalize()
    
    stats_text = f"""
    Framework Performance Statistics
    
    📊 Total Evaluations: {total_evaluations}
    📈 Average Improvement: {avg_improvement:+.3f}
    ✅ Improvement Rate: {improvement_rate:.1f}%
    ⏱️  Average Processing Time: {avg_time:.3f}s
    🏆 Best Performing Scenario: {best_scenario}
    
    🤖 LLM Provider: Mock (Testing)
    🔄 Max Iterations: 3
    📋 Scenarios Tested: {df['scenario'].nunique()}
    """
    
    ax4.text(0.5, 0.5, stats_text, fontsize=12, ha='center', va='center',
            transform=ax4.transAxes, 
            bbox=dict(boxstyle='round,pad=1', facecolor='lightgray', alpha=0.3))
    
    plt.tight_layout()
    plt.savefig('results/real_execution_visualizations/framework_performance_summary.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print("✅ Created: framework_performance_summary.png")

def create_detailed_analysis_chart():
    """Create detailed analysis of the framework execution."""
    df = load_real_data()
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('SRLP Framework - Detailed Execution Analysis', 
                 fontsize=18, fontweight='bold', y=0.98)
    
    # 1. Before vs After Quality Comparison
    scenarios = df['scenario'].str.capitalize()
    x = np.arange(len(scenarios))
    
    # Create connected line plot
    for i in range(len(df)):
        ax1.plot([i, i], [df.iloc[i]['initial_quality'], df.iloc[i]['final_quality']], 
                'o-', linewidth=3, markersize=8, alpha=0.7,
                color='green' if df.iloc[i]['improvement'] > 0 else 'red')
    
    ax1.scatter(x, df['initial_quality'], s=100, color='lightcoral', 
               label='Initial Quality', alpha=0.8, edgecolors='black', zorder=5)
    ax1.scatter(x, df['final_quality'], s=100, color='lightblue', 
               label='Final Quality', alpha=0.8, edgecolors='black', zorder=5)
    
    ax1.set_title('Quality Improvement Trajectories', fontsize=14, fontweight='bold', pad=20)
    ax1.set_xlabel('Scenario', fontsize=12)
    ax1.set_ylabel('Quality Score', fontsize=12)
    ax1.set_xticks(x)
    ax1.set_xticklabels(scenarios, rotation=45)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0.4, 0.7)
    
    # 2. Improvement vs Complexity Analysis
    ax2.scatter(df['scenario_complexity'], df['improvement'], 
               s=df['time_seconds']*2000, alpha=0.6, 
               c=df['final_quality'], cmap='viridis', edgecolors='black', linewidth=2)
    
    # Add trend line
    z = np.polyfit(df['scenario_complexity'], df['improvement'], 1)
    p = np.poly1d(z)
    ax2.plot(df['scenario_complexity'], p(df['scenario_complexity']), 
            "r--", alpha=0.8, linewidth=2)
    
    ax2.set_title('Complexity vs Improvement (Bubble = Time)', fontsize=14, fontweight='bold', pad=20)
    ax2.set_xlabel('Scenario Complexity', fontsize=12)
    ax2.set_ylabel('Quality Improvement', fontsize=12)
    ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    ax2.grid(True, alpha=0.3)
    
    # Add colorbar
    cbar = plt.colorbar(ax2.collections[0], ax=ax2)
    cbar.set_label('Final Quality', fontsize=10)
    
    # 3. Performance Categories
    perf_categories = df['performance_category'].value_counts()
    colors = ['lightgreen', 'orange', 'lightcoral']
    
    wedges, texts, autotexts = ax3.pie(perf_categories.values, labels=perf_categories.index,
                                      autopct='%1.1f%%', colors=colors, startangle=90)
    
    ax3.set_title('Performance Categories Distribution', fontsize=14, fontweight='bold', pad=20)
    
    # Make text bold
    for autotext in autotexts:
        autotext.set_fontweight('bold')
        autotext.set_fontsize(11)
    
    # 4. Iteration Analysis
    iterations = df['iterations']
    scenarios_iter = df['scenario'].str.capitalize()
    
    bars4 = ax4.bar(scenarios_iter, iterations, color='lightsteelblue', 
                   alpha=0.8, edgecolor='black')
    
    ax4.set_title('Refinement Iterations by Scenario', fontsize=14, fontweight='bold', pad=20)
    ax4.set_xlabel('Scenario', fontsize=12)
    ax4.set_ylabel('Number of Iterations', fontsize=12)
    ax4.tick_params(axis='x', rotation=45)
    ax4.set_ylim(0, max(iterations) + 0.5)
    
    # Add value labels
    for bar, value in zip(bars4, iterations):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                f'{int(value)}', ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    plt.tight_layout()
    plt.savefig('results/real_execution_visualizations/detailed_analysis.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print("✅ Created: detailed_analysis.png")

def create_execution_dashboard():
    """Create comprehensive execution dashboard."""
    df = load_real_data()
    
    # Create large dashboard figure
    fig = plt.figure(figsize=(20, 16))
    fig.suptitle('SRLP Framework - Real Execution Dashboard', fontsize=24, fontweight='bold', y=0.98)
    
    # Create grid layout
    gs = fig.add_gridspec(4, 4, hspace=0.3, wspace=0.3)
    
    # 1. Main Performance Chart (top-left, 2x2)
    ax1 = fig.add_subplot(gs[0:2, 0:2])
    
    scenarios = df['scenario'].str.capitalize()
    x_pos = np.arange(len(scenarios))
    width = 0.35
    
    bars1 = ax1.bar(x_pos - width/2, df['initial_quality'], width, 
                   label='Initial', color='lightcoral', alpha=0.8, edgecolor='black')
    bars2 = ax1.bar(x_pos + width/2, df['final_quality'], width,
                   label='Final', color='lightgreen', alpha=0.8, edgecolor='black')
    
    ax1.set_title('Quality Scores: Before vs After Refinement', fontsize=16, fontweight='bold')
    ax1.set_xlabel('Scenario', fontsize=12)
    ax1.set_ylabel('Quality Score', fontsize=12)
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(scenarios, rotation=45)
    ax1.legend(fontsize=12)
    ax1.set_ylim(0, 0.8)
    
    # Add improvement arrows
    for i, (initial, final) in enumerate(zip(df['initial_quality'], df['final_quality'])):
        if final > initial:
            ax1.annotate('', xy=(i, final + 0.02), xytext=(i, initial - 0.02),
                        arrowprops=dict(arrowstyle='->', color='green', lw=2))
        elif final < initial:
            ax1.annotate('', xy=(i, final - 0.02), xytext=(i, initial + 0.02),
                        arrowprops=dict(arrowstyle='->', color='red', lw=2))
    
    # 2. Key Metrics (top-right, 2x1)
    ax2 = fig.add_subplot(gs[0, 2:4])
    ax2.axis('off')
    
    # Calculate key metrics
    total_evals = len(df)
    avg_improvement = df['improvement'].mean()
    success_rate = (df['improvement'] > 0).sum() / len(df) * 100
    avg_time = df['time_seconds'].mean()
    
    metrics_text = f"""
    📊 EXECUTION METRICS
    
    Total Evaluations: {total_evals}
    Average Improvement: {avg_improvement:+.3f}
    Success Rate: {success_rate:.1f}%
    Avg Processing Time: {avg_time:.3f}s
    """
    
    ax2.text(0.5, 0.5, metrics_text, fontsize=14, ha='center', va='center',
            transform=ax2.transAxes, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.3))
    
    # 3. Improvement Distribution (middle-right, 1x2)
    ax3 = fig.add_subplot(gs[1, 2:4])
    
    improvements = df['improvement']
    colors = ['green' if x > 0 else 'red' if x < 0 else 'gray' for x in improvements]
    
    bars3 = ax3.bar(scenarios, improvements, color=colors, alpha=0.7, edgecolor='black')
    ax3.set_title('Quality Improvement by Scenario', fontsize=14, fontweight='bold')
    ax3.set_ylabel('Improvement', fontsize=12)
    ax3.tick_params(axis='x', rotation=45)
    ax3.axhline(y=0, color='black', linestyle='-', alpha=0.5)
    
    # Add value labels
    for bar, value in zip(bars3, improvements):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., 
                height + (0.001 if height >= 0 else -0.002),
                f'{value:+.3f}', ha='center', 
                va='bottom' if height >= 0 else 'top', 
                fontweight='bold', fontsize=10)
    
    # 4. Processing Time Analysis (bottom-left, 1x2)
    ax4 = fig.add_subplot(gs[2, 0:2])
    
    bars4 = ax4.bar(scenarios, df['time_seconds'], color='lightsteelblue', 
                   alpha=0.8, edgecolor='black')
    
    ax4.set_title('Processing Time by Scenario', fontsize=14, fontweight='bold')
    ax4.set_xlabel('Scenario', fontsize=12)
    ax4.set_ylabel('Time (seconds)', fontsize=12)
    ax4.tick_params(axis='x', rotation=45)
    
    # Add value labels
    for bar, value in zip(bars4, df['time_seconds']):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height + 0.001,
                f'{value:.3f}s', ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # 5. Quality Distribution (bottom-right, 1x2)
    ax5 = fig.add_subplot(gs[2, 2:4])
    
    quality_dist = df['quality_change_category'].value_counts()
    colors_pie = ['lightgreen', 'lightcoral', 'lightgray']
    
    wedges, texts, autotexts = ax5.pie(quality_dist.values, labels=quality_dist.index,
                                      autopct='%1.1f%%', colors=colors_pie, startangle=90)
    
    ax5.set_title('Quality Change Distribution', fontsize=14, fontweight='bold')
    
    for autotext in autotexts:
        autotext.set_fontweight('bold')
        autotext.set_fontsize(11)
    
    # 6. Framework Information (bottom, full width)
    ax6 = fig.add_subplot(gs[3, :])
    ax6.axis('off')
    
    framework_info = f"""
    🤖 FRAMEWORK INFORMATION
    
    LLM Provider: Mock (Testing Mode)  |  Model: mock-model  |  Max Iterations: 3  |  Scenarios: {df['scenario'].nunique()}
    
    Framework Status: ✅ Operational  |  Convergence Rate: {(df['converged'].sum() / len(df) * 100):.1f}%  |  
    Average Quality: {df['final_quality'].mean():.3f}  |  Best Scenario: {df.loc[df['final_quality'].idxmax(), 'scenario'].capitalize()}
    """
    
    ax6.text(0.5, 0.5, framework_info, fontsize=12, ha='center', va='center',
            transform=ax6.transAxes,
            bbox=dict(boxstyle='round,pad=1', facecolor='lightgray', alpha=0.3))
    
    plt.savefig('results/real_execution_visualizations/execution_dashboard.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print("✅ Created: execution_dashboard.png")

def generate_all_real_visualizations():
    """Generate all visualization charts from real execution data."""
    print("🎨 Creating Real Execution Visualizations...")
    print("=" * 60)
    
    create_scenario_performance_chart()
    create_framework_performance_summary()
    create_detailed_analysis_chart()
    create_execution_dashboard()
    
    print("=" * 60)
    print("🎉 All real execution visualizations created successfully!")
    print("📁 Saved to: results/real_execution_visualizations/")
    print("\n📊 Generated Charts:")
    print("   1. scenario_performance_real.png")
    print("   2. framework_performance_summary.png")
    print("   3. detailed_analysis.png")
    print("   4. execution_dashboard.png")

if __name__ == "__main__":
    generate_all_real_visualizations()

