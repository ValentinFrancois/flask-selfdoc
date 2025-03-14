import os
import sys
import unittest

from examples.custom.blog import app as custom_app
from examples.simple.blog import app as simple_app

from tests.config import IS_WINDOWS
from tests.config import NEW_FN_OFFSETS

# To regenerate the baseline data files, change this to True.
REGENERATE_FILES = False


class TestApp(object):
    maxDiff = None

    def setUp(self):
        self.client = self.app.test_client()

    def get_request(self):
        r = self.client.get(self.path)
        self.assertEqual(r.status_code, 200)
        data = r.data.decode('utf-8')
        return data

    def sub_pwd(self, data):
        file_path = os.getcwd()
        return data.replace(file_path, "%PATH%")        

    @unittest.skipIf(REGENERATE_FILES, "Regenerating the baseline files")
    @unittest.skipIf(not NEW_FN_OFFSETS, "This test will not work with the old way of detecting fn line numbers")
    @unittest.skipIf(IS_WINDOWS, "This test will not work with Windows style filepaths")
    def test_output(self):
        data = self.get_request()
        with open(self.filename) as f:
            expected = f.read()

        data = self.sub_pwd(data)
        self.assertEqual(data, expected)

    @unittest.skipIf(not REGENERATE_FILES, "This is only run to regenerate the baseline.")
    def test_regenerate(self):
        data = self.get_request()
        data = self.sub_pwd(data)
        with open(self.filename, "w") as f:
            f.write(data)
        self.assertTrue(False, "This test always fails, change REGENERATE_FILES back to False to proceed.")


class TestSimpleApp(TestApp, unittest.TestCase):
    app = simple_app
    filename = "tests/files/simple.html"
    path = "/doc"


class TestSimpleAppJSONOutput(TestApp, unittest.TestCase):
    app = simple_app
    filename = "tests/files/simple.json"
    path = "/doc/json"


class TestSimpleAppBuiltinJSONOutput(TestApp, unittest.TestCase):
    app = simple_app
    filename = "tests/files/builtin.json"
    path = "/doc/builtin_json"


class TestSimpleAppPrivateGroup(TestApp, unittest.TestCase):
    app = simple_app
    filename = "tests/files/simple_private.html"
    path = "/doc/private"


class TestFactoryApp(TestApp, unittest.TestCase):
    filename = "tests/files/factory.html"
    path = "/doc/"

    @classmethod
    def setUpClass(cls):
        sys.path.append('examples/factory')
        from app import create_app as factory_create_app
        cls.app = factory_create_app()


class TestCustomApp(TestApp, unittest.TestCase):
    app = custom_app
    filename = "tests/files/custom.html"
    path = "/doc/"


class TestCustomAppJSONOutput(TestApp, unittest.TestCase):
    app = custom_app
    filename = "tests/files/custom.json"
    path = "/doc/json"


if __name__ == "__main__":
    unittest.main()
