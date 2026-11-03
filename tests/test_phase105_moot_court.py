"""
Unit tests for Phase 105: Multi-Agent Adversarial Moot Court Case Simulator.
"""
import pytest
from legalmitra.simulation.moot_court_engine import moot_court_simulator

def test_moot_court_simulation_cheating():
    facts = "Complainant paid Rs 5,00,000 for supply of goods which were never delivered."
    result = moot_court_simulator.simulate(facts, "Criminal Breach & Cheating")
    
    assert "Section 318(4)" in result.petitioner_submission.primary_statutory_basis
    assert len(result.petitioner_submission.precedents_relied_on) > 0
    assert "Section 250" in result.defence_rebuttal.primary_statutory_basis
    assert len(result.defence_rebuttal.counter_arguments) > 0
    assert "Bench" in result.bench_ruling.bench_name
    assert "likelihood" in result.bench_ruling.probable_verdict_likelihood.lower()
    assert len(result.bench_ruling.suggested_evidentiary_steps) > 0

def test_moot_court_simulation_cheque_bounce():
    facts = "Cheque of Rs 2,50,000 dishonoured with remarks funds insufficient."
    result = moot_court_simulator.simulate(facts, "Cheque Dishonour 138 NI Act")
    
    assert "138" in result.petitioner_submission.primary_statutory_basis
    assert "Basalingappa" in result.defence_rebuttal.precedents_relied_on[0]
    assert "conviction" in result.bench_ruling.probable_verdict_likelihood.lower()
