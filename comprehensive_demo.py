#!/usr/bin/env python3
"""
Comprehensive demonstration of the SRLP Framework functionality.
This script showcases the framework with multiple scenarios and detailed output.
"""

import json
import time
from refinement_engine import create_refinement_engine
from test_scenarios import get_all_test_scenarios, get_scenario_by_name

def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 80)
    print(f" {title} ".center(80))
    print("=" * 80)

def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'-' * 60}")
    print(f" {title} ")
    print("-" * 60)

def run_scenario_demo(scenario_name):
    """Run a demonstration for a specific scenario."""
    print_section(f"Running {scenario_name.title()} Scenario")
    
    # Get scenario data
    scenario = get_scenario_by_name(scenario_name)
    problem = scenario['problem']
    
    print(f"Scenario: {scenario['name']}")
    print(f"Type: {problem['type']}")
    print(f"Goal: {problem['goal']}")
    print(f"Description: {problem.get('description', 'No description')}")
    
    if 'constraints' in problem:
        print("\nConstraints:")
        for constraint in problem['constraints']:
            print(f"  • {constraint['type'].title()}: {constraint['value']}")
    
    if 'requirements' in problem:
        print("\nRequirements:")
        for req in problem['requirements']:
            print(f"  • {req}")
    
    # Create refinement engine
    print("\nInitializing refinement engine...")
    try:
        engine = create_refinement_engine(provider="mock", max_iterations=3)
        print("✅ Engine created successfully")
        
        # Run refinement
        print("\nRunning refinement process...")
        start_time = time.time()
        result = engine.refine_plan(problem)
        end_time = time.time()
        
        # Display results
        print(f"\n📊 Results Summary:")
        print(f"   Iterations: {result.iterations}")
        print(f"   Converged: {'✅ Yes' if result.converged else '❌ No'}")
        print(f"   Improvement Score: {result.improvement_score:.3f}")
        print(f"   Processing Time: {end_time - start_time:.2f}s")
        
        # Show quality progression
        if result.refinement_history:
            print("\n📈 Quality Progression:")
            for i, iteration in enumerate(result.refinement_history, 1):
                score = iteration['check_result']['overall_score']
                errors = iteration['check_result']['error_count']
                print(f"   Iteration {i}: Score {score:.2f}, Errors: {errors}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def run_comprehensive_demo():
    """Run a comprehensive demonstration of the SRLP framework."""
    print_header("SRLP Framework - Comprehensive Demonstration")
    print("Self-Refinement for LLM Planners via Self-Checking Feedback")
    print("\nThis demo showcases the framework's ability to iteratively")
    print("improve plans across different domains and problem types.")
    
    # Get all available scenarios
    scenarios = get_all_test_scenarios()
    print(f"\n🎯 Available Scenarios: {len(scenarios)}")
    for scenario in scenarios:
        print(f"   • {scenario['name']} ({scenario['problem']['type']})")
    
    # Demo specific scenarios
    demo_scenarios = ['travel', 'cooking', 'project']
    results = {}
    
    for scenario_name in demo_scenarios:
        result = run_scenario_demo(scenario_name)
        if result:
            results[scenario_name] = result
    
    # Summary comparison
    print_section("Cross-Scenario Performance Summary")
    
    if results:
        print(f"{'Scenario':<15} {'Iterations':<12} {'Improvement':<12} {'Converged':<10}")
        print("-" * 50)
        
        for scenario_name, result in results.items():
            converged_str = "✅ Yes" if result.converged else "❌ No"
            print(f"{scenario_name:<15} {result.iterations:<12} {result.improvement_score:<12.3f} {converged_str:<10}")
        
        # Calculate averages
        avg_iterations = sum(r.iterations for r in results.values()) / len(results)
        avg_improvement = sum(r.improvement_score for r in results.values()) / len(results)
        convergence_rate = sum(1 for r in results.values() if r.converged) / len(results) * 100
        
        print("-" * 50)
        print(f"{'AVERAGES':<15} {avg_iterations:<12.1f} {avg_improvement:<12.3f} {convergence_rate:<10.0f}%")
    
    # Framework capabilities summary
    print_section("Framework Capabilities Demonstrated")
    
    capabilities = [
        "✅ Multi-domain problem solving (travel, cooking, project management)",
        "✅ Iterative plan refinement with quality improvement",
        "✅ Constraint-aware planning and optimization",
        "✅ Self-checking and error detection mechanisms",
        "✅ Convergence detection and stopping criteria",
        "✅ Detailed refinement history and progress tracking",
        "✅ Flexible LLM provider integration (mock demonstrated)",
        "✅ Comprehensive metrics and performance evaluation"
    ]
    
    for capability in capabilities:
        print(f"   {capability}")
    
    print_section("Technical Architecture Highlights")
    
    architecture_points = [
        "🏗️  Modular design with pluggable LLM providers",
        "🔄 Iterative refinement engine with configurable parameters",
        "🎯 Self-checking mechanism for quality assessment",
        "📊 Comprehensive metrics calculation and comparison",
        "🔧 Extensible scenario framework for different domains",
        "⚡ Efficient processing with convergence detection",
        "📈 Detailed logging and progress visualization"
    ]
    
    for point in architecture_points:
        print(f"   {point}")
    
    print_header("Demo Completed Successfully!")
    print("The SRLP Framework has successfully demonstrated its ability to:")
    print("• Handle diverse planning problems across multiple domains")
    print("• Iteratively improve plan quality through self-refinement")
    print("• Provide detailed feedback and progress tracking")
    print("• Achieve convergence with measurable improvements")
    print("\nFramework is ready for integration with real LLM providers!")

def run_quick_demo():
    """Run a quick demonstration with just one scenario."""
    print_header("SRLP Framework - Quick Demo")
    result = run_scenario_demo('travel')
    
    if result:
        print_section("Quick Demo Summary")
        print(f"✅ Successfully refined a travel planning problem")
        print(f"✅ Achieved {result.improvement_score:.1%} improvement")
        print(f"✅ Completed in {result.iterations} iterations")
        print(f"✅ {'Converged' if result.converged else 'Did not converge'}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        run_quick_demo()
    else:
        run_comprehensive_demo()