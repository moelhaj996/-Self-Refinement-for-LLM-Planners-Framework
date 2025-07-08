"""
Combine real execution results from multiple CSV files and create comprehensive dataset.
"""

import pandas as pd
import numpy as np
import os

def combine_execution_results():
    """Combine all real execution results into a comprehensive dataset."""
    
    # Read all CSV files
    results_dir = 'results/real_execution'
    csv_files = [
        'multi_scenario_mock.csv',
        'additional_scenarios.csv'
    ]
    
    all_data = []
    
    for csv_file in csv_files:
        file_path = os.path.join(results_dir, csv_file)
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            all_data.append(df)
            print(f"✅ Loaded {len(df)} records from {csv_file}")
    
    if not all_data:
        print("❌ No data files found")
        return
    
    # Combine all data
    combined_df = pd.concat(all_data, ignore_index=True)
    print(f"📊 Combined dataset: {len(combined_df)} total records")
    
    # Add additional calculated metrics
    combined_df['quality_change_category'] = combined_df['improvement'].apply(
        lambda x: 'Improved' if x > 0.001 else ('Degraded' if x < -0.001 else 'Unchanged')
    )
    
    combined_df['performance_category'] = combined_df['final_quality'].apply(
        lambda x: 'High' if x > 0.6 else ('Medium' if x > 0.4 else 'Low')
    )
    
    # Add scenario complexity scores (based on problem type)
    complexity_scores = {
        'travel': 0.6,
        'cooking': 0.4,
        'project': 0.8,
        'event': 0.7,
        'renovation': 0.7
    }
    
    combined_df['scenario_complexity'] = combined_df['scenario'].map(complexity_scores)
    
    # Calculate efficiency metrics
    combined_df['quality_per_second'] = combined_df['final_quality'] / combined_df['time_seconds']
    combined_df['improvement_per_iteration'] = combined_df['improvement'] / combined_df['iterations']
    
    # Save combined results
    output_file = os.path.join(results_dir, 'combined_real_execution_results.csv')
    combined_df.to_csv(output_file, index=False)
    print(f"💾 Saved combined results to: {output_file}")
    
    # Generate summary statistics
    print("\n📈 REAL EXECUTION SUMMARY STATISTICS")
    print("=" * 60)
    print(f"Total Evaluations: {len(combined_df)}")
    print(f"Scenarios Tested: {combined_df['scenario'].nunique()}")
    print(f"Average Initial Quality: {combined_df['initial_quality'].mean():.3f}")
    print(f"Average Final Quality: {combined_df['final_quality'].mean():.3f}")
    print(f"Average Improvement: {combined_df['improvement'].mean():.3f}")
    print(f"Average Processing Time: {combined_df['time_seconds'].mean():.3f}s")
    print(f"Convergence Rate: {(combined_df['converged'].sum() / len(combined_df) * 100):.1f}%")
    
    print("\n📊 Quality Change Distribution:")
    quality_dist = combined_df['quality_change_category'].value_counts()
    for category, count in quality_dist.items():
        percentage = (count / len(combined_df)) * 100
        print(f"   {category}: {count} ({percentage:.1f}%)")
    
    print("\n🎯 Performance by Scenario:")
    scenario_stats = combined_df.groupby('scenario').agg({
        'initial_quality': 'mean',
        'final_quality': 'mean',
        'improvement': 'mean',
        'time_seconds': 'mean'
    }).round(3)
    
    for scenario in scenario_stats.index:
        stats = scenario_stats.loc[scenario]
        print(f"   {scenario.capitalize()}: {stats['initial_quality']:.3f} → {stats['final_quality']:.3f} "
              f"({stats['improvement']:+.3f}) in {stats['time_seconds']:.3f}s")
    
    return combined_df

if __name__ == "__main__":
    combined_data = combine_execution_results()

