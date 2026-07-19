# Multi-Module HTML Guide Architecture

## High Cohesion, Low Coupling Principles

### Module Design Rules
- **High cohesion**: Each HTML file covers ONE topic completely. Don't split "what is X" and "how to solve X" into separate files — they're the same topic.
- **Low coupling**: Files don't duplicate content. Cross-reference via links instead.
- **Self-contained nav**: Every file has the full nav sidebar so it can be read independently.
- **Balanced size**: Aim for 10-20K text chars per module. If one module is 34K and others are 10K, consider splitting — but only if the halves are genuinely independent topics.

### Anti-pattern: Over-splitting
- BAD: "NP Problems" + "NP Solving Strategies" as separate files — these are the same topic. Merge them.
- BAD: "Theory" + "Applications" as separate files — applications ARE the theory made concrete.
- GOOD: Split by orthogonal dimensions — e.g., LP/IP (continuous+discrete) vs Graph/Network (structure-based) vs Heuristics (method-based).

### User Preference: Problem-Scene Classification
User wants content organized by **problem scenarios** (what problem am I facing?) not just by method (what algorithm exists?). Always include a "scenario lookup" module that maps real-world problems → recommended methods, with "identification signals" (keywords that indicate each problem type).

### File Renumbering Pitfall
When renaming files (e.g., 07→09), **always rename to temp names first**:
```python
os.rename("07-X.html", "tmp-X.html")  # first
os.rename("tmp-X.html", "09-X.html")  # then
```
Direct rename `07→09` while `09` exists = silent overwrite.

### Post-generation Verification Checklist
1. **Link integrity**: `grep -oP 'href="\K[^"#]+\.html' file | while read l; do [ ! -f "$l" ] && echo BROKEN; done`
2. **Section numbering**: `grep '<h2' file` — verify sequential after patches
3. **Nav consistency**: All files should have identical nav sidebars
4. **Cross-reference audit**: Every module mentioning a topic should link to the module covering it
5. **Content density**: Compare text chars across modules — no module should be 3x thinner

### Generation Pattern (Python Script)
For guides with 8+ modules, generate via a single Python script:
```python
CSS = r"""..."""   # Shared CSS template
NAV = r"""..."""   # Shared nav sidebar template
def wrap(title, body):
    return f"<!DOCTYPE html>...{CSS}...{NAV}...{body}..."

# Generate each file
for module in modules:
    with open(f"{OUT}/{module.filename}", "w") as f:
        f.write(wrap(module.title, module.body))
```
Benefits: consistent styling, single point of change for CSS/nav, easy verification.

### Enrichment Strategy
When user says "详尽" (thorough):
1. Check content density — find the thinnest module
2. Add detailed walkthroughs (step-by-step algorithm execution)
3. Add code examples (not just pseudocode)
4. Add numerical hand-calculations
5. Add "why" explanations (not just "what")

### Cross-Reference Audit Command
```bash
for f in *.html; do
  refs=$(grep -oP 'href="\K[^"#]+\.html' "$f" | sort -u)
  for link in $refs; do
    [ ! -f "$link" ] && echo "BROKEN: $f -> $link"
  done
done
```
