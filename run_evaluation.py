"""
Main evaluation script for the SRLP framework with LLM provider support.
Supports OpenAI, Claude, LLaMA, HuggingFace, and any LLM provider.

Usage examples:
    # Run with OpenAI GPT-4
    python run_evaluation.py --provider openai --model gpt-4 --scenario travel --export results.csv
    
    # Run with Claude
    python run_evaluation.py --provider claude --model claude-3-sonnet-20240229 --scenario cooking
    
    # Run with local LLaMA via Ollama
    python run_evaluation.py --provider llama --model llama2 --scenario project
    
    # Run multiple scenarios with HuggingFace
    python run_evaluation.py --provider huggingface --model gpt2 --scenarios travel cooking project
"""

import argparse
import json
import os
import sys
import time
from typing import Dict, List, Any, Optional

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from refinement_engine import create_refinement_engine
from srlp_framework.core.metrics_calculator import BasicMetricsCalculator
from srlp_framework.test_scenarios import get_scenario_by_name, get_all_test_scenarios
from srlp_framework.utils.visualization import generate_all_visualizations
from srlp_framework.llm_providers import LLMFactory, list_available_providers


def run_evaluation_with_llm(scenario_name: str, provider: str = "mock", 
                           model_name: Optional[str] = None, 
                           export_path: Optional[str] = None,
                           iterations: int = 3, **llm_kwargs) -> Dict[str, Any]:
    """
    Run SRLP evaluation with specified LLM provider.
    
    Args:
        scenario_name: Name of the scenario to evaluate
        provider: LLM provider name ('openai', 'claude', 'llama', 'huggingface', 'mock')
        model_name: Model name (optional, uses provider default)
        export_path: Path to export results (optional)
        iterations: Number of refinement iterations
        **llm_kwargs: Additional LLM configuration parameters
        
    Returns:
        Dictionary with evaluation results
    """
    
    print(f"🚀 Running SRLP Evaluation")
    print(f"📋 Scenario: {scenario_name}")
    print(f"🤖 LLM Provider: {provider}")
    if model_name:
        print(f"🧠 Model: {model_name}")
    print(f"🔄 Max Iterations: {iterations}")
    print("=" * 60)
    
    # Load scenario
    try:
        scenario_data = get_scenario_by_name(scenario_name)
        problem = scenario_data['problem']
        print(f"📝 Problem: {problem.get('goal', 'No goal specified')}")
        print(f"🎯 Type: {problem.get('type', 'general')}")
        print()
    except Exception as e:
        print(f"❌ Error loading scenario '{scenario_name}': {e}")
        return {}
    
    # Create LLM-enabled refinement engine
    try:
        print(f"🔧 Initializing {provider} LLM provider...")
        
        refinement_engine = create_refinement_engine(
            provider=provider,
            model_name=model_name,
            max_iterations=iterations,
            **llm_kwargs
        )
        
        # Test connection
        if not refinement_engine.test_connection():
            print(f"⚠️  Warning: Could not connect to {provider}. Using mock provider as fallback.")
            refinement_engine = create_refinement_engine(provider="mock", max_iterations=iterations)
        
        llm_info = refinement_engine.get_provider_info()
        print(f"✅ LLM Ready: {llm_info.get('provider', 'unknown')} - {llm_info.get('model', 'unknown')}")
        print()
        
    except Exception as e:
        print(f"❌ Error initializing {provider}: {e}")
        print("🔄 Falling back to mock provider...")
        refinement_engine = create_refinement_engine(provider="mock", max_iterations=iterations)
        llm_info = refinement_engine.get_provider_info()
    
    # Initialize metrics calculator
    calculator = BasicMetricsCalculator()
    
    # Run refinement process
    print("🔄 Starting refinement process...")
    start_time = time.time()
    
    try:
        refinement_result = refinement_engine.refine_plan(problem)
        
        # Extract plans and check results
        initial_plan = refinement_result.initial_plan
        final_plan = refinement_result.final_plan
        
        # Get check results from refinement history
        initial_check_data = refinement_result.refinement_history[0]['check_result']
        final_check_data = refinement_result.refinement_history[-1]['check_result']
        
        # Convert to CheckResult objects
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
        
        # Calculate metrics
        print("📊 Calculating metrics...")
        metrics_before = calculator.calculate_metrics(initial_plan, problem, initial_check)
        metrics_after = calculator.calculate_metrics(final_plan, problem, final_check)
        improvement_metrics = calculator.compare_metrics(metrics_before, metrics_after)
        
        total_time = time.time() - start_time
        
        # Display results
        print("\n" + "=" * 60)
        print("📈 EVALUATION RESULTS")
        print("=" * 60)
        
        print(f"⏱️  Total Processing Time: {total_time:.2f}s")
        print(f"🔄 Refinement Iterations: {refinement_result.iterations}")
        print(f"✅ Converged: {'Yes' if refinement_result.converged else 'No'}")
        print()
        
        print("📊 Quality Metrics:")
        print(f"   Initial Quality: {metrics_before.quality_metrics['overall_quality_score']:.3f}")
        print(f"   Final Quality:   {metrics_after.quality_metrics['overall_quality_score']:.3f}")
        print(f"   Improvement:     {improvement_metrics['overall_quality_score_absolute_improvement']:+.3f}")
        print(f"   Relative Gain:   {improvement_metrics['overall_quality_score_relative_improvement']:+.1f}%")
        print()
        
        print("🎯 Performance Metrics:")
        if 'total_errors_absolute_improvement' in improvement_metrics:
            print(f"   Error Reduction: {improvement_metrics['total_errors_absolute_improvement']:+.1f}")
        else:
            print(f"   Error Reduction: N/A")
        print(f"   Completeness:    {metrics_after.quality_metrics['completeness_score']:.3f}")
        print(f"   Consistency:     {metrics_after.quality_metrics['semantic_consistency']:.3f}")
        print()
        
        print("🤖 LLM Information:")
        print(f"   Provider: {llm_info.get('provider', 'unknown')}")
        print(f"   Model:    {llm_info.get('model', 'unknown')}")
        
        # Prepare results
        results = {
            'scenario': scenario_name,
            'problem': problem,
            'refinement_result': refinement_result.to_dict(),
            'metrics_before': metrics_before.to_dict(),
            'metrics_after': metrics_after.to_dict(),
            'improvement_metrics': improvement_metrics,
            'llm_info': llm_info,
            'evaluation_metadata': {
                'total_time': total_time,
                'timestamp': time.time(),
                'framework_version': '1.0.0'
            }
        }
        
        # Export results if requested
        if export_path:
            export_results(results, export_path)
        
        return results
        
    except Exception as e:
        print(f"❌ Error during evaluation: {e}")
        return {}


