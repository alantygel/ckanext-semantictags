import vdm.sqlalchemy
from sqlalchemy.orm import relation
from sqlalchemy import types, Column, Table, ForeignKey, and_, UniqueConstraint

import ckan.model.tag as _tag
import ckan.model.extension as _extension
import ckan.model.core as core
import ckan.model.meta as meta
import ckan.model.types as _types
import ckan.model.domain_object as domain_object
import ckan.model.activity as activity
import ckan  # this import is needed
import ckan.lib.dictization

__all__ = ['semantictag_table', 'predicate_table', 'tag_semantictag_table', 'SemanticTag', 'Predicate', 'TagSemanticTag',
		   'tag_semantictag_revision_table',
		   'MAX_TAG_LENGTH', 'MIN_TAG_LENGTH']

MAX_TAG_LENGTH = 200
MIN_TAG_LENGTH = 2

semantictag_table = Table('st_semantictag', meta.metadata,
		Column('id', types.UnicodeText, primary_key=True, default=_types.make_uuid),
		Column('URI', types.Unicode(MAX_TAG_LENGTH), nullable=False),
		Column('label', types.Unicode(MAX_TAG_LENGTH))
)

predicate_table = Table('st_predicate', meta.metadata,
		Column('id', types.UnicodeText, primary_key=True, default=_types.make_uuid),
		Column('namespace', types.Unicode(MAX_TAG_LENGTH), nullable=False),
		Column('prefix', types.Unicode(MAX_TAG_LENGTH), nullable=False),
		Column('predicate', types.Unicode(MAX_TAG_LENGTH), nullable=False)
)

tag_id = Column('tag_id', types.UnicodeText, ForeignKey('tag.id',ondelete="CASCADE"))
semantic_tag_id = Column('semantictag_id', types.UnicodeText, ForeignKey('st_semantictag.id',ondelete="CASCADE"))

tag_semantictag_table = Table('st_tag_semantictag', meta.metadata,
		Column('id', types.UnicodeText, primary_key=True, default=_types.make_uuid),
		tag_id,
		semantic_tag_id
		)

vdm.sqlalchemy.make_table_stateful(tag_semantictag_table)
# TODO: this has a composite primary key ...
#tag_semantictag_revision_table = core.make_revisioned_table(tag_semantictag_table)

class SemanticTag(domain_object.DomainObject):
	def __init__(self, URI=None, label=None):
		self.URI = URI
		self.label = label

	# not stateful so same as purge
	def delete(self):
		print "xxx"
		self.purge()
		return

	@classmethod
	def by_id(cls, semantictag_id, autoflush=True):
		'''Return the semantic tag with the given id, or None.

		:param semantictag_id: the id of the semantic tag to return
		:type semantictag_id: string

		:returns: the semantic tag with the given id, or None if there is no tag with
			that id
		:rtype: ckan.model.semantictag.SemanticTag # TODO check this

		'''
		query = meta.Session.query(SemanticTag).filter(SemanticTag.id==semantictag_id)
		query = query.autoflush(autoflush)
		semantictag = query.first()
		return semantictag

	@classmethod
	def by_URI(cls, URI, label=None, autoflush=True):
		'''Return the semantic ag with the given URI, or None.

		:param URI: the URI of the semantic tag to return
		:type URI: string (URI format)
		:param label: URI's label (optional, default: None)
		:type label: string

		:returns: the semantic tag object with the given id or URI, or None if there is
			no tag with that id or name
		:rtype: ckan.model.semantictag.SemanticTag #TODO check this

		'''
		if label:
			query = meta.Session.query(SemanticTag).filter(SemanticTag.label==label)
		else:
			query = meta.Session.query(SemanticTag).filter(SemanticTag.URI==URI)
		query = query.autoflush(autoflush)
		semantictag = query.first()
		return semantictag

	@classmethod
	def get(cls, tag_id_or_URI, label=None):
		'''Return the tag with the given id or URI, or None.

		:param tag_id_or_name: the id or name of the tag to return
		:type tag_id_or_name: string

		:returns: the tag object with the given id or name, or None if there is
			no tag with that id or name
		:rtype: ckan.model.tag.Tag

		'''
		# First try to get the tag by ID.
		semantictag = SemanticTag.by_id(tag_id_or_URI)
		if semantictag:
			return semantictag

		else:
			semantictag = SemanticTag.by_URI(tag_id_or_URI)
			return semantictag
		# Todo: Make sure tag names can't be changed to look like tag IDs?

	@classmethod
	def search_by_URI(cls, search_term):
		'''Return all tags whose URI or label contain a given string.

		:param search_term: the string to search for in the URI or label names
		:type search_term: string

		:returns: a list of semantictags that match the search term
		:rtype: list of ckan.model.semantictag.SemanticTag objects

		'''
	#TODO include label search
		query = meta.Session.query(SemanticTag)
		search_term = search_term.strip().lower()
		query = query.filter(SemanticTag.URI.contains(search_term))
		query = query.distinct().join(SemanticTag.tag_semantictags)
		return query

	@classmethod
	def list_all(cls):
		'''Return all semantic tags 

		:returns: a list of all semantic tags 
		:rtype: list of ckan.model.semantictag.SemanticTag objects

		'''
		query = meta.Session.query(SemanticTag)
		return query.all()
 
	@classmethod
	def all(cls):
		'''Return all tags that are currently applied to any dataset.

		:returns: a list of all tags that are currently applied to any dataset
		:rtype: list of ckan.model.tag.Tag objects

		'''
