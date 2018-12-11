import unittest
import os.path

from alpha2heb.main import entrypoint

class Tests(unittest.TestCase):
    def test1(self):
        res = entrypoint((os.path.join("tests", "config1.ini"),
                          os.path.join("tests", "symbols1.txt"),
                          "“mlḵ”",
                          "console",))
        self.assertEqual(res, "כלמ")