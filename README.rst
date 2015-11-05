
=============
ckanext-semantictags
=============

CKAN Semantic Tags gives the possibility for Open Data Portals to semantically tag their datasets. It also allows CKAN portals to connect to a Tag Server, in order to exchange data with other portals.

------------
Requirements
------------

CKAN >= 2.5

------------
Installation
------------

.. Add any additional install steps to the list below.
   For example installing any non-Python dependencies or adding any required
   config settings.

To install ckanext-semantictags:

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate

2. Install the ckanext-semantictags Python package into your virtual environment::

git clone https://github.com/alantygel/ckanext-semantictags
python setup.py develop
paster --plugin=ckanext-semantictags semantictags migrate -c /etc/ckan/default/production.ini	

3. Add ``semantictags`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

     sudo service apache2 reload


---------------
Config Settings
---------------

Document any optional config settings here. For example::

    # The minimum number of hours to wait before re-checking a resource
    # (optional, default: 24).
    ckanext.semantictags.some_setting = some_default_value


------------------------
Development Installation
------------------------

To install ckanext-semantictags for development, activate your CKAN virtualenv and
do::

    git clone https://github.com/alantygel/ckanext-semantictags.git
    cd ckanext-semantictags
    python setup.py develop
    pip install -r dev-requirements.txt


-----------------
Running the Tests
-----------------

To run the tests, do::

    nosetests --nologcapture --with-pylons=test.ini

To run the tests and produce a coverage report, first make sure you have
coverage installed in your virtualenv (``pip install coverage``) then run::

    nosetests --nologcapture --with-pylons=test.ini --with-coverage --cover-package=ckanext.semantictags --cover-inclusive --cover-erase --cover-tests


---------------------------------
Registering ckanext-semantictags on PyPI
---------------------------------

ckanext-semantictags should be availabe on PyPI as
https://pypi.python.org/pypi/ckanext-semantictags. If that link doesn't work, then
you can register the project on PyPI for the first time by following these
steps:

1. Create a source distribution of the project::

     python setup.py sdist

2. Register the project::

     python setup.py register

3. Upload the source distribution to PyPI::

     python setup.py sdist upload

4. Tag the first release of the project on GitHub with the version number from
   the ``setup.py`` file. For example if the version number in ``setup.py`` is
   0.0.1 then do::

       git tag 0.0.1
       git push --tags


----------------------------------------
Releasing a New Version of ckanext-semantictags
----------------------------------------

ckanext-semantictags is availabe on PyPI as https://pypi.python.org/pypi/ckanext-semantictags.
To publish a new version to PyPI follow these steps:

1. Update the version number in the ``setup.py`` file.
   See `PEP 440 <http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers>`_
   for how to choose version numbers.

2. Create a source distribution of the new version::

     python setup.py sdist

3. Upload the source distribution to PyPI::

     python setup.py sdist upload

4. Tag the new release of the project on GitHub with the version number from
   the ``setup.py`` file. For example if the version number in ``setup.py`` is
   0.0.2 then do::

       git tag 0.0.2
       git push --tags
