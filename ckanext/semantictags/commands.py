import ckan.plugins as p
import paste.script
import db
import logging

from ckan.lib.cli import CkanCommand

from ckan import model

log = logging.getLogger(__name__)

class SemanticTagsCommands(CkanCommand):
	"""
	ckanext-semantictags commands:
	Usage::
		paster semantictags migrate
	"""
	summary = __doc__.split('\n')[0]
	usage = __doc__

	parser = paste.script.command.Command.standard_parser(verbose=True)
	parser.add_option('-c', '--config', dest='config',
		default='development.ini', help='Config file to use.')

	def command(self):
		if not len(self.args):
			print self.__doc__
			return

		cmd = self.args[0]
		self._load_config()

		if cmd == 'migrate':
			self._migrate()
		else:
			print self.__doc__

	def _migrate(self):
		if not db.semantictag_table.exists():
			db.semantictag_table.create()
			log.info('Semantic Tags table created')
			print 'Semantic Tags table created'
		else:
			log.warning('Semantic Tags table already exists')
			print 'Semantic Tags table already exists'

		if not db.tag_semantictag_table.exists():
			db.tag_semantictag_table.create()
			log.info('Tag Semantic Tags table created')
			print 'Tag Semantic Tags table created'
		else:
			log.warning('Tag Semantic Tags table already exists')
			print 'Tag Semantic Tags table already exists'

		if not db.predicate_table.exists():
			db.predicate_table.create()
			log.info('Predicate table created')
			print 'Predicate table created'
		else:
			log.warning('Predicate table already exists')
			print 'Predicate table already exists'