#		if vocab_id_or_name:
#			vocab = vocabulary.Vocabulary.get(vocab_id_or_name)
#			if vocab is None:
#				# The user specified an invalid vocab.
#				raise ckan.logic.NotFound("could not find vocabulary '%s'"
#						% vocab_id_or_name)
#		   query = meta.Session.query(Tag).filter(Tag.vocabulary_id==vocab.id)
#		else:
		query = meta.Session.query(SemanticTag)
		query = query.distinct().join(TagSemanticTag)
#		query = query.filter_by(state='active')
		return query

	@property
	def tags(self):
		'''Return a list of all tags that have this semantic tag, sorted by name.

		:rtype: list of ckan.model.tag.Tag objects

		'''
		q = meta.Session.query(_tag.Tag)
		q = q.join(TagSemanticTag)
		q = q.filter_by(tag_id=self.id)
#		q = q.filter_by(state='active')
		q = q.order_by(_tag.Tag.name)
		tags = q.all()
		return tags

	def __repr__(self):
		return '<SemanticTag %s>' % self.URI

#class TagSemanticTag(vdm.sqlalchemy.RevisionedObjectMixin,
#		vdm.sqlalchemy.StatefulObjectMixin,
#		domain_object.DomainObject):i

class Predicate(domain_object.DomainObject):
	def __init__(self, namespace,prefix,predicate):
		self.namespace = namespace
		self.prefix = prefix
		self.predicate = predicate

	# not stateful so same as purge
	def delete(self):
		self.purge()
		return

	@classmethod
	def by_id(cls, predicate_id, autoflush=True):
		'''Return the predicate with the given id, or None.

		:param predicate_id: the id of the predicate to return
		:type predicate_id: string

		:returns: the predicate with the given id, or None if there is no predicate with
			that id
		:rtype: ckan.model.semantictag.Predicate

		'''
		query = meta.Session.query(Predicate).filter(Predicate.id==predicate_id)
		query = query.autoflush(autoflush)
		return query.first()

#	@classmethod
#	def by_URI(cls, URI, label=None, autoflush=True):
#		'''Return the Predicate with the given URI, or None.

#		:param URI: the URI of the semantic tag to return
#		:type URI: string (URI format)
#		:param label: URI's label (optional, default: None)
#		:type label: string

#		:returns: the predicate object with the given id or URI, or None if there is
#			no Predicate with that id or name
#		:rtype: ckan.model.semantictag.Predicate

#		'''
#		if label:
#			query = meta.Session.query(Predicate).filter(Predicate.label==label)
#		else:
#			query = meta.Session.query(Predicate).filter(Predicate.URI==URI)
#		query = query.autoflush(autoflush)
#		return query.first()

	@classmethod
	def list_all(cls):
		'''Return all predicates

		:returns: a list of all predicates 
		:rtype: list of ckan.model.semantictag.Predicate objects

		'''
		query = meta.Session.query(Predicate)
		return query.all()
 
	@classmethod
	def list_unique(cls):
		'''Return all unique namespaces

		:returns: a list of all predicates 
		:rtype: list of ckan.model.semantictag.Predicate objects

		'''
		query = meta.Session.query(Predicate).distinct(Predicate.namespace)
		return query.all()


