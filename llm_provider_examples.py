"""
Examples demonstrating how to use different LLM providers with the SRLP framework.
Shows the plug-and-play nature of the LLM abstraction.
"""

import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from srlp_framework.llm_providers import LLMFactory, create_best_available_llm
from srlp_framework.core.plan_generator import create_plan_generator
from refinement_engine import create_refinement_engine
from srlp_framework.test_scenarios import get_scenario_by_name


def example_1_basic_provider_usage():
    """Example 1: Basic usage with different providers."""
    print("🔧 Example 1: Basic Provider Usage")
    print("=" * 50)
    
    # Create different providers
    providers = [
        ('mock', None),  # Mock provider for testing
        # Uncomment these when you have API keys:
        # ('openai', 'gpt-3.5-turbo'),
        # ('claude', 'claude-3-sonnet-20240229'),
        # ('llama', 'llama2'),  # Requires Ollama running
        # ('huggingface', 'gpt2'),  # Requires transformers library
    ]
    
    for provider, model in providers:
        print(f"\n🤖 Testing {provider} provider...")
        try:
            # Create LLM instance
            llm = LLMFactory.create_llm(provider, model)
            
            # Get provider info
            info = llm.get_provider_info()
            print(f"✅ Created: {info.get('provider')} - {info.get('model')}")
            
            # Test basic generation
            response = llm.generate("Hello, how are you?", max_tokens=50)
            print(f"📝 Response: {response.content[:100]}...")
            print(f"⏱️  Time: {response.response_time:.3f}s")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)


