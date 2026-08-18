from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from data.classes import Skill


@dataclass
class SkillCooldowns:
    _data: dict[str, int] = field(default_factory=dict)

    @classmethod
    def from_skills(cls, skills: "tuple[Skill, ...]") -> "SkillCooldowns":
        return cls(_data={skill.name: 0 for skill in skills})

    @classmethod
    def from_dict(cls, data: dict[str, int]) -> "SkillCooldowns":
        return cls(_data=dict(data))

    def is_ready(self, name: str) -> bool:
        return self._data.get(name, 0) == 0

    def tick(self) -> "SkillCooldowns":
        return SkillCooldowns(_data={k: max(0, v - 1) for k, v in self._data.items()})

    def set_cooldown(self, name: str, turns: int) -> "SkillCooldowns":
        return SkillCooldowns(_data={**self._data, name: turns})

    def active(self) -> dict[str, int]:
        return {k: v for k, v in self._data.items() if v > 0}

    def as_dict(self) -> dict[str, int]:
        return dict(self._data)
