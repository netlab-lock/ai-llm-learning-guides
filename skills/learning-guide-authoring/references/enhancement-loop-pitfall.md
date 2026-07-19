# Enhancement Loop Anti-Pattern

**Discovered**: 2026-05-27 during P1 learning guide enhancement session

## The Problem

When the user asks to "check and enhance" or "enrich" existing learning guides, the agent can get stuck in an infinite loop:

1. Audit files → find 13 files under 12KB
2. Rewrite file 1 → still 7-8KB (content was already substantive)
3. Check progress → still 13 files thin
4. Rewrite file 2 → still 7-8KB
5. Repeat for 20+ turns with no meaningful progress

The user keeps sending the same goal prompt because nothing is actually improving.

## Root Cause

- Files with 7-10KB of good content (ASCII diagrams, formulas, tables, exercises) don't grow to 12KB by rewording
- The 12KB target in the skill is aspirational, not a hard requirement
- Rewriting the same content with different wording produces similar size
- The agent confuses "activity" with "progress"

## The Fix

1. **Define "done" clearly**: If all files have 8-dimension framework content + ASCII diagrams + formulas + comparison tables + exercises, the guide IS complete regardless of file size
2. **Enhancement = NEW content only**: Adding the latest 2025-2026 research, foundational knowledge the user lacks, or missing diagrams. NOT rewording existing content.
3. **Stop after 2-3 attempts**: If rewriting a file doesn't significantly increase size/quality after 2 attempts, the file is at its natural depth
4. **Audit before enhancing**: Check what's actually missing (foundational knowledge? latest tech? diagrams?) rather than blindly rewriting everything
5. **7-10KB with good content is acceptable**: The 12KB target is for initial creation, not for enhancement passes

## Session Stats

- P1 guides: 38 files, 451KB total
- Enhancement attempts: 20+ turns rewriting the same 13 files
- Net progress: ~0 (files stayed at similar sizes)
- Lesson: Stop rewriting, declare done when content is substantive
