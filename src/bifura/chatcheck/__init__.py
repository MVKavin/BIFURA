"""Chat check: ask an AI (Gemini, GPT or Claude) a numerical question, then let Bifura
recalculate every step with SymPy, find the first wrong step, ask the AI to correct
itself, and verify the correction.

Scope (honest): Bifura proves calculation mistakes exactly. It does not prove that a
chosen formula is the right physics; give an expected answer to check the final result.
"""