def run_multiple_evaluations(scenarios: List[str], provider: str = "mock",
                            model_name: Optional[str] = None,
                            export_path: Optional[str] = None,
                            iterations: int = 3, **llm_kwargs) -> List[Dict[str, Any]]:
    """
    Run evaluations on multiple scenarios.
    
    Args:
        scenarios: List of scenario names
        provider: LLM provider name
        model_name: Model name (optional)
        export_path: Path to export aggregate results
        iterations: Number of refinement iterations
        **llm_kwargs: Additional LLM configuration parameters
        
    Returns:
        List of evaluation results
    """
    
    print(f"🚀 Running SRLP Multi-Scenario Evaluation")
    print(f"📋 Scenarios: {', '.join(scenarios)}")
    print(f"🤖 LLM Provider: {provider}")
    if model_name:
        print(f"🧠 Model: {model_name}")
    print(f"🔄 Max Iterations: {iterations}")
    print("=" * 80)
    
    results = []
    start_time = time.time()
    
    for i, scenario_name in enumerate(scenarios, 1):
        print(f"\n[{i}/{len(scenarios)}] 🎯 Evaluating: {scenario_name}")
        print("-" * 60)
        
        try:
            result = run_evaluation_with_llm(
                scenario_name=scenario_name,
                provider=provider,
                model_name=model_name,
                iterations=iterations,
                **llm_kwargs
            )
            
            if result:
                results.append(result)
                
                # Brief summary
                before_quality = result['metrics_before']['quality_metrics']['overall_quality_score']
                after_quality = result['metrics_after']['quality_metrics']['overall_quality_score']
                improvement = after_quality - before_quality
                converged = result['refinement_result']['converged']
                
                print(f"✅ Completed: {before_quality:.3f} → {after_quality:.3f} ({improvement:+.3f})")
                print(f"   Converged: {'Yes' if converged else 'No'}")
            else:
                print(f"❌ Failed to evaluate {scenario_name}")
                
        except Exception as e:
            print(f"❌ Error evaluating {scenario_name}: {e}")
            continue
    
    total_time = time.time() - start_time
    
    # Generate aggregate summary
    if results:
        print("\n" + "=" * 80)
        print("📊 AGGREGATE RESULTS")
        print("=" * 80)
        
        avg_initial = sum(r['metrics_before']['quality_metrics']['overall_quality_score'] 
                         for r in results) / len(results)
        avg_final = sum(r['metrics_after']['quality_metrics']['overall_quality_score'] 
                       for r in results) / len(results)
        avg_improvement = avg_final - avg_initial
        success_rate = sum(1 for r in results if r['refinement_result']['converged']) / len(results)
        avg_iterations = sum(r['refinement_result']['iterations'] for r in results) / len(results)
        
        print(f"📈 Summary Statistics:")
        print(f"   Scenarios Evaluated: {len(results)}/{len(scenarios)}")
        print(f"   Average Initial Quality: {avg_initial:.3f}")
        print(f"   Average Final Quality: {avg_final:.3f}")
        print(f"   Average Improvement: {avg_improvement:+.3f} ({(avg_improvement/avg_initial)*100:+.1f}%)")
        print(f"   Success Rate: {success_rate:.1%}")
        print(f"   Average Iterations: {avg_iterations:.1f}")
        print(f"   Total Processing Time: {total_time:.2f}s")
        print()
        
        print(f"🤖 LLM Provider: {provider}")
        if model_name:
            print(f"🧠 Model: {model_name}")
    
    # Export aggregate results
    if export_path and results:
        export_aggregate_results(results, export_path)
    
    return results


