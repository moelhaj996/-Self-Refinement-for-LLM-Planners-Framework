"""
Create comprehensive visualizations for multi-provider LLM comparison.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Set style for professional plots
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("Set2")

# Create output directory
os.makedirs('results/multi_provider_visualizations', exist_ok=True)

def load_comparison_data():
    """Load the multi-provider comparison data."""
    return pd.read_csv('results/multi_provider_comparison/all_providers_comparison.csv')

def create_provider_performance_comparison():
    """Create comprehensive provider performance comparison."""
    df = load_comparison_data()
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 16))
    fig.suptitle('LLM Provider Performance Comparison - SRLP Framework', 
                 fontsize=24, fontweight='bold', y=0.98)
    
    # 1. Quality Scores by Provider
    provider_quality = df.groupby('llm_provider').agg({
        'initial_quality': 'mean',
        'final_quality': 'mean',
        'improvement': 'mean'
    }).round(3)
    
    providers = provider_quality.index
    x_pos = np.arange(len(providers))
    width = 0.35
    
    bars1 = ax1.bar(x_pos - width/2, provider_quality['initial_quality'], width,
                   label='Initial Quality', color='lightcoral', alpha=0.8, edgecolor='black')
    bars2 = ax1.bar(x_pos + width/2, provider_quality['final_quality'], width,
                   label='Final Quality', color='lightblue', alpha=0.8, edgecolor='black')
    
    ax1.set_title('Quality Scores by LLM Provider', fontsize=16, fontweight='bold', pad=20)
    ax1.set_xlabel('LLM Provider', fontsize=14)
    ax1.set_ylabel('Quality Score', fontsize=14)
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels([p.upper() for p in providers], fontsize=12)
    ax1.legend(fontsize=12)
    ax1.set_ylim(0, 1)
    
    # Add value labels
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{height:.3f}', ha='center', va='bottom', fontweight='bold', fontsize=10)
    for bar in bars2:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{height:.3f}', ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # 2. Processing Speed Comparison
    speed_data = df.groupby('llm_provider')['time_seconds'].mean().sort_values()
    colors = plt.cm.viridis(np.linspace(0, 1, len(speed_data)))
    
    bars3 = ax2.barh(range(len(speed_data)), speed_data.values, color=colors, alpha=0.8, edgecolor='black')
    
    ax2.set_title('Processing Speed by Provider (Lower = Better)', fontsize=16, fontweight='bold', pad=20)
    ax2.set_xlabel('Average Processing Time (seconds)', fontsize=14)
    ax2.set_ylabel('LLM Provider', fontsize=14)
    ax2.set_yticks(range(len(speed_data)))
    ax2.set_yticklabels([p.upper() for p in speed_data.index], fontsize=12)
    
    # Add value labels
    for i, (bar, value) in enumerate(zip(bars3, speed_data.values)):
        ax2.text(value + 0.05, i, f'{value:.2f}s', va='center', fontweight='bold', fontsize=11)
    
    # 3. Success Rate and Convergence
    provider_stats = df.groupby('llm_provider').agg({
        'improvement': lambda x: (x > 0.005).mean() * 100,
        'converged': lambda x: x.mean() * 100
    }).round(1)
    
    x_pos = np.arange(len(provider_stats))
    width = 0.35
    
    bars4 = ax3.bar(x_pos - width/2, provider_stats['improvement'], width,
                   label='Success Rate (%)', color='lightgreen', alpha=0.8, edgecolor='black')
    bars5 = ax3.bar(x_pos + width/2, provider_stats['converged'], width,
                   label='Convergence Rate (%)', color='orange', alpha=0.8, edgecolor='black')
    
    ax3.set_title('Success Rate vs Convergence Rate', fontsize=16, fontweight='bold', pad=20)
    ax3.set_xlabel('LLM Provider', fontsize=14)
    ax3.set_ylabel('Percentage (%)', fontsize=14)
    ax3.set_xticks(x_pos)
    ax3.set_xticklabels([p.upper() for p in provider_stats.index], fontsize=12)
    ax3.legend(fontsize=12)
    ax3.set_ylim(0, 100)
    
    # Add value labels
    for bar in bars4:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=10)
    for bar in bars5:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # 4. Quality Improvement Distribution
    improvement_data = []
    provider_names = []
    
    for provider in df['llm_provider'].unique():
        provider_improvements = df[df['llm_provider'] == provider]['improvement'].values
        improvement_data.append(provider_improvements)
        provider_names.append(provider.upper())
    
    bp = ax4.boxplot(improvement_data, labels=provider_names, patch_artist=True)
    
    # Color the boxes
    colors = ['lightcoral', 'lightblue', 'lightgreen', 'orange', 'lightgray']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.8)
    
    ax4.set_title('Quality Improvement Distribution', fontsize=16, fontweight='bold', pad=20)
    ax4.set_xlabel('LLM Provider', fontsize=14)
    ax4.set_ylabel('Quality Improvement', fontsize=14)
    ax4.axhline(y=0, color='red', linestyle='--', alpha=0.7, linewidth=2)
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('results/multi_provider_visualizations/provider_performance_comparison.png',
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print("✅ Created: provider_performance_comparison.png")

def create_scenario_provider_heatmap():
    """Create heatmap showing provider performance across scenarios."""
    df = load_comparison_data()
    
    # Create pivot table for heatmap
    pivot_data = df.pivot_table(
        values='improvement',
        index='llm_provider',
        columns='scenario',
        aggfunc='mean'
    )
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
    fig.suptitle('Provider Performance Across Scenarios', fontsize=20, fontweight='bold', y=0.98)
    
    # 1. Improvement Heatmap
    sns.heatmap(pivot_data, annot=True, cmap='RdYlGn', center=0, 
                fmt='.3f', cbar_kws={'label': 'Quality Improvement'},
                ax=ax1, square=True, linewidths=0.5)
    
    ax1.set_title('Quality Improvement by Provider & Scenario', fontsize=14, fontweight='bold', pad=20)
    ax1.set_xlabel('Scenario', fontsize=12)
    ax1.set_ylabel('LLM Provider', fontsize=12)
    ax1.set_yticklabels([p.upper() for p in pivot_data.index], rotation=0)
    ax1.set_xticklabels([s.capitalize() for s in pivot_data.columns], rotation=45)
    
    # 2. Final Quality Heatmap
    pivot_quality = df.pivot_table(
        values='final_quality',
        index='llm_provider',
        columns='scenario',
        aggfunc='mean'
    )
    
    sns.heatmap(pivot_quality, annot=True, cmap='Blues', 
                fmt='.3f', cbar_kws={'label': 'Final Quality Score'},
                ax=ax2, square=True, linewidths=0.5)
    
    ax2.set_title('Final Quality by Provider & Scenario', fontsize=14, fontweight='bold', pad=20)
    ax2.set_xlabel('Scenario', fontsize=12)
    ax2.set_ylabel('LLM Provider', fontsize=12)
    ax2.set_yticklabels([p.upper() for p in pivot_quality.index], rotation=0)
    ax2.set_xticklabels([s.capitalize() for s in pivot_quality.columns], rotation=45)
    
    plt.tight_layout()
    plt.savefig('results/multi_provider_visualizations/scenario_provider_heatmap.png',
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print("✅ Created: scenario_provider_heatmap.png")

def create_model_comparison_chart():
    """Create detailed model comparison within providers."""
    df = load_comparison_data()
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 16))
    fig.suptitle('Detailed Model Comparison Within Providers', 
                 fontsize=20, fontweight='bold', y=0.98)
    
    # 1. Model Quality Comparison
    model_quality = df.groupby(['llm_provider', 'llm_model'])['final_quality'].mean().reset_index()
    
    # Create grouped bar chart
    providers = model_quality['llm_provider'].unique()
    x_offset = 0
    colors = plt.cm.Set3(np.linspace(0, 1, len(model_quality)))
    
    for i, (_, row) in enumerate(model_quality.iterrows()):
        ax1.bar(x_offset, row['final_quality'], color=colors[i], alpha=0.8, 
               edgecolor='black', width=0.8)
        ax1.text(x_offset, row['final_quality'] + 0.01, f"{row['final_quality']:.3f}",
                ha='center', va='bottom', fontweight='bold', fontsize=9)
        x_offset += 1
    
    ax1.set_title('Final Quality by Model', fontsize=14, fontweight='bold', pad=20)
    ax1.set_xlabel('Models', fontsize=12)
    ax1.set_ylabel('Final Quality Score', fontsize=12)
    ax1.set_xticks(range(len(model_quality)))
    ax1.set_xticklabels([f"{row['llm_provider']}\n{row['llm_model']}" 
                        for _, row in model_quality.iterrows()], rotation=45, ha='right')
    ax1.set_ylim(0, 1)
    
    # 2. Speed vs Quality Scatter
    model_stats = df.groupby(['llm_provider', 'llm_model']).agg({
        'final_quality': 'mean',
        'time_seconds': 'mean',
        'improvement': 'mean'
    }).reset_index()
    
    # Color by provider
    provider_colors = {'openai': 'red', 'claude': 'blue', 'llama': 'green', 
                      'huggingface': 'orange', 'mock': 'gray'}
    
    for provider in model_stats['llm_provider'].unique():
        provider_data = model_stats[model_stats['llm_provider'] == provider]
        ax2.scatter(provider_data['time_seconds'], provider_data['final_quality'],
                   s=200, alpha=0.7, label=provider.upper(), 
                   color=provider_colors.get(provider, 'black'), edgecolors='black')
        
        # Add model labels
        for _, row in provider_data.iterrows():
            ax2.annotate(row['llm_model'], 
                        (row['time_seconds'], row['final_quality']),
                        xytext=(5, 5), textcoords='offset points', fontsize=8,
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))
    
    ax2.set_title('Speed vs Quality Trade-off', fontsize=14, fontweight='bold', pad=20)
    ax2.set_xlabel('Processing Time (seconds)', fontsize=12)
    ax2.set_ylabel('Final Quality Score', fontsize=12)
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    
    # 3. Provider Efficiency (Quality/Time)
    model_stats['efficiency'] = model_stats['final_quality'] / model_stats['time_seconds']
    efficiency_sorted = model_stats.sort_values('efficiency', ascending=True)
    
    colors = [provider_colors.get(p, 'black') for p in efficiency_sorted['llm_provider']]
    bars = ax3.barh(range(len(efficiency_sorted)), efficiency_sorted['efficiency'],
                   color=colors, alpha=0.8, edgecolor='black')
    
    ax3.set_title('Model Efficiency (Quality/Time)', fontsize=14, fontweight='bold', pad=20)
    ax3.set_xlabel('Efficiency Score', fontsize=12)
    ax3.set_ylabel('Models', fontsize=12)
    ax3.set_yticks(range(len(efficiency_sorted)))
    ax3.set_yticklabels([f"{row['llm_provider']}-{row['llm_model']}" 
                        for _, row in efficiency_sorted.iterrows()], fontsize=10)
    
    # Add value labels
    for i, (bar, value) in enumerate(zip(bars, efficiency_sorted['efficiency'])):
        ax3.text(value + 0.01, i, f'{value:.2f}', va='center', fontweight='bold', fontsize=10)
    
    # 4. Improvement Consistency
    improvement_std = df.groupby(['llm_provider', 'llm_model'])['improvement'].agg(['mean', 'std']).reset_index()
    improvement_std.columns = ['llm_provider', 'llm_model', 'mean_improvement', 'std_improvement']
    
    for provider in improvement_std['llm_provider'].unique():
        provider_data = improvement_std[improvement_std['llm_provider'] == provider]
        ax4.scatter(provider_data['std_improvement'], provider_data['mean_improvement'],
                   s=200, alpha=0.7, label=provider.upper(),
                   color=provider_colors.get(provider, 'black'), edgecolors='black')
        
        # Add model labels
        for _, row in provider_data.iterrows():
            ax4.annotate(row['llm_model'],
                        (row['std_improvement'], row['mean_improvement']),
                        xytext=(5, 5), textcoords='offset points', fontsize=8,
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))
    
    ax4.set_title('Improvement Consistency (Mean vs Std Dev)', fontsize=14, fontweight='bold', pad=20)
    ax4.set_xlabel('Standard Deviation of Improvement', fontsize=12)
    ax4.set_ylabel('Mean Improvement', fontsize=12)
    ax4.axhline(y=0, color='red', linestyle='--', alpha=0.7)
    ax4.legend(fontsize=10)
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('results/multi_provider_visualizations/model_comparison_chart.png',
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print("✅ Created: model_comparison_chart.png")

def create_comprehensive_dashboard():
    """Create comprehensive multi-provider dashboard."""
    df = load_comparison_data()
    
    # Create large dashboard figure
    fig = plt.figure(figsize=(24, 18))
    fig.suptitle('SRLP Framework - Multi-Provider Comprehensive Dashboard', 
                 fontsize=28, fontweight='bold', y=0.98)
    
    # Create complex grid layout
    gs = fig.add_gridspec(4, 6, hspace=0.3, wspace=0.4)
    
    # 1. Provider Rankings (top-left, 2x2)
    ax1 = fig.add_subplot(gs[0:2, 0:2])
    
    provider_scores = df.groupby('llm_provider').agg({
        'final_quality': 'mean',
        'improvement': 'mean',
        'time_seconds': 'mean',
        'converged': 'mean'
    })
    
    # Calculate overall score
    provider_scores['overall_score'] = (
        provider_scores['final_quality'] * 0.4 +
        provider_scores['improvement'] * 10 * 0.3 +
        provider_scores['converged'] * 0.2 +
        (1 / provider_scores['time_seconds']) * 0.1
    )
    
    provider_scores_sorted = provider_scores.sort_values('overall_score', ascending=True)
    
    colors = plt.cm.RdYlGn(np.linspace(0.3, 0.9, len(provider_scores_sorted)))
    bars = ax1.barh(range(len(provider_scores_sorted)), provider_scores_sorted['overall_score'],
                   color=colors, alpha=0.8, edgecolor='black')
    
    ax1.set_title('Provider Overall Rankings', fontsize=16, fontweight='bold')
    ax1.set_xlabel('Overall Score', fontsize=12)
    ax1.set_yticks(range(len(provider_scores_sorted)))
    ax1.set_yticklabels([p.upper() for p in provider_scores_sorted.index], fontsize=12)
    
    # Add rank numbers
    for i, (bar, score) in enumerate(zip(bars, provider_scores_sorted['overall_score'])):
        rank = len(provider_scores_sorted) - i
        ax1.text(score + 0.01, i, f'#{rank} ({score:.3f})', 
                va='center', fontweight='bold', fontsize=11)
    
    # 2. Quality Distribution (top-middle, 2x2)
    ax2 = fig.add_subplot(gs[0:2, 2:4])
    
    quality_data = []
    provider_names = []
    
    for provider in df['llm_provider'].unique():
        quality_data.append(df[df['llm_provider'] == provider]['final_quality'].values)
        provider_names.append(provider.upper())
    
    bp = ax2.boxplot(quality_data, labels=provider_names, patch_artist=True)
    colors = ['lightcoral', 'lightblue', 'lightgreen', 'orange', 'lightgray']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.8)
    
    ax2.set_title('Quality Score Distribution', fontsize=16, fontweight='bold')
    ax2.set_ylabel('Final Quality Score', fontsize=12)
    ax2.grid(True, alpha=0.3)
    
    # 3. Speed Comparison (top-right, 2x2)
    ax3 = fig.add_subplot(gs[0:2, 4:6])
    
    speed_stats = df.groupby('llm_provider')['time_seconds'].agg(['mean', 'std']).reset_index()
    
    x_pos = np.arange(len(speed_stats))
    bars = ax3.bar(x_pos, speed_stats['mean'], yerr=speed_stats['std'],
                  capsize=5, alpha=0.8, edgecolor='black',
                  color=['red', 'blue', 'green', 'orange', 'gray'])
    
    ax3.set_title('Processing Speed Comparison', fontsize=16, fontweight='bold')
    ax3.set_xlabel('LLM Provider', fontsize=12)
    ax3.set_ylabel('Time (seconds)', fontsize=12)
    ax3.set_xticks(x_pos)
    ax3.set_xticklabels([p.upper() for p in speed_stats['llm_provider']], rotation=45)
    
    # Add value labels
    for bar, mean_val in zip(bars, speed_stats['mean']):
        ax3.text(bar.get_x() + bar.get_width()/2., mean_val + 0.1,
                f'{mean_val:.2f}s', ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # 4. Scenario Performance Matrix (middle, full width)
    ax4 = fig.add_subplot(gs[2, :])
    
    pivot_improvement = df.pivot_table(
        values='improvement',
        index='llm_provider',
        columns='scenario',
        aggfunc='mean'
    )
    
    sns.heatmap(pivot_improvement, annot=True, cmap='RdYlGn', center=0,
                fmt='.3f', cbar_kws={'label': 'Quality Improvement'},
                ax=ax4, square=False, linewidths=0.5)
    
    ax4.set_title('Provider Performance Across Scenarios', fontsize=16, fontweight='bold')
    ax4.set_xlabel('Scenario', fontsize=12)
    ax4.set_ylabel('LLM Provider', fontsize=12)
    ax4.set_yticklabels([p.upper() for p in pivot_improvement.index], rotation=0)
    ax4.set_xticklabels([s.capitalize() for s in pivot_improvement.columns], rotation=0)
    
    # 5. Key Statistics (bottom-left, 1x3)
    ax5 = fig.add_subplot(gs[3, 0:3])
    ax5.axis('off')
    
    # Calculate key statistics
    total_evaluations = len(df)
    best_provider = provider_scores_sorted.index[-1].upper()
    fastest_provider = df.groupby('llm_provider')['time_seconds'].mean().idxmin().upper()
    most_consistent = df.groupby('llm_provider')['improvement'].std().idxmin().upper()
    
    stats_text = f"""
    📊 MULTI-PROVIDER EVALUATION SUMMARY
    
    Total Evaluations: {total_evaluations}
    Providers Tested: {df['llm_provider'].nunique()}
    Scenarios Evaluated: {df['scenario'].nunique()}
    Models Compared: {df['llm_model'].nunique()}
    
    🏆 Best Overall: {best_provider}
    ⚡ Fastest: {fastest_provider}
    📈 Most Consistent: {most_consistent}
    """
    
    ax5.text(0.5, 0.5, stats_text, fontsize=14, ha='center', va='center',
            transform=ax5.transAxes, fontweight='bold',
            bbox=dict(boxstyle='round,pad=1', facecolor='lightblue', alpha=0.3))
    
    # 6. Success Rates (bottom-right, 1x3)
    ax6 = fig.add_subplot(gs[3, 3:6])
    
    success_rates = df.groupby('llm_provider')['improvement'].apply(lambda x: (x > 0.005).mean() * 100)
    convergence_rates = df.groupby('llm_provider')['converged'].mean() * 100
    
    x_pos = np.arange(len(success_rates))
    width = 0.35
    
    bars1 = ax6.bar(x_pos - width/2, success_rates.values, width,
                   label='Success Rate', color='lightgreen', alpha=0.8, edgecolor='black')
    bars2 = ax6.bar(x_pos + width/2, convergence_rates.values, width,
                   label='Convergence Rate', color='orange', alpha=0.8, edgecolor='black')
    
    ax6.set_title('Success & Convergence Rates', fontsize=16, fontweight='bold')
    ax6.set_xlabel('LLM Provider', fontsize=12)
    ax6.set_ylabel('Rate (%)', fontsize=12)
    ax6.set_xticks(x_pos)
    ax6.set_xticklabels([p.upper() for p in success_rates.index], rotation=45)
    ax6.legend(fontsize=12)
    ax6.set_ylim(0, 100)
    
    # Add value labels
    for bar in bars1:
        height = bar.get_height()
        ax6.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=10)
    for bar in bars2:
        height = bar.get_height()
        ax6.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    plt.savefig('results/multi_provider_visualizations/comprehensive_dashboard.png',
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print("✅ Created: comprehensive_dashboard.png")

def generate_all_multi_provider_visualizations():
    """Generate all multi-provider comparison visualizations."""
    print("🎨 Creating Multi-Provider Comparison Visualizations...")
    print("=" * 80)
    
    create_provider_performance_comparison()
    create_scenario_provider_heatmap()
    create_model_comparison_chart()
    create_comprehensive_dashboard()
    
    print("=" * 80)
    print("🎉 All multi-provider visualizations created successfully!")
    print("📁 Saved to: results/multi_provider_visualizations/")
    print("\n📊 Generated Charts:")
    print("   1. provider_performance_comparison.png")
    print("   2. scenario_provider_heatmap.png")
    print("   3. model_comparison_chart.png")
    print("   4. comprehensive_dashboard.png")

if __name__ == "__main__":
    generate_all_multi_provider_visualizations()

