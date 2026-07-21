import unittest

from card.audit_animal_skills import audit_all, audit_animal, han_count


class AuditAnimalSkillsTest(unittest.TestCase):
    def test_han_count_ignores_punctuation(self):
        self.assertEqual(han_count("咬住目標，立刻轉身！"), 8)

    def test_valid_row_has_no_format_issue(self):
        row = audit_animal(
            {
                "id": "test",
                "name": "測試動物",
                "skillName": "巧手取食",
                "skillDesc": "用細長樹枝探進小洞，找出藏在裡面的食物。",
                "skillBonus": [{"attr": 4, "val": 2}, {"attr": 0, "val": 2}],
            }
        )
        self.assertEqual(row.format_issues, ())

    def test_same_skill_name_is_reported_for_both_rows(self):
        animals = [
            {
                "id": "a",
                "name": "甲",
                "skillName": "巧手取食",
                "skillDesc": "用細長樹枝探進小洞，找出藏在裡面的食物。",
                "skillBonus": [{"attr": 4, "val": 4}],
            },
            {
                "id": "b",
                "name": "乙",
                "skillName": "巧手取食",
                "skillDesc": "用細長樹枝探進小洞，找出藏在裡面的食物。",
                "skillBonus": [{"attr": 4, "val": 4}],
            },
        ]
        rows = audit_all(animals)
        self.assertTrue(all("duplicate_skill_name" in row.format_issues for row in rows))

    def test_prompt_risk_terms_are_candidates(self):
        row = audit_animal(
            {
                "id": "test",
                "name": "測試動物",
                "skillName": "伏地突襲",
                "skillDesc": "躲在暗處等待獵物，然後突然撲出一擊必殺。",
                "skillBonus": [{"attr": 2, "val": 4}],
            }
        )
        self.assertIn("external_actor", row.prompt_risk_flags)
        self.assertIn("violent_visual", row.prompt_risk_flags)
        self.assertIn("absolute_or_hyperbolic", row.prompt_risk_flags)


if __name__ == "__main__":
    unittest.main()
