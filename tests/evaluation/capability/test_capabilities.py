from __future__ import annotations

import re

import pytest

from src.opencode.evaluation.capability.capabilities import Capability


class TestCapabilityMembers:
    def test_defines_all_twenty_capabilities(self) -> None:
        assert tuple(Capability) == (
            Capability.PYTHON,
            Capability.SQL,
            Capability.ORACLE_SQL,
            Capability.POSTGRES_SQL,
            Capability.ARCHITECTURE,
            Capability.CODE_REVIEW,
            Capability.DEBUGGING,
            Capability.TESTING,
            Capability.REFACTORING,
            Capability.PLANNING,
            Capability.REASONING,
            Capability.PROMPT_ENGINEERING,
            Capability.TOOL_USE,
            Capability.FUNCTION_CALLING,
            Capability.MULTIMODAL,
            Capability.MATH,
            Capability.WRITING,
            Capability.DOCUMENTATION,
            Capability.SUMMARIZATION,
            Capability.TRANSLATION,
        )

    @pytest.mark.parametrize("capability", tuple(Capability))
    def test_from_string_returns_matching_member(self, capability: Capability) -> None:
        assert Capability.from_string(capability.value) is capability

    def test_from_string_rejects_unknown_value(self) -> None:
        with pytest.raises(ValueError, match="Unknown capability"):
            Capability.from_string("unknown_capability")

    def test_from_string_error_lists_valid_options(self) -> None:
        with pytest.raises(ValueError) as error:
            Capability.from_string("unknown_capability")

        message = str(error.value)
        assert all(capability.value in message for capability in Capability)

    def test_enum_values_are_unique(self) -> None:
        values = tuple(capability.value for capability in Capability)

        assert len(values) == len(set(values))

    def test_enum_values_are_lowercase_snake_case(self) -> None:
        pattern = re.compile(r"[a-z]+(?:_[a-z]+)*")

        assert all(pattern.fullmatch(capability.value) for capability in Capability)


class TestCapabilityCategories:
    def test_programming_languages_returns_all_four_language_capabilities(self) -> None:
        assert Capability.programming_languages() == (
            Capability.PYTHON,
            Capability.SQL,
            Capability.ORACLE_SQL,
            Capability.POSTGRES_SQL,
        )

    def test_software_engineering_returns_all_seven_engineering_capabilities(self) -> None:
        assert Capability.software_engineering() == (
            Capability.ARCHITECTURE,
            Capability.CODE_REVIEW,
            Capability.DEBUGGING,
            Capability.TESTING,
            Capability.REFACTORING,
            Capability.PLANNING,
            Capability.REASONING,
        )

    def test_ai_specific_returns_all_four_ai_capabilities(self) -> None:
        assert Capability.ai_specific() == (
            Capability.PROMPT_ENGINEERING,
            Capability.TOOL_USE,
            Capability.FUNCTION_CALLING,
            Capability.MULTIMODAL,
        )

    def test_general_returns_all_five_general_capabilities(self) -> None:
        assert Capability.general() == (
            Capability.MATH,
            Capability.WRITING,
            Capability.DOCUMENTATION,
            Capability.SUMMARIZATION,
            Capability.TRANSLATION,
        )

    def test_category_helpers_are_disjoint(self) -> None:
        categories = (
            set(Capability.programming_languages()),
            set(Capability.software_engineering()),
            set(Capability.ai_specific()),
            set(Capability.general()),
        )

        assert all(
            category.isdisjoint(other)
            for index, category in enumerate(categories)
            for other in categories[index + 1 :]
        )
