import unittest

from lib.data.convert import class_to_json, json_to_class
from lib.data.result import character


class MyTestCase(unittest.TestCase):
    def test_something(self):
        info = character.RCharacter('测试')
        info.outlook.body.age_range = character.AgeRange(min=12, max=30)
        json1 = class_to_json(info)
        info2 = json_to_class(json1, character.RCharacter)
        self.assertEqual(info, info2)
        print(info)


if __name__ == '__main__':
    unittest.main()
