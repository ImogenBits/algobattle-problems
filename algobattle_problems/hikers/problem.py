"""The Hikers problem class."""
from typing import ClassVar
from pydantic import Field

from algobattle.problem import ProblemModel, SolutionModel, ValidationError


class Hikers(ProblemModel):
    """The Tsptimewindows problem class."""

    name: ClassVar[str] = "Hikers"
    min_size: ClassVar[int] = 5

    hikers: list[tuple[int, int]] = Field(ge=0)

    @property
    def size(self) -> int:
        """The instance size is the number of hikers."""
        return len(self.hikers)

    def validate_instance(self) -> None:
        if any(min_size > max_size for min_size, max_size in self.hikers):
            raise ValidationError("One hiker's minimum group size is larger than their maximum group size.")

    class Solution(SolutionModel):
        """A solution to a Hikers problem."""

        direction: ClassVar = "maximize"

        assignments: dict[int, int] = Field(ge=0)

        def validate_solution(self, instance: "Hikers") -> None:
            if any(hiker > len(instance.hikers) for hiker in self.assignments):
                raise ValidationError("Solution contains hiker that is not in the instance.")

            group_sizes = {}
            for group in self.assignments.items():
                group_sizes[group] = group_sizes.get(group, 0) + 1

            for hiker, group in self.assignments.items():
                min_size, max_size = instance.hikers[hiker]
                if not (min_size <= group_sizes[group] <= max_size):
                    raise ValidationError("A Hiker is not happy with their assignment!")

        def score(self, size: int, instance: "Hikers") -> float:
            return len(self.assignments)
