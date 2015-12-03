ckanext-semantictags
====================

CKAN SemanticTags plugin gives the possibility for Open Data Portals to atribute semantic tags to their datasets.

What can you do with the SemanticTags plugin?
-------------------------------------------
With the SemanticTags plugin you can:

- Relate your CKAN tags with semantic objects
- Define custom RDF predicates for linking your datasets with the Linked Open Data cloud
- Connect several CKAN instances through the use of global semantic tags

Why a SemanticTags plugin?
-------------------------------------------
CKAN core offers an RDF version of each database, which gives access to all metadata in Linked Open Data format. However, it does not allow linking the database to external semantic resources. SemanticTags fills this gap, allowing datasets to be tagged with LOD resources.

------------
Requirements
------------

CKAN >= 2.5

------------
Installation
------------

To install ckanext-semantictags:

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate

2. Install the ckanext-semantictags Python package into your virtual environment::

	pip install ckanext-semantictags

3. Run the database migration::

	paster --plugin=ckanext-semantictags semantictags migrate -c /etc/ckan/default/production.ini	

3. Add ``semantictags`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

     sudo service apache2 reload


------------------------
Development Installation
------------------------

To install ckanext-semantictags for development, activate your CKAN virtualenv and
do::

    git clone https://github.com/alantygel/ckanext-semantictags.git
    cd ckanext-semantictags
    python setup.py develop
    paster --plugin=ckanext-semantictags semantictags migrate -c /etc/ckan/default/development.ini

Add ``semantictags`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/development.ini``).


