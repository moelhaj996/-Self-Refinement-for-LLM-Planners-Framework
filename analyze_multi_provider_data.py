"""
Analyze multi-provider comparison data and generate comprehensive statistics.
"""

import pandas as pd
import numpy as np

def analyze_provider_comparison():
    """Analyze the multi-provider comparison data."""
    
    # Load the data
    df = pd.read_csv('results/multi_provider_comparison/all_providers_comparison.csv')
    
    print("🔍 MULTI-PROVIDER ANALYSIS")
    print("=" * 80)
    print(f"📊 Total Evaluations: {len(df)}")
    print(f"🤖 Providers: {df['llm_provider'].nunique()} ({', '.join(df['llm_provider'].unique())})")
    print(f"📋 Scenarios: {df['scenario'].nunique()} ({', '.join(df['scenario'].unique())})")
    print(f"🔧 Models: {df['llm_model'].nunique()}")
    
    # Provider-level analysis
    print("\n🏆 PROVIDER RANKINGS")
    print("=" * 80)
    
    provider_stats = df.groupby('llm_provider').agg({
        'initial_quality': 'mean',
        'final_quality': 'mean',
        'improvement': ['mean', 'std'],
        'time_seconds': 'mean',
        'converged': 'mean',
        'iterations': 'mean',
        'efficiency': 'mean'
    }).round(4)
    
    # Flatten column names
    provider_stats.columns = ['_'.join(col).strip() for col in provider_stats.columns.values]
    
    # Calculate success rate
    provider_stats['success_rate'] = df.groupby('llm_provider')['improvement'].apply(lambda x: (x > 0.005).mean() * 100).round(1)
    
    # Calculate overall score (weighted combination of metrics)
    provider_stats['overall_score'] = (
        provider_stats['final_quality_mean'] * 0.4 +
        provider_stats['improvement_mean'] * 100 * 0.3 +
        (provider_stats['converged_mean'] * 100) / 100 * 0.2 +
        (100 - provider_stats['success_rate']) / 100 * 0.1
    ).round(3)
    
    # Sort by overall score
    provider_rankings = provider_stats.sort_values('overall_score', ascending=False)
    
    print("Rank | Provider    | Quality | Improvement | Speed  | Success | Convergence | Overall")
    print("-" * 80)
    
    for i, (provider, stats) in enumerate(provider_rankings.iterrows(), 1):
        print(f"{i:4d} | {provider:11s} | {stats['final_quality_mean']:7.3f} | "
              f"{stats['improvement_mean']:11.3f} | {stats['time_seconds_mean']:6.2f}s | "
              f"{stats['success_rate']:7.1f}% | {stats['converged_mean']*100:11.1f}% | "
              f"{stats['overall_score']:7.3f}")
    
    # Model-level analysis
    print("\n🔧 MODEL PERFORMANCE")
    print("=" * 80)
    
    model_stats = df.groupby(['llm_provider', 'llm_model']).agg({
        'final_quality': 'mean',
        'improvement': 'mean',
        'time_seconds': 'mean',
        'converged': 'mean'
    }).round(3)
    
    for (provider, model), stats in model_stats.iterrows():
        print(f"{provider:12s} | {model:20s} | Quality: {stats['final_quality']:5.3f} | "
              f"Improvement: {stats['improvement']:+6.3f} | Speed: {stats['time_seconds']:5.2f}s")
    
    # Scenario analysis
    print("\n📋 SCENARIO DIFFICULTY ANALYSIS")
    print("=" * 80)
    
    scenario_stats = df.groupby('scenario').agg({
        'initial_quality': 'mean',
        'final_quality': 'mean',
        'improvement': ['mean', 'std'],
        'time_seconds': 'mean',
        'scenario_complexity': 'first'
    }).round(3)
    
    scenario_stats.columns = ['_'.join(col).strip() for col in scenario_stats.columns.values]
    scenario_stats = scenario_stats.sort_values('scenario_complexity_first')
    
    print("Scenario    | Complexity | Initial | Final   | Improvement | Std Dev | Avg Time")
    print("-" * 80)
    
    for scenario, stats in scenario_stats.iterrows():
        print(f"{scenario:11s} | {stats['scenario_complexity_first']:10.1f} | "
              f"{stats['initial_quality_mean']:7.3f} | {stats['final_quality_mean']:7.3f} | "
              f"{stats['improvement_mean']:11.3f} | {stats['improvement_std']:7.3f} | "
              f"{stats['time_seconds_mean']:8.2f}s")
    
    # Provider vs Scenario matrix
    print("\n🎯 PROVIDER vs SCENARIO PERFORMANCE MATRIX")
    print("=" * 80)
    
    pivot_improvement = df.pivot_table(
        values='improvement', 
        index='llm_provider', 
        columns='scenario', 
        aggfunc='mean'
    ).round(3)
    
    print("Provider    |", end="")
    for scenario in pivot_improvement.columns:
        print(f" {scenario:8s} |", end="")
    print()
    print("-" * (13 + len(pivot_improvement.columns) * 11))
    
    for provider in pivot_improvement.index:
        print(f"{provider:11s} |", end="")
        for scenario in pivot_improvement.columns:
            value = pivot_improvement.loc[provider, scenario]
            print(f" {value:+8.3f} |", end="")
        print()
    
    # Quality tier analysis
    print("\n📊 QUALITY TIER DISTRIBUTION")
    print("=" * 80)
    
    tier_dist = df.groupby(['llm_provider', 'performance_tier']).size().unstack(fill_value=0)
    tier_percentages = tier_dist.div(tier_dist.sum(axis=1), axis=0) * 100
    
    for provider in tier_percentages.index:
        print(f"{provider:12s} | ", end="")
        for tier in ['High', 'Medium', 'Low']:
            if tier in tier_percentages.columns:
                pct = tier_percentages.loc[provider, tier]
                print(f"{tier}: {pct:5.1f}% | ", end="")
        print()
    
    # Statistical significance tests
    print("\n📈 IMPROVEMENT STATISTICS")
    print("=" * 80)
    
    for provider in df['llm_provider'].unique():
        provider_data = df[df['llm_provider'] == provider]['improvement']
        positive_improvements = (provider_data > 0.005).sum()
        total_evaluations = len(provider_data)
        mean_improvement = provider_data.mean()
        std_improvement = provider_data.std()
        
        print(f"{provider:12s} | Mean: {mean_improvement:+6.3f} ± {std_improvement:5.3f} | "
              f"Positive: {positive_improvements}/{total_evaluations} "
              f"({positive_improvements/total_evaluations*100:4.1f}%)")
    
    # Save detailed analysis
    analysis_summary = {
        'provider_rankings': provider_rankings,
        'model_performance': model_stats,
        'scenario_difficulty': scenario_stats,
        'provider_scenario_matrix': pivot_improvement,
        'quality_tiers': tier_percentages
    }
    
    # Export summary to CSV
    provider_rankings.to_csv('results/multi_provider_comparison/provider_rankings.csv')
    pivot_improvement.to_csv('results/multi_provider_comparison/llm_provider_performance_matrix.csv')
    
    print(f"\n💾 Analysis results saved to:")
    print(f"   - provider_rankings.csv")
    print(f"   - llm_provider_performance_matrix.csv")
    
    return analysis_summary

if __name__ == "__main__":
    analysis_results = analyze_provider_comparison()

