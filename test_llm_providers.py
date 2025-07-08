"""
Comprehensive test script for LLM providers in the SRLP framework.
Tests all provider types and demonstrates plug-and-play functionality.
"""

import sys
import os
import time
from typing import Dict, Any

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from srlp_framework.llm_providers import (
    LLMFactory, list_available_providers, create_best_available_llm,
    MockLLM, LLMConfig
)
from srlp_framework.core.plan_generator import create_plan_generator
from refinement_engine import create_refinement_engine
from srlp_framework.test_scenarios import get_scenario_by_name


def test_provider_creation():
    """Test creating different LLM providers."""
    print("🧪 Testing LLM Provider Creation")
    print("=" * 50)
    
    providers_to_test = ['mock', 'openai', 'claude', 'llama', 'huggingface']
    
    for provider in providers_to_test:
        print(f"\n🔧 Testing {provider} provider...")
        try:
            llm = LLMFactory.create_llm(provider)
            info = llm.get_provider_info()
            print(f"✅ Created: {info.get('provider', 'unknown')} - {info.get('model', 'unknown')}")
            
            # Test connection
            if llm.test_connection():
                print(f"✅ Connection: Working")
            else:
                print(f"⚠️  Connection: Failed (expected for non-mock providers without API keys)")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)


def test_plan_generation():
    """Test plan generation with different providers."""
    print("\n🧪 Testing Plan Generation with Different Providers")
    print("=" * 60)
    
    # Load a test problem
    scenario = get_scenario_by_name('travel')
    problem = scenario['problem']
    
    print(f"📝 Test Problem: {problem.get('goal', 'No goal')}")
    print(f"🎯 Type: {problem.get('type', 'general')}")
    
    providers_to_test = ['mock']  # Start with mock, can add others with API keys
    
    for provider in providers_to_test:
        print(f"\n🤖 Testing with {provider} provider...")
        try:
            # Create plan generator
            plan_generator = create_plan_generator(provider=provider)
            
            # Generate plan
            start_time = time.time()
            plan = plan_generator.generate_plan(problem)
            generation_time = time.time() - start_time
            
            print(f"✅ Plan generated in {generation_time:.3f}s")
            print(f"📊 Confidence: {plan.confidence_score:.3f}")
            print(f"📝 Steps ({len(plan.steps)}):")
            for i, step in enumerate(plan.steps[:3], 1):  # Show first 3 steps
                print(f"   {i}. {step}")
            if len(plan.steps) > 3:
                print(f"   ... and {len(plan.steps) - 3} more steps")
            
            print(f"🔧 Provider: {plan.metadata.get('provider', 'unknown')}")
            print(f"🧠 Model: {plan.metadata.get('model', 'unknown')}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)


def test_refinement_process():
    """Test the complete refinement process."""
    print("\n🧪 Testing Complete Refinement Process")
    print("=" * 60)
    
    # Load test scenario
    scenario = get_scenario_by_name('cooking')
    problem = scenario['problem']
    
    print(f"📝 Test Problem: {problem.get('goal', 'No goal')}")
    
    try:
        # Create refinement engine with mock provider
        refinement_engine = create_refinement_engine(
            provider='mock',
            max_iterations=2  # Keep it short for testing
        )
        
        print(f"🤖 Using: {refinement_engine.get_provider_info()}")
        
        # Run refinement
        print("\n🔄 Running refinement process...")
        start_time = time.time()
        result = refinement_engine.refine_plan(problem)
        total_time = time.time() - start_time
        
        print(f"✅ Refinement completed in {total_time:.3f}s")
        print(f"🔄 Iterations: {result.iterations}")
        print(f"✅ Converged: {'Yes' if result.converged else 'No'}")
        print(f"📈 Improvement: {result.improvement_score:+.3f}")
        
        # Show initial vs final plan
        print(f"\n📊 Initial Plan Quality: {result.refinement_history[0]['quality_score']:.3f}")
        print(f"📊 Final Plan Quality: {result.refinement_history[-1]['quality_score']:.3f}")
        
        print(f"\n📝 Initial Plan Steps:")
        for i, step in enumerate(result.initial_plan.steps[:2], 1):
            print(f"   {i}. {step}")
        
        print(f"\n📝 Final Plan Steps:")
        for i, step in enumerate(result.final_plan.steps[:2], 1):
            print(f"   {i}. {step}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)


def test_provider_switching():
    """Test switching between providers."""
    print("\n🧪 Testing Provider Switching")
    print("=" * 50)
    
    try:
        # Create initial plan generator
        plan_generator = create_plan_generator(provider='mock')
        print(f"🤖 Initial provider: {plan_generator.get_provider_info()}")
        
        # Switch to different provider (mock again for testing)
        plan_generator.switch_provider('mock', model_name='mock-model-v2')
        print(f"🔄 Switched to: {plan_generator.get_provider_info()}")
        
        # Test that it still works
        scenario = get_scenario_by_name('project')
        problem = scenario['problem']
        
        plan = plan_generator.generate_plan(problem)
        print(f"✅ Plan generated with new provider")
        print(f"📊 Confidence: {plan.confidence_score:.3f}")
        print(f"📝 Steps: {len(plan.steps)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)


def test_provider_info():
    """Test provider information and listing."""
    print("\n🧪 Testing Provider Information")
    print("=" * 50)
    
    # List all available providers
    providers = list_available_providers()
    print(f"📋 Available providers: {len(providers)}")
    
    for provider_name, info in providers.items():
        print(f"\n🤖 {provider_name.upper()}")
        print(f"   Description: {info['description']}")
        print(f"   Default Model: {info['default_model']}")
        print(f"   Requires API Key: {info['requires_api_key']}")
        if info.get('features'):
            print(f"   Features: {', '.join(info['features'])}")
    
    print("\n" + "=" * 50)


def test_error_handling():
    """Test error handling and fallbacks."""
    print("\n🧪 Testing Error Handling and Fallbacks")
    print("=" * 50)
    
    # Test invalid provider
    try:
        print("🔧 Testing invalid provider...")
        llm = LLMFactory.create_llm('invalid_provider')
        print("❌ Should have failed!")
    except Exception as e:
        print(f"✅ Correctly caught error: {type(e).__name__}")
    
    # Test auto-selection
    try:
        print("\n🔧 Testing auto-selection...")
        llm = create_best_available_llm()
        info = llm.get_provider_info()
        print(f"✅ Auto-selected: {info.get('provider', 'unknown')}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)


def run_comprehensive_test():
    """Run all tests."""
    print("🚀 SRLP Framework - LLM Provider Comprehensive Test")
    print("=" * 80)
    
    test_provider_creation()
    test_plan_generation()
    test_refinement_process()
    test_provider_switching()
    test_provider_info()
    test_error_handling()
    
    print("\n🎉 All tests completed!")
    print("=" * 80)


if __name__ == "__main__":
    run_comprehensive_test()

