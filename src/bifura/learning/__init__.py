"""Incident-driven learning: dataset, features, training, prediction, retrieval.

Four separate things (spec §6.1):
- incident storage  -> incident_store.py
- incident retrieval -> retrieve.py (similarity; not training)
- model training     -> dataset.py + train.py (scikit-learn, local)
- LLM investigation  -> bifura.agent (uses predictions as hypotheses only)
"""
