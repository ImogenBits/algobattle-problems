"""The OSCM3 problem class."""
from typing import ClassVar
from pydantic import Field

from algobattle.problem import ProblemModel, SolutionModel, ValidationError, Scored


class OSCM3(ProblemModel):
    """The OSCM3 problem class."""

    name: ClassVar[str] = "One-Sided Crossing Minimization-3"
    min_size: ClassVar[int] = 1

    size: int = Field(ge=0)
    neighbors: dict[int, set[int]] = Field(ge=0)

    def validate_instance(self, max_size: int) -> None:
        super().validate_instance(max_size)
        if self.size > max_size:
            raise ValidationError("Instance contains too many vertices.")
        if any(not 0 <= v < self.size for v in self.neighbors):
            raise ValidationError("Instance contains element of V_1 out of the permitted range.")
        if any(not 0 <= v < self.size for neighbors in self.neighbors.values() for v in neighbors):
            raise ValidationError("Instance contains element of V_2 out of the permitted range.")
        if any(len(neighbors) > 3 for neighbors in self.neighbors.values()):
            raise ValidationError("A vertex of V_1 has more than 3 neighbors.")
        for u in range(self.size):
            self.neighbors.setdefault(u, set())

    class Solution(SolutionModel, Scored):
        """A solution to a One-Sided Crossing Minimization-3 problem"""

        direction: ClassVar = "minimize"

        vertex_order: list[int] = Field(ge=0)

        def validate_solution(self, instance: "OSCM3") -> None:
            if any(not 0 <= i < instance.size for i in self.vertex_order):
                raise ValidationError("An element of the solution is not in the permitted range.")
            if len(self.vertex_order) != len(set(self.vertex_order)):
                raise ValidationError("The solution contains duplicate numbers.")
            if len(self.vertex_order) != instance.size:
                raise ValidationError("The solution does not order the whole instance.")

        def score(self, instance: "OSCM3") -> float:
            score = 0
            for position, vertex in enumerate(self.vertex_order):
                for i in instance.neighbors[vertex]:
                    score += sum(j < i for other in self.vertex_order[position:] for j in instance.neighbors[other])
            return score
