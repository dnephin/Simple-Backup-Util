

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
			(os.path.abspath('./test/bogus'),),
			(os.path.abspath('./test/third'), '\w{2}'),
			(os.path.abspath('./test/forth/file'),),
		]

		exp = self.packer.expand_file_list(includes)
		self.assertEquals(8, len(exp), exp)
		

	def test_build_tarfile(self):
		fl = [os.path.abspath('./test/second/a'), os.path.abspath('./test/second/b')]
		self.assertFalse(self.packer.build_tarfile(fl, '/tmp/bogus/blah'))
		self.assertFalse(self.packer.build_tarfile(fl, '/root/stuff'))
		self.assertTrue(self.packer.build_tarfile(fl, '/tmp/backup.test'))

	def test_relative(self):
		import posixpath
		import ntpath

		for t in [
			('/tmp/testing/what', 'tmp/testing/what', posixpath),
			('/metoo/more', 'metoo/more', posixpath),
			('./relative/path', './relative/path', os.path),
			('rel/path', 'rel/path', os.path),
			('c:\some\place', 'some\place', ntpath),
			('z:\\another\path', 'another\path', ntpath)
				]:
			path, expected, module = t
			self.assertEquals(
					self.packer.make_relative(path, pathmodule=module), expected)


class TestBackup(unittest.TestCase):
	" Unit tests for module functions. "

	def test_rotate(self):
		resp = backup.rotate(os.path.abspath('./test/rotate'), 'file', 3)
		self.assertTrue(resp)
		


if __name__ == "__main__":
	unittest.main()