class TagSemanticTag(domain_object.DomainObject):

	def __init__(self, tag=None, semantictag=None):#, state=None): #, **kwargs):
		self.tag_id = tag.id
		self.semantictag_id = semantictag.id
		#self.state = state
	
		#for k,v in kwargs.items():
		#	setattr(self, k, v)

	def __repr__(self):
		s = u'<TagSemanticTag tag=%s semantictag=%s>' % (self.tag_id, self.semantictag_id)
		return s.encode('utf8')

	def activity_stream_detail(self, activity_id, activity_type):
		if activity_type == 'new':
			# New TagSemanticTag objects are recorded as 'added tag' activities.
			activity_type = 'added'
		elif activity_type == 'changed':
			# Changed TagSemanticTag objects are recorded as 'removed tag'
			# activities.
			# FIXME: This assumes that whenever a TagSemanticTag is changed it's
			# because its' state has been changed from 'active' to 'deleted'.
			# Should do something more here to test whether that is in fact
			# what has changed.
			activity_type = 'removed'
		else:
			return None

		# Return an 'added semantic tag' or 'removed tag' activity.
		import ckan.model as model
		c = {'model': model}
		d = {'semantictag': ckan.lib.dictization.table_dictize(self.semantictag, c),
			'tag': ckan.lib.dictization.table_dictize(self.tag, c)}
		return activity.ActivityDetail(
			activity_id=activity_id,
			object_id=self.id,
			object_type='tag',
			activity_type=activity_type,
			data=d)

	@classmethod
	def by_name(self, tag_name, semantictag_URI,
			autoflush=True):
		'''Return the TagSemanticTag for the given tag name and semantic tag URI, or None.

		:param tag_name: the name of the tag to look for
		:type tag_name: string
		:param tag_URI: the name of the tag to look for
		:type tag_URI: string

		:returns: the TagSemanticTag for the given tag name and semantic tag URI, or None
			if there is no TagSemanticTag for those semantic tag and tag names
		:rtype: ckan.model.tag_semanictag.TagSemanticTag

		'''
		
		query = (meta.Session.query(TagSemanticTag)
					.filter(_tag.Tag.name==tag_name)
					.filter(SemanticTag.URI==semantictag_URI))
		query = query.autoflush(autoflush)
		return query.one()[0]

	def related_tags(self):
		return [self.tags]

	@classmethod
	def list_all(cls):
		'''Return all tag semantic tags 

		:returns: a list of all tag semantic tags 
		:rtype: list of ckan.model.tagsemantictag.TagSemanticTag objects

		'''
		query = meta.Session.query(TagSemanticTag)
		return query.all()

	@classmethod
	def by_tag_id(self,tag_id):
		'''Return all the semantic tag related to the given tag id

		:returns: a semantic tag or None
		:rtype: list of ckan.model.semantictag.SemanticTag object

		'''
		query = meta.Session.query(TagSemanticTag).filter(TagSemanticTag.tag_id==tag_id)
		return query.first()

	@classmethod
	def get(self,id):
		'''Return all the semantic tag related to the given tag id

		:returns: a semantic tag or None
		:rtype: list of ckan.model.semantictag.SemanticTag object

		'''
		query = meta.Session.query(TagSemanticTag).filter(TagSemanticTag.id==id)
		return query.first()



meta.mapper(SemanticTag, semantictag_table, properties={
	'tag_semantictags': relation(TagSemanticTag, backref='semantictag',cascade='all, delete, delete-orphan')
	},
	order_by=semantictag_table.c.URI,
	)

meta.mapper(TagSemanticTag, tag_semantictag_table, properties={
	'tag': relation(_tag.Tag, foreign_keys=[tag_id]),
	'semantic_tag': relation(SemanticTag, foreign_keys=[semantic_tag_id])
	}
	)

meta.mapper(Predicate, predicate_table,order_by=predicate_table.c.namespace)

#meta.mapper(TagSemanticTag, tag_semantictag_table, properties={
#	'smtag':relation(_tag.Tag, backref='tag_semantictag_all',
#		cascade='none',
#		)
#	},
#	order_by=tag_semantictag_table.c.id,
##	extension=[vdm.sqlalchemy.Revisioner(tag_semantictag_revision_table),
##			   _extension.PluginMapperExtension(),
##			   ],
#	)

