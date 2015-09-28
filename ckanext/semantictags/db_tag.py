import vdm.sqlalchemy
from sqlalchemy.orm import relation
from sqlalchemy import types, Column, Table, ForeignKey, and_, UniqueConstraint

import package as _package
import extension as _extension
import core
import meta
import types as _types
import domain_object
import vocabulary
import activity
import ckan  # this import is needed
import ckan.lib.dictization

__all__ = ['semantictag_table', 'package_semantictag_table', 'SemanticTag', 'PackageSemanticTag',
           'package_semantictag_revision_table',
           'MAX_TAG_LENGTH', 'MIN_TAG_LENGTH']

MAX_TAG_LENGTH = 200
MIN_TAG_LENGTH = 2

semantictag_table = Table('semantictag', meta.metadata,
        Column('id', types.UnicodeText, primary_key=True, default=_types.make_uuid),
        Column('URI', types.Unicode(MAX_TAG_LENGTH), nullable=False),
        Column('label', types.Unicode(MAX_TAG_LENGTH))
)

package_semantictag_table = Table('package_semantictag', meta.metadata,
        Column('id', types.UnicodeText, primary_key=True, default=_types.make_uuid),
        Column('package_id', types.UnicodeText, ForeignKey('package.id')),
        Column('semantictag_id', types.UnicodeText, ForeignKey('semantictag.id')),
        )

vdm.sqlalchemy.make_table_stateful(package_tag_table)
# TODO: this has a composite primary key ...
package_semantictag_revision_table = core.make_revisioned_table(package_semantictag_table)

