"""
 Backup Filesystem

 Daniel Nephin

 Configuration:
 	- package name
 	- compression level
	- number of backup packages to keep (rotates packages and removes oldest)
 	- a list of directories to include (can match a pattern)
	- a list of destinations to copy to
		 - filters to process to package for each destination (encryption)

"""

import tarfile
import sys
import os.path
import re
import logging

log = logging

config = {
	# name used in the backup file
	'backup_name': 'dn-laptop',
	# number of backup packages
	'num_backup_packages': 3,
	# local backup location
	'local_path': '/home/pontiffx/backup/',

	# path regex to include
	# format: (dir, file_regex, exclude_list)
	'include': [
		('/home/pontiffx/', '\..*', set(('.cache', '.Trash'))),
		('/etc',),
		('/home/pontiffx/pers',),
#		('/root/', '\..*'),
	],

	# list of destinations for the backup file
	# Tuple format: (name, path, type, filter_name)
	'destinations': [
#		('desktop', 'ssh://daniel@192.168.0.190', 'scp', None),
	],

	# list of function pointers to filter the backup package
	'filters': [
	]
}

# TODO: pass exclude list to Tarfile for finer grain exclude

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
			# TODO: handle DIR does not exist or is not a dir
			# TODO: handle invalid pattern

			if len(include_tuple) < 1:
				log.warn("Skipping empty tuple in include.")
				continue
			directory = include_tuple[0]

			if len(include_tuple) >= 2:
				pattern = re.compile(include_tuple[1])
			else:
				pattern = re.compile("")

			if len(include_tuple) >= 3:
				excluded = include_tuple[2]
			else:
				excluded = set()

			for filename in os.listdir(directory):
				if pattern.match(filename):
					if filename in excluded:
						continue
					expanded.append(
							os.path.normpath("%s/%s" % (directory, filename)))
		return expanded

	def build_tarfile(self, file_list, name):
		"""
		 Build a compressed tarball that includes all the paths in include
		"""
		# TODO: check path is valid
		# TODO: catch ReadError CompressionError
		tf = tarfile.open(name, mode='w:bz2')
		for file_path in file_list:
			try:
				tf.add(file_path)
			except (OSError, IOError), e:
				log.warn("Failed to add (%s): %s" % (file_path, e))

		tf.close()
	

"""
 Send tarball to all destinations.
"""


"""
 Rotate files, and move older files.
"""


if __name__ == "__main__":
	p = Packager()
	p.package(config['include'], '/tmp/test.tar.bz')
