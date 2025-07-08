import sys
import os

# Add the parent directory to path to import srlp_framework
sys.path.append('/Users/mohamedelhajsuliman/Desktop/Mohamed 2025 summer thesis')

# Import necessary modules
from srlp_framework.core.evaluator import Evaluator
from srlp_framework.core.metrics_calculator import BasicMetricsCalculator
from srlp_framework.core.refinement_engine import RefinementEngine
from srlp_framework.test_scenarios import get_scenario_by_name
from srlp_framework.utils.visualization import generate_all_visualizations
import json
import time

def demonstrate_supervisor_requirements():
    """
    Demonstrate all supervisor requirements for the SRLP framework.
    """
    print("=" * 80)
    print("SRLP FRAMEWORK - SUPERVISOR REQUIREMENTS DEMONSTRATION")
    print("=" * 80)
    print("Self-Refinement for LLM Planners via Self-Checking Feedback")
    print()
    
    # Ensure results directory exists
    os.makedirs('results/final_demo', exist_ok=True)
    
    # ✅ REQUIREMENT 1: Run at least 2–3 test scenarios using your framework
    print("✅ REQUIREMENT 1: Running 3 test scenarios using SRLP framework")
    print("-" * 60)
    
    scenarios_to_test = ['travel', 'cooking', 'project']
    all_results = []
    
    for i, scenario_name in enumerate(scenarios_to_test, 1):
        print(f"\n[{i}/3] Running scenario: {scenario_name}")
        print("=" * 40)
        
        # Get scenario
        scenario = get_scenario_by_name(scenario_name)
        problem = scenario['problem']
        
        print(f"Problem: {problem['goal']}")
        print(f"Type: {problem['type']}")
        print(f"Constraints: {len(problem['constraints'])}")
        
        # Initialize components
        evaluator = Evaluator()
        calculator = BasicMetricsCalculator()
        
        # Run evaluation (Input → Plan → Self-Check → Feedback → Refine → Evaluate)
        print("\nExecuting: Input → Plan → Self-Check → Feedback → Refine → Evaluate")
        evaluation_result = evaluator.evaluate_scenario(scenario['name'], problem)
        
        # Extract results
        refinement_result = evaluation_result.refinement_result
        initial_plan = refinement_result.initial_plan
        final_plan = refinement_result.final_plan
        
        # Get check results from refinement history
        initial_check_data = refinement_result.refinement_history[0]['check_result']
        final_check_data = refinement_result.refinement_history[-1]['check_result']
        
        # Convert to CheckResult objects for metrics calculation
        from srlp_framework.core.self_checker import CheckResult
        
        initial_check = CheckResult(
            overall_score=initial_check_data['overall_score'],
            error_count=initial_check_data['error_count'],
            errors=initial_check_data['errors'],
            constraint_violations=initial_check_data['constraint_violations'],
            uncertainty_scores=initial_check_data['uncertainty_scores'],
            semantic_consistency=initial_check_data['semantic_consistency'],
            completeness_score=initial_check_data['completeness_score']
        )
        
        final_check = CheckResult(
            overall_score=final_check_data['overall_score'],
            error_count=final_check_data['error_count'],
            errors=final_check_data['errors'],
            constraint_violations=final_check_data['constraint_violations'],
            uncertainty_scores=final_check_data['uncertainty_scores'],
            semantic_consistency=final_check_data['semantic_consistency'],
            completeness_score=final_check_data['completeness_score']
        )
        
        # ✅ REQUIREMENT 2: Output metrics (before vs. after refinement)
        print("\n✅ REQUIREMENT 2: Calculating metrics (before vs. after refinement)")
        
        # Calculate metrics using BasicMetricsCalculator.calculate_metrics()
        metrics_before = calculator.calculate_metrics(initial_plan, problem, initial_check)
        metrics_after = calculator.calculate_metrics(final_plan, problem, final_check)
        
        # Display metrics comparison
        print("\nMETRICS COMPARISON:")
        print("-" * 30)
        print(f"Quality Score:     {metrics_before.quality_metrics['overall_quality_score']:.3f} → {metrics_after.quality_metrics['overall_quality_score']:.3f}")
        print(f"Completeness:      {metrics_before.quality_metrics['completeness_score']:.3f} → {metrics_after.quality_metrics['completeness_score']:.3f}")
        print(f"Semantic Consist.: {metrics_before.quality_metrics['semantic_consistency']:.3f} → {metrics_after.quality_metrics['semantic_consistency']:.3f}")
        print(f"Error Count:       {int(metrics_before.quality_metrics['total_errors'])} → {int(metrics_after.quality_metrics['total_errors'])}")
        print(f"Constraint Violat: {int(metrics_before.quality_metrics['constraint_violations'])} → {int(metrics_after.quality_metrics['constraint_violations'])}")
        
        improvement = metrics_after.quality_metrics['overall_quality_score'] - metrics_before.quality_metrics['overall_quality_score']
        print(f"Overall Improvement: {improvement:+.3f} ({(improvement/metrics_before.quality_metrics['overall_quality_score'])*100:+.1f}%)")
        
        # Store results for aggregation
        result_data = {
            'scenario': scenario_name,
            'problem': problem,
            'metrics_before': metrics_before.to_dict(),
            'metrics_after': metrics_after.to_dict(),
            'refinement_result': refinement_result.to_dict(),
            'evaluation_metrics': evaluation_result.metrics
        }
        all_results.append(result_data)
        
        # Export individual scenario results to CSV
        csv_filename = f"results/final_demo/{scenario_name}_metrics.csv"
        calculator.export_comparison_to_csv(metrics_before, metrics_after, csv_filename)
        print(f"Metrics exported to: {csv_filename}")
    
    print("\n" + "=" * 80)
    print("✅ REQUIREMENT 3: Visualize and export metrics for thesis")
    print("-" * 60)
    
    # Generate comprehensive visualizations
    print("Generating visualizations for thesis inclusion...")
    viz_files = generate_all_visualizations(all_results, 'results/final_demo/visualizations')
    
    print(f"Generated {len(viz_files)} visualization files:")
    for viz_file in viz_files:
        print(f"  - {viz_file}")
    
    # Export aggregate results
    print("\nExporting aggregate results...")
    
    # CSV format for easy analysis
    import csv
    csv_summary_file = 'results/final_demo/aggregate_results.csv'
    with open(csv_summary_file, 'w', newline='') as csvfile:
        fieldnames = ['scenario', 'initial_quality', 'final_quality', 'improvement', 
                     'improvement_percent', 'converged', 'iterations', 'time_seconds']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for result in all_results:
            scenario = result['scenario']
            before_quality = result['metrics_before']['quality_metrics']['overall_quality_score']
            after_quality = result['metrics_after']['quality_metrics']['overall_quality_score']
            improvement = after_quality - before_quality
            converged = result['refinement_result']['converged']
            iterations = result['refinement_result']['iterations']
            time_taken = result['refinement_result']['total_time']
            
            writer.writerow({
                'scenario': scenario,
                'initial_quality': before_quality,
                'final_quality': after_quality,
                'improvement': improvement,
                'improvement_percent': (improvement / max(0.001, before_quality)) * 100,
                'converged': converged,
                'iterations': iterations,
                'time_seconds': time_taken
            })
    
    print(f"Aggregate CSV exported to: {csv_summary_file}")
    
    # JSON format for complete data
    json_file = 'results/final_demo/complete_results.json'
    with open(json_file, 'w') as f:
        json.dump({
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
            'framework_version': '1.0.0',
            'total_scenarios': len(all_results),
            'summary_statistics': calculate_summary_statistics(all_results),
            'detailed_results': all_results
        }, f, indent=2)
    
    print(f"Complete JSON exported to: {json_file}")
    
    print("\n" + "=" * 80)
    print("✅ REQUIREMENT 4: Reusable script with all components")
    print("-" * 60)
    
    print("This script demonstrates integration of all framework components:")
    print("  ✓ evaluator.py - Comprehensive framework evaluation")
    print("  ✓ test_scenarios.py - Predefined test scenarios")
    print("  ✓ metrics_calculator.py - BasicMetricsCalculator.calculate_metrics()")
    print("  ✓ refinement_engine.py - Iterative refinement process")
    print("  ✓ Visualization tools - Charts and graphs for thesis")
    print("  ✓ Export capabilities - CSV and JSON formats")
    
    # Generate final summary
    print("\n" + "=" * 80)
    print("FINAL SUMMARY")
    print("=" * 80)
    
    summary_stats = calculate_summary_statistics(all_results)
    
    print(f"Scenarios Evaluated: {summary_stats['total_scenarios']}")
    print(f"Average Initial Quality: {summary_stats['avg_initial_quality']:.3f}")
    print(f"Average Final Quality: {summary_stats['avg_final_quality']:.3f}")
    print(f"Average Improvement: {summary_stats['avg_improvement']:.3f} ({summary_stats['avg_improvement_percent']:.1f}%)")
    print(f"Success Rate (Converged): {summary_stats['success_rate']:.1%}")
    print(f"Average Iterations: {summary_stats['avg_iterations']:.1f}")
    print(f"Total Processing Time: {summary_stats['total_time']:.2f}s")
    
    print(f"\nBest Performing Scenario: {summary_stats['best_scenario']}")
    print(f"Largest Improvement: {summary_stats['max_improvement']:.3f}")
    
    print("\n" + "=" * 80)
    print("✅ ALL SUPERVISOR REQUIREMENTS COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    print("Framework is ready for thesis submission and evaluation.")
    print("All results, metrics, and visualizations are available in: results/final_demo/")
    
    return all_results


def calculate_summary_statistics(results):
    """Calculate summary statistics for the evaluation results."""
    if not results:
        return {}
    
    initial_qualities = [r['metrics_before']['quality_metrics']['overall_quality_score'] for r in results]
    final_qualities = [r['metrics_after']['quality_metrics']['overall_quality_score'] for r in results]
    improvements = [f - i for i, f in zip(initial_qualities, final_qualities)]
    convergence = [r['refinement_result']['converged'] for r in results]
    iterations = [r['refinement_result']['iterations'] for r in results]
    times = [r['refinement_result']['total_time'] for r in results]
    
    # Find best performing scenario
    best_idx = improvements.index(max(improvements))
    best_scenario = results[best_idx]['scenario']
    
    return {
        'total_scenarios': len(results),
        'avg_initial_quality': sum(initial_qualities) / len(initial_qualities),
        'avg_final_quality': sum(final_qualities) / len(final_qualities),
        'avg_improvement': sum(improvements) / len(improvements),
        'avg_improvement_percent': (sum(improvements) / sum(initial_qualities)) * 100,
        'success_rate': sum(convergence) / len(convergence),
        'avg_iterations': sum(iterations) / len(iterations),
        'total_time': sum(times),
        'best_scenario': best_scenario,
        'max_improvement': max(improvements)
    }


def main():
    """Main function to run the demonstration."""
    print("Starting SRLP Framework Final Demonstration...")
    print("This script fulfills all supervisor requirements.")
    print()
    
    start_time = time.time()
    results = demonstrate_supervisor_requirements()
    end_time = time.time()
    
    print(f"\nDemonstration completed in {end_time - start_time:.2f} seconds")
    print("Ready for thesis submission!")


if __name__ == "__main__":
    main()