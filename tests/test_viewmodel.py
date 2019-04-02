import unittest

from gapsule.utils.viewmodels import ViewModelDict, ViewModelField, ViewModelList


class ViewModelTestCase(unittest.TestCase):
    def test_required_and_not_nullable1(self):
        class _class1(ViewModelDict):
            field1 = ViewModelField('field1', required=True, nullable=False)

        with self.assertRaises(ValueError):
            d1 = _class1()
            d1['field1'] = "NotNone"

        d2 = _class1(field1='NotNone')
        with self.assertRaises(AttributeError):
            d2.field1 = None

        with self.assertRaises(AttributeError):
            del d2.field1

    def test_required_and_not_nullable2(self):
        class _class2(ViewModelDict):
            field1 = ViewModelField(
                'field1', required=True, nullable=False, default="NonNone")

        d2 = _class2()
        self.assertIs(d2.field1, d2['field1'])
        self.assertEqual(d2.field1, 'NonNone')

    def test_default1(self):
        class _class3(ViewModelDict):
            field1 = ViewModelField('field1', required=True, nullable=False)

            @field1.default
            def field1(self):
                return "NonNone"

        d3 = _class3()
        self.assertIs(d3.field1, d3['field1'])
        self.assertEqual(d3.field1, "NonNone")

    def test_default_name1(self):
        class _class4(ViewModelDict):
            field1 = ViewModelField(required=True, default=5)

        d4 = _class4()
        self.assertEqual(d4.field1, 5)

    def test_default_name2(self):
        class _class4(ViewModelDict):
            field1 = ViewModelField(
                required=True, default=lambda: "not classmethod")

        d4 = _class4()
        self.assertEqual(d4.field1, "not classmethod")

    def test_readonly1(self):
        class _class5(ViewModelDict):
            field1 = ViewModelField(readonly=True)

        d5 = _class5(field1=6)
        with self.assertRaises(AttributeError):
            d5.field1 = 3
        self.assertEqual(d5.field1, 6)

    def test_validation1(self):
        class _class4(ViewModelDict):
            field1 = ViewModelField(
                required=True, validation=lambda x: x > 0)

        d4 = _class4(field1=2)
        self.assertEqual(d4.field1, 2)
        d4.field1 = 1
        self.assertEqual(d4.field1, 1)
        with self.assertRaises(AssertionError):
            d4.field1 = 0

    def test_validation2(self):
        class _class4(ViewModelDict):
            field1 = ViewModelField(required=True)

            @field1.validation
            def field1(self, x):
                return x > 0

        d4 = _class4(field1=2)
        self.assertEqual(d4.field1, 2)
        d4.field1 = 1
        self.assertEqual(d4.field1, 1)
        with self.assertRaises(AssertionError):
            d4.field1 = 0

    def test_isdict(self):
        self.assertTrue(issubclass(ViewModelDict, dict))


class ViewModelListTestCase(unittest.TestCase):
    def test_islist(self):
        self.assertTrue(issubclass(ViewModelList, list))