class SemanticTag(domain_object.DomainObject):
    def __init__(self, name='', vocabulary_id=None):
        self.name = name
        #self.vocabulary_id = vocabulary_id

    # not stateful so same as purge
    def delete(self):
        self.purge()

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
    def by_name(cls, URI, label=None, autoflush=True):
        '''Return the semantic ag with the given name, or None.

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
    def get(cls, tag_id_or_name, vocab_id_or_name=None):
        '''Return the tag with the given id or name, or None.

        By default only free tags (tags which do not belong to any vocabulary)
        are returned.

        If the optional argument ``vocab_id_or_name`` is given then only tags
        that belong to that vocabulary will be returned, and ``None`` will be
        returned if there is no vocabulary with that vocabulary id or name or
        if there is no tag with that tag id or name in that vocabulary.

        :param tag_id_or_name: the id or name of the tag to return
        :type tag_id_or_name: string
        :param vocab_id_or_name: the id or name of the vocabulary to look for
            the tag in
        :type vocab_id_or_name: string

        :returns: the tag object with the given id or name, or None if there is
            no tag with that id or name
        :rtype: ckan.model.tag.Tag

        '''
        # First try to get the tag by ID.
        semantictag = SemanticTag.by_id(tag_id_or_name)
        if semantictag:
            return semantictag

        else:
            semantictag = SemanticTag.by_name(tag_id_or_name)
            return tag
        # Todo: Make sure tag names can't be changed to look like tag IDs?

    @classmethod
    def search_by_name(cls, search_term, vocab_id_or_name=None):
        '''Return all tags whose names contain a given string.

        By default only free tags (tags which do not belong to any vocabulary)
        are returned. If the optional argument ``vocab_id_or_name`` is given
        then only tags from that vocabulary are returned.

        :param search_term: the string to search for in the tag names
        :type search_term: string
        :param vocab_id_or_name: the id or name of the vocabulary to look in
            (optional, default: None)
        :type vocab_id_or_name: string

        :returns: a list of tags that match the search term
        :rtype: list of ckan.model.tag.Tag objects

        '''
#        if vocab_id_or_name:
#            vocab = vocabulary.Vocabulary.get(vocab_id_or_name)
#            if vocab is None:
#                # The user specified an invalid vocab.
#                return None
#            query = meta.Session.query(Tag).filter(Tag.vocabulary_id==vocab.id)
#        else:
        query = meta.Session.query(SemanticTag)
        search_term = search_term.strip().lower()
        query = query.filter(SemanticTag.URI.contains(search_term))
        query = query.distinct().join(SemanticTag.package_tags)
        return query

    @classmethod
    def all(cls, vocab_id_or_name=None):
        '''Return all tags that are currently applied to any dataset.

        By default only free tags (tags which do not belong to any vocabulary)
        are returned. If the optional argument ``vocab_id_or_name`` is given
        then only tags from that vocabulary are returned.

        :param vocab_id_or_name: the id or name of the vocabulary to look in
            (optional, default: None)
        :type vocab_id_or_name: string

        :returns: a list of all tags that are currently applied to any dataset
        :rtype: list of ckan.model.tag.Tag objects

        '''
#        if vocab_id_or_name:
#            vocab = vocabulary.Vocabulary.get(vocab_id_or_name)
#            if vocab is None:
#                # The user specified an invalid vocab.
#                raise ckan.logic.NotFound("could not find vocabulary '%s'"
#                        % vocab_id_or_name)
#           query = meta.Session.query(Tag).filter(Tag.vocabulary_id==vocab.id)
#        else:
        query = meta.Session.query(SemanticTag)
        query = query.distinct().join(PackageTag)
        query = query.filter_by(state='active')
        return query

    @property
    def packages(self):
        '''Return a list of all packages that have this tag, sorted by name.

        :rtype: list of ckan.model.package.Package objects

        '''
        q = meta.Session.query(_package.Package)
        q = q.join(PackageSemanticTag)
        q = q.filter_by(tag_id=self.id)
        q = q.filter_by(state='active')
        q = q.order_by(_package.Package.name)
        packages = q.all()
        return packages

    def __repr__(self):
        return '<Tag %s>' % self.URI

class PackageSemanticTag(vdm.sqlalchemy.RevisionedObjectMixin,
        vdm.sqlalchemy.StatefulObjectMixin,
        domain_object.DomainObject):
    def __init__(self, package=None, semantictag=None, state=None, **kwargs):
        self.package = package
        self.semantictag = semantictag
        self.state = state
        for k,v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        s = u'<PackageSemanticTag package=%s tag=%s>' % (self.package.name, self.semantictag.URI)
        return s.encode('utf8')

    def activity_stream_detail(self, activity_id, activity_type):
        if activity_type == 'new':
            # New PackageTag objects are recorded as 'added tag' activities.
            activity_type = 'added'
        elif activity_type == 'changed':
            # Changed PackageTag objects are recorded as 'removed tag'
            # activities.
            # FIXME: This assumes that whenever a PackageTag is changed it's
            # because its' state has been changed from 'active' to 'deleted'.
            # Should do something more here to test whether that is in fact
            # what has changed.
            activity_type = 'removed'
        else:
            return None

        # Return an 'added tag' or 'removed tag' activity.
        import ckan.model as model
        c = {'model': model}
        d = {'semantictag': ckan.lib.dictization.table_dictize(self.semantictag, c),
            'package': ckan.lib.dictization.table_dictize(self.package, c)}
        return activity.ActivityDetail(
            activity_id=activity_id,
            object_id=self.id,
            object_type='tag',
            activity_type=activity_type,
            data=d)

    @classmethod
    def by_name(self, package_name, semantictag_name, vocab_id_or_name=None,
            autoflush=True):
        '''Return the PackageTag for the given package and tag names, or None.

        By default only PackageTags for free tags (tags which do not belong to
        any vocabulary) are returned. If the optional argument
        ``vocab_id_or_name`` is given then only PackageTags for tags from that
        vocabulary are returned.

        :param package_name: the name of the package to look for
        :type package_name: string
        :param tag_name: the name of the tag to look for
        :type tag_name: string
        :param vocab_id_or_name: the id or name of the vocabulary to look for
            the tag in
        :type vocab_id_or_name: string

        :returns: the PackageTag for the given package and tag names, or None
            if there is no PackageTag for those package and tag names
        :rtype: ckan.model.tag.PackageTag

        '''
        if vocab_id_or_name:
            vocab = vocabulary.Vocabulary.get(vocab_id_or_name)
            if vocab is None:
                # The user specified an invalid vocab.
                return None
            query = (meta.Session.query(PackageTag, Tag, _package.Package)
                    .filter(Tag.vocabulary_id == vocab.id)
                    .filter(_package.Package.name==package_name)
                    .filter(Tag.name==tag_name))
        else:
            query = (meta.Session.query(PackageTag)
                    .filter(_package.Package.name==package_name)
                    .filter(Tag.name==tag_name))
        query = query.autoflush(autoflush)
        return query.one()[0]

    def related_packages(self):
        return [self.package]

meta.mapper(Tag, tag_table, properties={
    'package_tags': relation(PackageTag, backref='tag',
        cascade='all, delete, delete-orphan',
        ),
    'vocabulary': relation(vocabulary.Vocabulary,
        order_by=tag_table.c.name)
    },
    order_by=tag_table.c.name,
    )

meta.mapper(PackageSemanticTag, package_tag_table, properties={
    'pkg':relation(_package.Package, backref='package_tag_all',
        cascade='none',
        )
    },
    order_by=package_semantictag_table.c.id,
    extension=[vdm.sqlalchemy.Revisioner(package_semantictag_revision_table),
               _extension.PluginMapperExtension(),
               ],
    )
