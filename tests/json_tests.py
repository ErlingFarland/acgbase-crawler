import unittest
from dataclasses import dataclass
from typing import List, Optional

from lib.data.convert import class_to_json, json_to_class
from lib.data.indices import GenderInfo


@dataclass
class TestDataA:
    value: int

@dataclass
class TestDataB:
    a: TestDataA
    optional: Optional[TestDataA]
    enum: GenderInfo
    a_list: List[TestDataA]


test_data = TestDataB(
    a=TestDataA(1),
    optional=None,
    enum=GenderInfo.Male,
    a_list=[
        TestDataA(2), TestDataA(3), TestDataA(4),
    ]
)

class MyTestCase(unittest.TestCase):
    def test_something(self):
        print(test_data)
        j = class_to_json(test_data)
        print(j)
        d = json_to_class(j, TestDataB)
        print(d)
        j2 = class_to_json(d)
        self.assertEqual(j, j2)


if __name__ == '__main__':
    unittest.main()
