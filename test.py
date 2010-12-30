

import backup
import unittest
import os.path


class TestPackager(unittest.TestCase):

	def setUp(self):
		self.packer = backup.Packager()

	def test_expand_file_list(self):
		includes = [
			(os.path.abspath('./test/first'), '\d+', set(('4', '5'))),
			(os.path.abspath('./test/second'),),
			(os.path.abspath('./test/third'), '\w{2}'),
		]

		exp = self.packer.expand_file_list(includes)
		self.assertEquals(7, len(exp), exp)
		

	


if __name__ == "__main__":
	unittest.main()

