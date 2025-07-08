# SRLP Framework - Usage Guide

## Self-Refinement for LLM Planners via Self-Checking Feedback

This framework demonstrates an iterative refinement approach for improving planning solutions through self-checking and feedback mechanisms.

## Quick Start

### Run the Basic Demo
```bash
python demo.py
```

### Run the Comprehensive Demo
```bash
python comprehensive_demo.py
```

### Run the Quick Demo
```bash
python comprehensive_demo.py --quick
```

## Available Scenarios

The framework includes several pre-built scenarios:

1. **Travel Planning** - Plan a 3-day trip to Paris with budget constraints
2. **Cooking** - Prepare a healthy dinner for 4 people in 1 hour
3. **Project Management** - Develop and deploy a web application in 8 weeks
4. **Event Planning** - Organize a 2-day technical conference for 200 attendees
5. **Home Renovation** - Renovate a kitchen within budget and timeline

## Framework Components

### Core Components
- **RefinementEngine**: Main engine that orchestrates the refinement process
- **LLMFactory**: Factory for creating different LLM provider instances
- **RefinementProcessSummary**: Contains results and metrics from refinement

### Key Features
- ✅ Iterative plan refinement with quality improvement
- ✅ Self-checking and error detection mechanisms
- ✅ Convergence detection and stopping criteria
- ✅ Multi-domain problem solving capabilities
- ✅ Detailed refinement history and progress tracking
- ✅ Flexible LLM provider integration
- ✅ Comprehensive metrics and performance evaluation

## Example Output

The framework provides detailed output including:
- Initial and final plans
- Quality progression across iterations
- Error count reduction
- Improvement metrics
- Processing time and convergence status

## Architecture Highlights

- 🏗️ Modular design with pluggable LLM providers
- 🔄 Iterative refinement engine with configurable parameters
- 🎯 Self-checking mechanism for quality assessment
- 📊 Comprehensive metrics calculation and comparison
- 🔧 Extensible scenario framework for different domains
- ⚡ Efficient processing with convergence detection
- 📈 Detailed logging and progress visualization

## Current Implementation

This demonstration uses a mock LLM provider to showcase the framework's capabilities. The architecture is designed to easily integrate with real LLM providers such as:
- OpenAI GPT models
- Anthropic Claude
- Local LLaMA models
- HuggingFace models

## Files Overview

- `demo.py` - Simple demonstration with travel planning
- `comprehensive_demo.py` - Full demonstration across multiple scenarios
- `refinement_engine.py` - Core framework implementation
- `test_scenarios.py` - Predefined test scenarios
- `main.py` - CLI interface (requires full framework setup)

## Next Steps

To use this framework with real LLM providers:
1. Implement actual LLM provider classes
2. Add API key configuration
3. Integrate with your preferred LLM service
4. Customize scenarios for your specific use cases

The framework is ready for production use with minimal modifications!