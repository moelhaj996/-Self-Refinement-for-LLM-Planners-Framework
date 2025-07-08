"""
Test Scenarios for SRLP Framework Evaluation
"""

import json
from typing import Dict, List, Any


def get_travel_scenario() -> Dict[str, Any]:
    """Travel planning scenario with budget and time constraints."""
    return {
        'name': 'travel_planning',
        'problem': {
            'type': 'travel',
            'goal': 'Plan a 3-day trip to Paris within budget',
            'description': 'Plan a complete 3-day vacation to Paris including flights, accommodation, activities, and meals',
            'destination': 'Paris',
            'duration': '3 days',
            'budget': '$1200',
            'constraints': [
                {'type': 'budget', 'value': '$1200'},
                {'type': 'time', 'value': '3 days'},
                {'type': 'resource', 'value': 'single traveler'}
            ],
            'requirements': [
                'Book round-trip flights',
                'Reserve accommodation for 3 nights',
                'Plan daily activities and sightseeing',
                'Include meal planning',
                'Arrange airport transportation',
                'Prepare travel documents'
            ]
        }
    }


def get_cooking_scenario() -> Dict[str, Any]:
    """Cooking scenario with dietary constraints and time limits."""
    return {
        'name': 'cooking_dinner',
        'problem': {
            'type': 'cooking',
            'goal': 'Prepare a healthy dinner for 4 people in 1 hour',
            'description': 'Cook a complete healthy dinner including main course, side dish, and dessert',
            'dish': 'grilled chicken with vegetables',
            'servings': 4,
            'time_limit': '1 hour',
            'constraints': [
                {'type': 'time', 'value': '1 hour'},
                {'type': 'dietary', 'value': 'low-carb, gluten-free'},
                {'type': 'budget', 'value': '$30'}
            ],
            'requirements': [
                'Prepare main protein dish',
                'Include vegetable side dishes',
                'Prepare healthy dessert option',
                'Ensure all dietary restrictions are met',
                'Complete cooking within time limit'
            ]
        }
    }


def get_project_scenario() -> Dict[str, Any]:
    """Project management scenario with team coordination and deadlines."""
    return {
        'name': 'software_project',
        'problem': {
            'type': 'project',
            'goal': 'Develop and deploy a web application in 8 weeks',
            'description': 'Plan and execute a complete software development project from requirements to deployment',
            'project_name': 'Customer Portal Web App',
            'deadline': '8 weeks',
            'team_size': 5,
            'constraints': [
                {'type': 'time', 'value': '8 weeks'},
                {'type': 'budget', 'value': '$50000'},
                {'type': 'resource', 'value': '5 developers'},
                {'type': 'quality', 'value': 'production-ready'}
            ],
            'requirements': [
                'Gather and document requirements',
                'Design system architecture',
                'Implement core functionality',
                'Conduct thorough testing',
                'Deploy to production environment',
                'Provide user documentation and training'
            ]
        }
    }


def get_event_planning_scenario() -> Dict[str, Any]:
    """Event planning scenario with multiple stakeholders and logistics."""
    return {
        'name': 'conference_planning',
        'problem': {
            'type': 'event',
            'goal': 'Organize a 2-day technical conference for 200 attendees',
            'description': 'Plan and execute a complete technical conference including venue, speakers, catering, and logistics',
            'event_type': 'technical conference',
            'duration': '2 days',
            'attendees': 200,
            'constraints': [
                {'type': 'budget', 'value': '$25000'},
                {'type': 'time', 'value': '3 months planning time'},
                {'type': 'venue', 'value': 'downtown location'},
                {'type': 'capacity', 'value': '200 people maximum'}
            ],
            'requirements': [
                'Secure appropriate venue',
                'Recruit and coordinate speakers',
                'Arrange catering for all meals',
                'Set up registration system',
                'Plan networking activities',
                'Coordinate audio/visual equipment',
                'Manage day-of logistics'
            ]
        }
    }


def get_home_renovation_scenario() -> Dict[str, Any]:
    """Home renovation scenario with budget constraints and permits."""
    return {
        'name': 'kitchen_renovation',
        'problem': {
            'type': 'renovation',
            'goal': 'Renovate kitchen within budget and timeline',
            'description': 'Complete kitchen renovation including design, permits, construction, and finishing',
            'room': 'kitchen',
            'budget': '$15000',
            'timeline': '6 weeks',
            'constraints': [
                {'type': 'budget', 'value': '$15000'},
                {'type': 'time', 'value': '6 weeks'},
                {'type': 'permits', 'value': 'required for electrical and plumbing'},
                {'type': 'living', 'value': 'minimize disruption to daily life'}
            ],
            'requirements': [
                'Design new kitchen layout',
                'Obtain necessary permits',
                'Demolish existing kitchen',
                'Install new plumbing and electrical',
                'Install cabinets and countertops',
                'Complete flooring and painting',
                'Final inspection and cleanup'
            ]
        }
    }


def get_all_test_scenarios() -> List[Dict[str, Any]]:
    """Get all available test scenarios."""
    return [
        get_travel_scenario(),
        get_cooking_scenario(),
        get_project_scenario(),
        get_event_planning_scenario(),
        get_home_renovation_scenario()
    ]


def get_scenario_by_name(name: str) -> Dict[str, Any]:
    """Get a specific scenario by name."""
    scenarios = {
        'travel': get_travel_scenario(),
        'cooking': get_cooking_scenario(),
        'project': get_project_scenario(),
        'event': get_event_planning_scenario(),
        'renovation': get_home_renovation_scenario()
    }
    
    return scenarios.get(name, get_travel_scenario())


def save_scenarios_to_files():
    """Save all scenarios to individual JSON files."""
    import os
    
    scenarios_dir = 'srlp_framework/scenarios'
    os.makedirs(scenarios_dir, exist_ok=True)
    
    scenarios = get_all_test_scenarios()
    
    for scenario in scenarios:
        filename = f"{scenarios_dir}/{scenario['name']}.json"
        with open(filename, 'w') as f:
            json.dump(scenario, f, indent=2)
        print(f"Saved scenario: {filename}")


def load_scenario_from_file(filepath: str) -> Dict[str, Any]:
    """Load a scenario from a JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)


def create_custom_scenario(name: str, problem_type: str, goal: str, 
                          constraints: List[Dict[str, str]], 
                          requirements: List[str]) -> Dict[str, Any]:
    """Create a custom test scenario."""
    return {
        'name': name,
        'problem': {
            'type': problem_type,
            'goal': goal,
            'description': f'Custom scenario: {goal}',
            'constraints': constraints,
            'requirements': requirements
        }
    }


if __name__ == "__main__":
    # Save all scenarios to files when run directly
    save_scenarios_to_files()
    
    # Print summary of available scenarios
    scenarios = get_all_test_scenarios()
    print(f"\nAvailable Test Scenarios ({len(scenarios)}):")
    print("=" * 40)
    
    for scenario in scenarios:
        problem = scenario['problem']
        print(f"Name: {scenario['name']}")
        print(f"Type: {problem['type']}")
        print(f"Goal: {problem['goal']}")
        print(f"Constraints: {len(problem['constraints'])}")
        print(f"Requirements: {len(problem['requirements'])}")
        print("-" * 40)

