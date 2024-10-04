from typing import Awaitable, Callable
from beartype import beartype
from temporalio import activity

from ...autogen.openapi_model import CreateTransitionRequest, Transition
from ...common.protocol.tasks import StepContext
from ...env import testing
from ...models.execution.create_execution_transition import create_execution_transition


@beartype
async def transition_step(
    context: StepContext,
    transition_info: CreateTransitionRequest,
) -> Transition:
    # Create transition
    transition = create_execution_transition(
        developer_id=context.execution_input.developer_id,
        execution_id=context.execution_input.execution.id,
        task_id=context.execution_input.task.id,
        data=transition_info,
        task_token=transition_info.task_token,
        update_execution_status=True,
    )
    return transition


original_transition_step = transition_step
mock_transition_step = transition_step

transition_step: Callable[[StepContext], Awaitable[Transition]] = activity.defn(
    name="transition_step"
)(transition_step if not testing else mock_transition_step)
