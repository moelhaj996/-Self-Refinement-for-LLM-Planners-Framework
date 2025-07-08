"""Script to run the SRLP framework project."""

import os
import sys

# Add the parent directory to the Python path
sys.path.append('/Users/mohamedelhajsuliman/Desktop/Mohamed 2025 summer thesis')

# Import necessary modules
from srlp_framework.core.refinement_engine import RefinementEngine
from srlp_framework.llm_providers import LLMFactory
from srlp_framework.test_scenarios import get_scenario_by_name

def create_refinement_engine(provider="mock", model_name=None, max_iterations=3, **kwargs):
    """
    Create a refinement engine with the specified LLM provider.
    
    Args:
        provider: LLM provider name ('openai', 'claude', 'llama', 'huggingface', 'mock')
        model_name: Model name (optional, uses provider default)
        max_iterations: Maximum number of refinement iterations
        **kwargs: Additional LLM configuration parameters
        
    Returns:
        RefinementEngine instance
    """
    # Create LLM instance
    llm = LLMFactory.create_llm(provider, model_name, **kwargs)
    
    # Create and return refinement engine
    return RefinementEngine(llm=llm, max_iterations=max_iterations)

def run_example():
    """Run a simple example using the SRLP framework."""
    print("Running SRLP Framework Example")
    print("=" * 50)
    
    # Load a test scenario
    scenario = get_scenario_by_name('travel')
    problem = scenario['problem']
    
    print(f"Problem: {problem.get('goal')}")
    
    # Create refinement engine with mock provider
    refinement_engine = create_refinement_engine(
        provider='mock',
        max_iterations=2  # Keep it short for testing
    )
    
    print(f"Using: {refinement_engine.get_provider_info()}")
    
    # Run refinement
    print("\nRunning refinement process...")
    result = refinement_engine.refine_plan(problem)
    
    print(f"Refinement completed in {result.total_time:.3f}s")
    print(f"Iterations: {result.iterations}")
    print(f"Converged: {'Yes' if result.converged else 'No'}")
    print(f"Improvement: {result.improvement_score:+.3f}")
    
    # Show initial vs final plan
    print(f"\nInitial Plan Quality: {result.refinement_history[0]['quality_score']:.3f}")
    print(f"Final Plan Quality: {result.refinement_history[-1]['quality_score']:.3f}")
    
    print(f"\nInitial Plan Steps:")
    for i, step in enumerate(result.initial_plan.steps[:3], 1):
        print(f"   {i}. {step}")
    
    print(f"\nFinal Plan Steps:")
    for i, step in enumerate(result.final_plan.steps[:3], 1):
        print(f"   {i}. {step}")

if __name__ == "__main__":
    run_example()