def export_results(results: Dict[str, Any], export_path: str):
    """Export single evaluation results."""
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(export_path) if os.path.dirname(export_path) else '.', exist_ok=True)
    
    if export_path.endswith('.csv'):
        # Export metrics comparison as CSV
        calculator = BasicMetricsCalculator()
        
        # Convert back to MetricsResult objects
        from srlp_framework.core.metrics_calculator import MetricsResult
        
        metrics_before = MetricsResult(
            plan_metrics=results['metrics_before']['plan_metrics'],
            quality_metrics=results['metrics_before']['quality_metrics'],
            performance_metrics=results['metrics_before']['performance_metrics'],
            comparison_metrics=results['metrics_before']['comparison_metrics'],
            composite_scores=results['metrics_before']['composite_scores']
        )
        
        metrics_after = MetricsResult(
            plan_metrics=results['metrics_after']['plan_metrics'],
            quality_metrics=results['metrics_after']['quality_metrics'],
            performance_metrics=results['metrics_after']['performance_metrics'],
            comparison_metrics=results['metrics_after']['comparison_metrics'],
            composite_scores=results['metrics_after']['composite_scores']
        )
        
        calculator.export_comparison_to_csv(metrics_before, metrics_after, export_path)
        print(f"📄 Results exported to CSV: {export_path}")
        
    else:
        # Export as JSON
        json_path = export_path if export_path.endswith('.json') else export_path + '.json'
        with open(json_path, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"📄 Results exported to JSON: {json_path}")


def export_aggregate_results(results: List[Dict[str, Any]], export_path: str):
    """Export aggregate results from multiple evaluations."""
    
    os.makedirs(os.path.dirname(export_path) if os.path.dirname(export_path) else '.', exist_ok=True)
    
    if export_path.endswith('.csv'):
        # Create summary CSV
        import csv
        
        summary_data = []
        for result in results:
            scenario = result['scenario']
            before_quality = result['metrics_before']['quality_metrics']['overall_quality_score']
            after_quality = result['metrics_after']['quality_metrics']['overall_quality_score']
            improvement = after_quality - before_quality
            converged = result['refinement_result']['converged']
            iterations = result['refinement_result']['iterations']
            time_taken = result['refinement_result']['total_time']
            llm_info = result.get('llm_info', {})
            
            summary_data.append({
                'scenario': scenario,
                'initial_quality': before_quality,
                'final_quality': after_quality,
                'improvement': improvement,
                'improvement_percent': (improvement / max(0.001, before_quality)) * 100,
                'converged': converged,
                'iterations': iterations,
                'time_seconds': time_taken,
                'llm_provider': llm_info.get('provider', 'unknown'),
                'llm_model': llm_info.get('model', 'unknown')
            })
        
        with open(export_path, 'w', newline='') as csvfile:
            fieldnames = ['scenario', 'initial_quality', 'final_quality', 'improvement', 
                         'improvement_percent', 'converged', 'iterations', 'time_seconds',
                         'llm_provider', 'llm_model']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(summary_data)
        
        print(f"📄 Aggregate results exported to CSV: {export_path}")
        
    else:
        # Export as JSON
        aggregate_data = {
            'summary': {
                'total_scenarios': len(results),
                'avg_initial_quality': sum(r['metrics_before']['quality_metrics']['overall_quality_score'] 
                                         for r in results) / len(results),
                'avg_final_quality': sum(r['metrics_after']['quality_metrics']['overall_quality_score'] 
                                       for r in results) / len(results),
                'success_rate': sum(1 for r in results if r['refinement_result']['converged']) / len(results),
                'llm_provider': results[0].get('llm_info', {}).get('provider', 'unknown') if results else 'unknown'
            },
            'detailed_results': results
        }
        
        json_path = export_path if export_path.endswith('.json') else export_path + '.json'
        with open(json_path, 'w') as f:
            json.dump(aggregate_data, f, indent=2)
        
        print(f"📄 Aggregate results exported to JSON: {json_path}")


