import pytest
from mergen.domain import Execution, ExecutionState, InvalidTransition

def test_execution_transitions_are_explicit():
    execution = Execution.create("project", "item")
    assert execution.transition(ExecutionState.VALIDATING).state is ExecutionState.VALIDATING
    with pytest.raises(InvalidTransition): execution.transition(ExecutionState.COMPLETED)
