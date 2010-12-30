"""
 Backup Util

 Only backup the files you want, frequently and automatically.

"""

import tarfile
import sys
import os
import re
import logging

log = logging

# TODO: pass exclude list to Tarfile for finer grain exclude 
# TODO: move config to another file (JSON, XML, property, python)?

config = {
	# name used in the backup file
	'backup_name': 'dn-laptop',
	# number of backup packages
	'num_backup_packages': 2,
	# local backup location
	'local_path': '/home/pontiffx/backup/',

	# path regex to include
	# format: (dir, file_regex, exclude_list)
	'include': [
		('/home/pontiffx/', '\..*', set(('.cache', '.Trash'))),
		('/etc',),
		('/home/pontiffx/pers',),
		('/root/', '\..*'),
	],
}



class Packager(object):
	"""
	Build a compressed tarball from the list of include sources.
	"""

	def __init__(self):
		pass

	def package(self, include, filename):
		"""
		Create a new package tarball from the list of include files, and store
		it as filename.
		"""
		expanded_list = self.expand_file_list(include)
		self.build_tarfile(expanded_list, filename)

	def expand_file_list(self, include):
		"""
		Expand the include list to a full list of directories.
		"""
		expanded = []
		for include_tuple in include:

			if len(include_tuple) < 1:
				log.warn("Skipping empty tuple in include.")
				continue
			path = include_tuple[0]

			if len(include_tuple) >= 2:
				pattern = re.compile(include_tuple[1])
			else:
				pattern = re.compile("")

			if len(include_tuple) >= 3:
				excluded = include_tuple[2]
			else:
				excluded = set()

			# just a file
			if os.path.isfile(path):
				expanded.append(path)
				continue

			if not os.path.isdir(path):
				log.warn("Skipping: %s (Not a file or directory)" % (path))
				continue
			
			try:
				file_list = os.listdir(path)
			except OSError, e:
				log.warn("Error reading dir (%s): %s" % (path, e))

			for filename in file_list: 
				if pattern.match(filename):
					if filename in excluded:
						continue
					expanded.append(
							os.path.normpath("%s/%s" % (path, filename)))
		return expanded


	# TODO: this requires 2.7
	class FilterCallable(object):
		
		def __init__(self, includes):
			self.includes = includes

		def __call__(self, filename):
			pass

	def build_tarfile(self, file_list, name):
		"""
		 Build a compressed tarball that includes all the paths in include
		"""
		try:
			tf = tarfile.open(name, mode='w:bz2')
		except (IOError, tarfile.TarError), e:
			log.warn("Failed to create archive: %s" % e)
			return False

		for file_path in file_list:
			try:
				arcname = self.make_relative(file_path)
				tf.add(file_path, arcname)
			except (OSError, IOError), e:
				log.warn("Failed to add (%s): %s" % (file_path, e))

		tf.close()
		return True

	@staticmethod
	def make_relative(file_path, pathmodule=os.path):
		"""
		Make an absolute path relative to the root of the filesystem.  This is
		done so that when the backed up files are extracted they do not 
		overwrite the new files.

		*Should* be portable to all OS supported by python.
		"""
		if not pathmodule.isabs(file_path):
			return file_path

		drive, arcname = pathmodule.splitdrive(file_path)
		return arcname[1:]
	


def rotate(path, name, copies):
	"""
	Rotate files, and move older files.
	"""
	if copies <= 1:
		return

	for num in range(copies-2, -1, -1):
		cur = filename(path, name, num)
		new = filename(path, name, num+1)

		if not os.path.isfile(cur):
			continue

		try:
			os.rename(cur, new)
		except OSError, e:
			log.warn("Failed to rotate %s to %s: %s" % (cur, new, e))
			return False
	return True
		

def filename(path, name, num=0):
	return os.path.normpath("%s/%s.%d.tar.bz2" % (path, name, num))



if __name__ == "__main__":
	from optparse import OptionParser

	parser = OptionParser(usage="Usage: %prog [options]")
	parser.add_option("-r", "--rotateonly", 
			action="store_true", dest="rotateonly",
			help="Only rotate the files.")
	parser.add_option("-b", "--backuponly", 
			action="store_true", dest="backuponly",
			help="Only backup the files, do not rotate.")
	(options, args) = parser.parse_args()

	if not options.backuponly:
		rotate(config['local_path'], config['backup_name'], 
				config['num_backup_packages'])

	if not options.rotateonly:
		p = Packager()
		p.package(config['include'], 
				filename(config['local_path'], config['backup_name']))