def main():
    """Main entry point for the evaluation script."""
    parser = argparse.ArgumentParser(
        description='SRLP Framework Evaluation with LLM Provider Support',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with OpenAI GPT-4
  python run_evaluation.py --provider openai --model gpt-4 --scenario travel --export results.csv
  
  # Run with Claude
  python run_evaluation.py --provider claude --model claude-3-sonnet-20240229 --scenario cooking
  
  # Run with local LLaMA via Ollama
  python run_evaluation.py --provider llama --model llama2 --scenario project
  
  # Run multiple scenarios with HuggingFace
  python run_evaluation.py --provider huggingface --model gpt2 --scenarios travel cooking project --export results.csv
  
  # Test all scenarios with mock provider
  python run_evaluation.py --provider mock --scenarios travel cooking project event renovation --export results.csv
        """
    )
    
    # Scenario selection
    scenario_group = parser.add_mutually_exclusive_group(required=True)
    scenario_group.add_argument('--scenario', type=str,
                               help='Single scenario to evaluate')
    scenario_group.add_argument('--scenarios', nargs='+',
                               help='Multiple scenarios to evaluate')
    
    # LLM Provider options
    parser.add_argument('--provider', type=str, default='mock',
                       help='LLM provider (openai, claude, llama, huggingface, mock)')
    parser.add_argument('--model', type=str,
                       help='Model name (uses provider default if not specified)')
    parser.add_argument('--api-key', type=str,
                       help='API key for the provider')
    parser.add_argument('--base-url', type=str,
                       help='Base URL for the provider API')
    parser.add_argument('--temperature', type=float, default=0.7,
                       help='Temperature for text generation (default: 0.7)')
    parser.add_argument('--max-tokens', type=int, default=1000,
                       help='Maximum tokens to generate (default: 1000)')
    
    # Framework options
    parser.add_argument('--iterations', type=int, default=3,
                       help='Maximum refinement iterations (default: 3)')
    
    # Output options
    parser.add_argument('--export', type=str,
                       help='Export results to file (CSV or JSON)')
    parser.add_argument('--visualize', action='store_true',
                       help='Generate visualization charts')
    
    # Utility options
    parser.add_argument('--list-scenarios', action='store_true',
                       help='List all available scenarios')
    parser.add_argument('--list-providers', action='store_true',
                       help='List all available LLM providers')
    
    args = parser.parse_args()
    
    # Handle utility commands
    if args.list_scenarios:
        scenarios = get_all_test_scenarios()
        print("Available scenarios:")
        print("=" * 40)
        for scenario in scenarios:
            print(f"Name: {scenario['name']}")
            print(f"Type: {scenario['problem']['type']}")
            print(f"Goal: {scenario['problem']['goal']}")
            print("-" * 40)
        return
    
    if args.list_providers:
        providers = list_available_providers()
        print("Available LLM providers:")
        print("=" * 50)
        for provider_name, info in providers.items():
            print(f"Provider: {provider_name}")
            print(f"Description: {info['description']}")
            print(f"Default Model: {info['default_model']}")
            print(f"Requires API Key: {info['requires_api_key']}")
            if info.get('api_key_env_var'):
                print(f"API Key Environment Variable: {info['api_key_env_var']}")
            print("-" * 50)
        return
    
    # Prepare LLM configuration
    llm_kwargs = {
        'temperature': args.temperature,
        'max_tokens': args.max_tokens
    }
    
    if args.api_key:
        llm_kwargs['api_key'] = args.api_key
    if args.base_url:
        llm_kwargs['base_url'] = args.base_url
    
    # Ensure results directory exists
    os.makedirs('results', exist_ok=True)
    
    try:
        if args.scenarios:
            # Run multiple scenarios
            results = run_multiple_evaluations(
                scenarios=args.scenarios,
                provider=args.provider,
                model_name=args.model,
                export_path=args.export,
                iterations=args.iterations,
                **llm_kwargs
            )
            
            # Generate visualizations if requested
            if args.visualize and results:
                print("\n📊 Generating visualizations...")
                viz_dir = os.path.join(os.path.dirname(args.export) if args.export else 'results', 'visualizations')
                generate_all_visualizations(results, viz_dir)
                print(f"📊 Visualizations saved to: {viz_dir}")
            
        else:
            # Run single scenario
            result = run_evaluation_with_llm(
                scenario_name=args.scenario,
                provider=args.provider,
                model_name=args.model,
                export_path=args.export,
                iterations=args.iterations,
                **llm_kwargs
            )
            
            # Generate visualizations if requested
            if args.visualize and result:
                print("\n📊 Generating visualizations...")
                viz_dir = os.path.join(os.path.dirname(args.export) if args.export else 'results', 'visualizations')
                generate_all_visualizations([result], viz_dir)
                print(f"📊 Visualizations saved to: {viz_dir}")
        
        print("\n🎉 Evaluation completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

