from datetime import date
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, model_validator


Slug = str


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class CardDefinition(StrictModel):
    schema_version: Literal[1]
    id: Slug = Field(pattern=r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
    issuer: str = Field(min_length=1)
    name: str = Field(min_length=1)
    networks: list[Literal["amex", "diners", "mastercard", "rupay", "visa"]] = Field(
        min_length=1
    )
    parser: Slug = Field(pattern=r"^[a-z0-9]+(?:_[a-z0-9]+)*$")


class RuleSource(StrictModel):
    title: str = Field(min_length=1)
    url: HttpUrl
    accessed_on: date


class RewardDefinition(StrictModel):
    kind: Literal["cashback", "fee_waiver", "membership", "points", "voucher"]
    description: str = Field(min_length=1)
    estimated_value: Decimal | None = Field(default=None, ge=0)
    expected_within_days: int | None = Field(default=None, ge=0)


class BenefitDefinition(StrictModel):
    id: Slug = Field(pattern=r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
    kind: Literal["accelerated_reward", "cashback", "milestone", "waiver"]
    name: str = Field(min_length=1)
    period: Literal["billing_cycle", "calendar_month", "calendar_quarter", "card_year"]
    threshold: Decimal | None = Field(default=None, gt=0)
    reward: RewardDefinition
    exclusions: list[Slug] = Field(default_factory=list)

    @model_validator(mode="after")
    def milestone_requires_threshold(self):
        if self.kind in {"milestone", "waiver"} and self.threshold is None:
            raise ValueError(f"{self.kind} benefits require a threshold")
        return self


class RuleSet(StrictModel):
    schema_version: Literal[1]
    version: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    effective_from: date
    effective_to: date | None = None
    sources: list[RuleSource] = Field(min_length=1)
    benefits: list[BenefitDefinition] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_rule_set(self):
        if self.effective_to and self.effective_to < self.effective_from:
            raise ValueError("effective_to cannot be before effective_from")

        benefit_ids = [benefit.id for benefit in self.benefits]
        if len(benefit_ids) != len(set(benefit_ids)):
            raise ValueError("benefit IDs must be unique within a rule version")

        if self.version != self.effective_from.isoformat():
            raise ValueError("rule version must match effective_from")
        return self
