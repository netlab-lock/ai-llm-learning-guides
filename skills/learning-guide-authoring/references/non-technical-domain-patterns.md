# Non-Technical Domain Adaptation Patterns

When using the learning-guide-authoring skill for non-technical topics (finance, law, health, career, etc.), adapt the content structure away from formulas/code/benchmarks toward practical decision frameworks.

## Content Pattern Differences

| Aspect | Technical Guide | Non-Technical/Practical Guide |
|--------|----------------|------------------------------|
| Core content | Architecture, formulas, code | Decision trees, comparison tables, risk ratings |
| Diagrams | System architecture, data flow | Allocation pyramids, process flows, lifecycle stages |
| "Code blocks" | Actual code snippets | Step-by-step action sequences, checklist templates |
| "Benchmarks" | Performance metrics, scores | Product comparisons, fee tables, historical returns |
| Exercises | Implementation tasks | Scenario analysis, personal audits, plan design |
| Citations | arXiv papers, GitHub repos | Regulatory sources, market data, official rates |

## Structural Adaptations for Practical Domains

### 1. Product/Tool Comparison Tables
Every module should have at least one comparison table of real products/tools relevant to the domain. Users want actionable recommendations, not just theory.

### 2. Risk/Warning Sections
Non-technical domains (finance, health, legal) need prominent "防坑" (pitfall avoidance) sections. Use `warn` boxes for regulatory/compliance warnings and scam alerts.

### 3. Lifecycle/Stage Frameworks
Practical domains often organize by life stage (age, career phase, family status) rather than by technical depth. Include a lifecycle table showing how priorities shift.

### 4. Quantitative References with Context
Numbers need context: "3% interest rate" means nothing without comparison to inflation, alternatives, and historical range. Always provide a reference frame.

### 5. Action-Oriented Module Endings
Technical guides end with "understand this concept." Practical guides end with "do this today." The final module should have a concrete "first 3 steps" action plan.

## Phase Structure for Practical Guides

```
Phase 1: Foundations (understand the landscape)
  - Core concepts, terminology, mental models
  - Personal assessment tools (budget, risk tolerance)

Phase 2: Tools/Instruments (know your options)  
  - Individual product/instrument deep-dives
  - Comparison tables, fee analysis, selection criteria

Phase 3: Strategy/Frameworks (build your system)
  - Portfolio/allocation theory
  - Behavioral psychology for the domain
  - Tax/legal optimization

Phase 4: Execution (put it all together)
  - Platform/tool recommendations
  - Scenario-based plans (by age, income, risk level)
  - Maintenance schedules (rebalance, review, update)
```

## Module Sizing

Non-technical modules tend to be slightly smaller (8-12KB) than technical ones (12-20KB) because they have less code/formula content. This is fine — density of actionable advice matters more than raw size.

## Domain-Specific Considerations

### Personal Finance (理财)
- Include current market rates (search-verify, not training data)
- Regulatory information varies by jurisdiction (China-specific: 存款保险, LPR, 个人养老金)
- Product codes (fund codes, stock codes) are highly actionable
- Include fee calculation examples (real cost of credit card installment, fund management fees)

### Legal/Compliance
- Always include jurisdiction disclaimers
- Cite specific regulations and articles
- Distinguish "common practice" from "legal requirement"

### Health/Wellness
- Include "consult a professional" disclaimers
- Focus on evidence-based recommendations
- Avoid prescriptive medical advice
