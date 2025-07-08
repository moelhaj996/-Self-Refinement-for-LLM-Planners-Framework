#!/usr/bin/env python3
"""
Simple demonstration of the SRLP Framework functionality.
This script runs a basic refinement process using the local implementation.
"""

import json
import time
from refinement_engine import create_refinement_engine

def create_sample_problem():
    """Create a sample travel planning problem."""
    return {
        "type": "travel_planning",
        "goal": "Plan a 3-day trip to Paris",
        "constraints": [
            "Budget: $1500",
            "Must visit Eiffel Tower",
            "Prefer public transportation",
            "Need accommodation near city center"
        ],
        "requirements": [
            "Daily itinerary",
            "Transportation details",
            "Accommodation booking",
            "Budget breakdown"
        ]
    }

def run_demo():
    """Run a demonstration of the SRLP framework."""
    print("=" * 60)
    print("SRLP Framework - Self-Refinement for LLM Planners")
    print("=" * 60)
    print()
    
    # Create sample problem
    problem = create_sample_problem()
    print("Sample Problem:")
    print(f"Type: {problem['type']}")
    print(f"Goal: {problem['goal']}")
    print(f"Constraints: {', '.join(problem['constraints'])}")
    print(f"Requirements: {', '.join(problem['requirements'])}")
    print()
    
    # Create refinement engine
    print("Initializing Refinement Engine...")
    try:
        engine = create_refinement_engine(provider="mock", max_iterations=3)
        print("✅ Refinement engine created successfully")
        
        # Get provider info
        provider_info = engine.llm.get_provider_info()
        print(f"LLM Provider: {provider_info.get('provider', 'unknown')}")
        print(f"Model: {provider_info.get('model', 'unknown')}")
        print()
        
    except Exception as e:
        print(f"❌ Error creating refinement engine: {e}")
        return
    
    # Run refinement process
    print("Running Refinement Process...")
    print("-" * 40)
    
    try:
        start_time = time.time()
        result = engine.refine_plan(problem)
        end_time = time.time()
        
        print("✅ Refinement completed successfully!")
        print()
        
        # Display results
        print("Results Summary:")
        print("-" * 40)
        print(f"Iterations: {result.iterations}")
        print(f"Converged: {'Yes' if result.converged else 'No'}")
        print(f"Processing Time: {end_time - start_time:.2f}s")
        print(f"Improvement Score: {result.improvement_score:.3f}")
        print()
        
        # Show initial plan
        print("Initial Plan:")
        print("-" * 20)
        if hasattr(result, 'initial_plan') and result.initial_plan:
            if isinstance(result.initial_plan, dict):
                print(json.dumps(result.initial_plan, indent=2))
            else:
                print(result.initial_plan)
        else:
            print("No initial plan available")
        print()
        
        # Show final plan
        print("Final Plan:")
        print("-" * 20)
        if hasattr(result, 'final_plan') and result.final_plan:
            if isinstance(result.final_plan, dict):
                print(json.dumps(result.final_plan, indent=2))
            else:
                print(result.final_plan)
        else:
            print("No final plan available")
        print()
        
        # Show refinement history
        if hasattr(result, 'refinement_history') and result.refinement_history:
            print(f"Refinement History ({len(result.refinement_history)} iterations):")
            print("-" * 30)
            for i, iteration in enumerate(result.refinement_history, 1):
                print(f"Iteration {i}:")
                if 'check_result' in iteration:
                    check = iteration['check_result']
                    print(f"  Overall Score: {check.get('overall_score', 'N/A')}")
                    print(f"  Error Count: {check.get('error_count', 'N/A')}")
                    print(f"  Completeness: {check.get('completeness_score', 'N/A')}")
                if 'feedback' in iteration:
                    feedback = iteration['feedback']
                    if isinstance(feedback, dict):
                        print(f"  Feedback: {feedback.get('summary', 'No summary')}")
                    else:
                        print(f"  Feedback: {str(feedback)[:100]}...")
                print()
        
        print("=" * 60)
        print("Demo completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error during refinement: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_demo()