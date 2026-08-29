"""
Chapter 10: Formal Invariant Verification using Microsoft Z3 SMT Solver
Demonstrates mathematical proof of Conservation of Mass and Balance Non-Negativity.
"""
import pytest

try:
    from z3 import Solver, Real, And, Not, unsat
    Z3_AVAILABLE = True
except ImportError:
    Z3_AVAILABLE = False


@pytest.mark.skipif(not Z3_AVAILABLE, reason="z3-solver package not installed")
def test_prove_ledger_conservation_and_non_negativity():
    """
    Formally prove that under valid guard conditions, transfer logic cannot violate
    the Conservation of Mass invariant or create negative balances.
    """
    # Symbolic variables
    balance_a_initial = Real('balance_a_initial')
    balance_b_initial = Real('balance_b_initial')
    transfer_amount = Real('transfer_amount')
    
    balance_a_final = Real('balance_a_final')
    balance_b_final = Real('balance_b_final')
    
    s = Solver()
    
    # Preconditions
    s.add(balance_a_initial >= 0)
    s.add(balance_b_initial >= 0)
    s.add(transfer_amount > 0)
    
    # AI-Generated Guard Condition
    transfer_guard = (balance_a_initial >= transfer_amount)
    
    # State Transition Equations
    s.add(balance_a_final == balance_a_initial - transfer_amount)
    s.add(balance_b_final == balance_b_initial + transfer_amount)
    
    # Invariants
    conservation_holds = (balance_a_initial + balance_b_initial == balance_a_final + balance_b_final)
    non_negative_holds = (balance_a_final >= 0)
    
    # Search for any counterexample where guard succeeds but invariant fails
    s.add(transfer_guard)
    s.add(Not(And(conservation_holds, non_negative_holds)))
    
    # unsat means NO counterexample exists -> theorem mathematically proven!
    assert s.check() == unsat
