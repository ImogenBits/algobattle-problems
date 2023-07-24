"""The Scheduling problem class."""
from typing import Annotated

from algobattle.problem import Problem, InstanceModel, SolutionModel, Scored, minimize
from algobattle.types import Interval, SizeLen


Timespan = Annotated[int, Interval(ge=0, le=(2**64 - 1) / 5)]
Machine = Annotated[int, Interval(ge=1, le=5)]


class Instance(InstanceModel):
    """The Scheduling problem class."""

    job_lengths: list[Timespan]

    @property
    def size(self) -> int:
        return len(self.job_lengths)


class Solution(SolutionModel[Instance], Scored[Instance]):
    """A solution to a Job Shop Scheduling problem."""

    assignments: SizeLen[list[Machine]]

    @minimize
    def score(self, instance: Instance) -> float:
        finish_time = [0] * 5
        for duration, machine in zip(instance.job_lengths, self.assignments):
            finish_time[machine - 1] += duration * machine
        return max(finish_time)


Scheduling = Problem(
    name="Job Shop Scheduling",
    min_size=5,
    instance_cls=Instance,
    solution_cls=Solution,
)
