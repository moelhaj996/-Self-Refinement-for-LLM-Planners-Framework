# Self-Refinement for LLM Planners Framework

## Framework Overview

```mermaid
graph TD
    A[Input Problem] --> B[Generate Initial Plan]
    B --> C[Self-Check Plan]
    C --> D{Quality OK?}
    D -->|Yes| E[Final Plan]
    D -->|No| F[Refine Plan]
    F --> C
```