def example_2_plan_generation_comparison():
    """Example 2: Compare plan generation across providers."""
    print("\n🔧 Example 2: Plan Generation Comparison")
    print("=" * 60)
    
    # Load a test scenario
    scenario = get_scenario_by_name('travel')
    problem = scenario['problem']
    
    print(f"📝 Problem: {problem.get('goal')}")
    
    # Test with available providers
    providers = ['mock']  # Add more when you have API keys
    
    for provider in providers:
        print(f"\n🤖 Using {provider} provider...")
        try:
            # Create plan generator
            plan_generator = create_plan_generator(provider=provider)
            
            # Generate plan
            plan = plan_generator.generate_plan(problem)
            
            print(f"✅ Generated plan with {len(plan.steps)} steps")
            print(f"📊 Confidence: {plan.confidence_score:.3f}")
            print(f"⏱️  Time: {plan.generation_time:.3f}s")
            print(f"📝 First 2 steps:")
            for i, step in enumerate(plan.steps[:2], 1):
                print(f"   {i}. {step}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)


def example_3_refinement_with_different_providers():
    """Example 3: Refinement process with different providers."""
    print("\n🔧 Example 3: Refinement with Different Providers")
    print("=" * 60)
    
    # Load scenario
    scenario = get_scenario_by_name('cooking')
    problem = scenario['problem']
    
    print(f"📝 Problem: {problem.get('goal')}")
    
    providers = ['mock']  # Add more when you have API keys
    
    for provider in providers:
        print(f"\n🤖 Using {provider} provider...")
        try:
            # Create refinement engine
            engine = create_refinement_engine(
                provider=provider,
                max_iterations=2  # Keep short for demo
            )
            
            # Run refinement
            result = engine.refine_plan(problem)
            
            print(f"✅ Refinement completed")
            print(f"🔄 Iterations: {result.iterations}")
            print(f"📈 Improvement: {result.improvement_score:+.3f}")
            print(f"⏱️  Total time: {result.total_time:.3f}s")
            
            # Show quality progression
            qualities = [h['quality_score'] for h in result.refinement_history]
            print(f"📊 Quality progression: {' → '.join(f'{q:.3f}' for q in qualities)}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)


def example_4_provider_switching():
    """Example 4: Dynamic provider switching."""
    print("\n🔧 Example 4: Dynamic Provider Switching")
    print("=" * 50)
    
    # Create initial plan generator
    plan_generator = create_plan_generator(provider='mock')
    
    scenario = get_scenario_by_name('project')
    problem = scenario['problem']
    
    print(f"📝 Problem: {problem.get('goal')}")
    
    # Generate plan with initial provider
    print(f"\n🤖 Initial provider: {plan_generator.get_provider_info()}")
    plan1 = plan_generator.generate_plan(problem)
    print(f"✅ Plan 1: {len(plan1.steps)} steps, confidence {plan1.confidence_score:.3f}")
    
    # Switch provider and generate again
    plan_generator.switch_provider('mock', model_name='mock-model-v2')
    print(f"\n🔄 Switched to: {plan_generator.get_provider_info()}")
    plan2 = plan_generator.generate_plan(problem)
    print(f"✅ Plan 2: {len(plan2.steps)} steps, confidence {plan2.confidence_score:.3f}")
    
    # Compare plans
    print(f"\n📊 Comparison:")
    print(f"   Plan 1 confidence: {plan1.confidence_score:.3f}")
    print(f"   Plan 2 confidence: {plan2.confidence_score:.3f}")
    print(f"   Difference: {plan2.confidence_score - plan1.confidence_score:+.3f}")
    
    print("\n" + "=" * 50)


def example_5_configuration_options():
    """Example 5: Different configuration options."""
    print("\n🔧 Example 5: Configuration Options")
    print("=" * 50)
    
    # Test different temperature settings
    temperatures = [0.1, 0.7, 1.0]
    
    for temp in temperatures:
        print(f"\n🌡️  Temperature: {temp}")
        try:
            # Create plan generator with specific temperature
            plan_generator = create_plan_generator(
                provider='mock',
                temperature=temp,
                max_tokens=500
            )
            
            scenario = get_scenario_by_name('event')
            problem = scenario['problem']
            
            plan = plan_generator.generate_plan(problem)
            print(f"✅ Generated plan: {len(plan.steps)} steps")
            print(f"📊 Confidence: {plan.confidence_score:.3f}")
            print(f"🌡️  Used temperature: {plan.metadata.get('temperature', 'unknown')}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)


def example_6_real_world_usage():
    """Example 6: Real-world usage patterns."""
    print("\n🔧 Example 6: Real-World Usage Patterns")
    print("=" * 60)
    
    print("🎯 Pattern 1: Auto-select best available provider")
    try:
        llm = create_best_available_llm()
        info = llm.get_provider_info()
        print(f"✅ Auto-selected: {info.get('provider')} - {info.get('model')}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n🎯 Pattern 2: Environment-based configuration")
    # Set environment variables for demonstration
    os.environ['SRLP_LLM_PROVIDER'] = 'mock'
    os.environ['SRLP_LLM_MODEL'] = 'mock-model-env'
    
    try:
        from srlp_framework.llm_providers import create_llm_from_env
        llm = create_llm_from_env()
        info = llm.get_provider_info()
        print(f"✅ From environment: {info.get('provider')} - {info.get('model')}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n🎯 Pattern 3: Configuration from dictionary")
    config_dict = {
        'provider': 'mock',
        'model_name': 'mock-model-dict',
        'temperature': 0.5,
        'max_tokens': 800
    }
    
    try:
        llm = LLMFactory.create_from_config_dict(config_dict)
        info = llm.get_provider_info()
        print(f"✅ From config dict: {info.get('provider')} - {info.get('model')}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)


def run_all_examples():
    """Run all examples."""
    print("🚀 SRLP Framework - LLM Provider Examples")
    print("=" * 80)
    
    example_1_basic_provider_usage()
    example_2_plan_generation_comparison()
    example_3_refinement_with_different_providers()
    example_4_provider_switching()
    example_5_configuration_options()
    example_6_real_world_usage()
    
    print("\n🎉 All examples completed!")
    print("\n💡 To use real LLM providers:")
    print("   1. Install required libraries (openai, anthropic, transformers, etc.)")
    print("   2. Set up API keys in environment variables")
    print("   3. For LLaMA: Install and run Ollama locally")
    print("   4. Uncomment the provider examples above")
    print("=" * 80)


if __name__ == "__main__":
    run_all_examples()

