"""A module to compute rollup scores."""

from abc import ABC, abstractmethod

from scorch.models import ScoreLevel, ScoringItemResponse

class ScoreLevelComputer(ABC):
    """ScoreLeveler computes the ScoreLevel for a ScoreItemResponse."""

    @abstractmethod
    def score_level(self, sir: ScoringItemResponse) -> ScoreLevel:
        """Return the direct or computed score level."""


class ThreshholdScoreLevelComputer(ScoreLevelComputer):

    def score_level(self, sir: ScoringItemResponse) -> ScoreLevel:
        if sir.score_item_version.score_item.level.is_last():
            return sir.score_level
        level = None
        scorecard = sir.response.scorecard_version.scorecard
        for level in sorted(scorecard.score_levels(), key=lambda x: x.order):
            if sir.score >= level.threshhold():
                break
        return level


    # def eval_float(item: 'ScoreItem', expr: str, default: float=0) -> float:
    #     res = default
    #     # TODO: this is where the expression evaluator goes
    #     return res

    # def eval_bool(item: 'ScoreItem', expr: str, default: bool=False) -> bool:
    #     res = default
    #     # TODO: this is where the expression evaluator goes
    #     return res

    # def get_owner(self) -> str:
    #     """Return the nearest explicitly set owner."""
    #     owner = self.owner
    #     if owner is None and self.parent is not None:
    #         owner = self.parent.get_owner()
    #     return owner

    # def get_label(self) -> str:
    #     label = None
    #     if self.scorecard_version is not None:
    #         label = self.scorecard_version.label
    #     elif self.parent is not None:
    #         label = self.parent.get_label()
    #     return label

class EvalWeighter():
    def get_weight(self) -> float:
        weight = self.weight
        if weight is None:
            weight = ScoreItem.eval_float(self, self.weight_expr)
            if weight is None:
                if self.parent is not None:
                    weight = self.parent.get_weight()
                elif self.scorecard_version is not None:
                    weight = self.scorecard_version.scorecard.default_weight
        return weight

    def get_mandatory(self) -> bool:
        mandatory = self.mandatory
        if mandatory is None:
            mandatory = self.eval_bool(self, self.mandatory_expr)
            if mandatory is None:
                if self.parent is not None:
                    mandatory = self.parent.get_mandatory()
                elif self.scorecard_version is not None:
                    mandatory = (
                        self.scorecard_version.scorecard.default_mandatory)
        return mandatory


class Scorer(ABC):
    """A class representing a scoring strategy."""

    def __init__(self, max_score: float) -> None:
        self.max_score = max_score

    @abstractmethod
    def score(self, resp: ScoringItemResponse) -> float:
        """Return the score for this Scoarable."""



class DeductionScorer(Scorer):
    """A Scorer that uses a deduction method for computing scores.

    Requires a maximum score. Raw scores are subtracted from the
    maximum score to calculate a deduction. Deductions are summed
    using their weights to computed a weighted average deduction for
    the parent. That deduction is passed upward to parents to compute their
    score, which in turn becomes their deduction.
    """

    def score(self, item: ScoringItemResponse) -> float:
        score = item.get_direct_score()
        if score is not None:
            return score

        score = 0.
        deduction = 0.
        weights = 0.
        for child in item.get_children():
            child_score = self.score(child)
            child_weight = child.get_weight()
            deduction += (self.max_score - child_score) * child_weight
            weights += child_weight
        if weights > 0:
            score = max(0, (self.max_score - deduction) / weights)
        return score
