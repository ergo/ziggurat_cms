ziggurat_cms README
==================

Getting Started
---------------

- ``cd <directory containing this file>``
- ``$VENV/bin/pip install -r requirements.txt``
- ``$VENV/bin/pip install -r requirements-dev.txt``
- ``$VENV/bin/migrate_ziggurat_cms_db development.ini``
- ``$VENV/bin/initialize_ziggurat_cms_db development.ini``
- ``$VENV/bin/pserve development.ini``

Working with Translations
-------------------------

Create pot file

    pot-create -c message-extraction.ini \
    -o ziggurat_cms/locale/ziggurat_cms.pot \
    --package-name ziggurat_cms ziggurat_cms

create new PO files for specific language:

    msginit -l en -o ziggurat_cms/locale/en/LC_MESSAGES/ziggurat_cms.po

update PO files for specific language:

    msgmerge --update ziggurat_cms/locale/en/LC_MESSAGES/ziggurat_cms.po ziggurat_cms/locale/ziggurat_cms.pot

compile translations

    msgfmt -o ziggurat_cms/locale/en/LC_MESSAGES/ziggurat_cms.mo \
          ziggurat_cms/locale/en/LC_MESSAGES/ziggurat_cms.po
