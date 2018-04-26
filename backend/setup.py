import os
import re

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()
with open(os.path.join(here, 'requirements.txt')) as f:
    REQUIREMENTS = f.readlines()

with open(os.path.join(here, 'requirements-dev.txt')) as f:
    REQUIREMENTS_DEV = f.readlines()

compiled = re.compile('([^=><]*).*')


def parse_req(req):
    return compiled.search(req).group(1).strip()


requires = filter(None, map(parse_req, REQUIREMENTS))

requires_dev = filter(None, map(parse_req, REQUIREMENTS_DEV))

setup(name='ziggurat_cms',
      version='0.0',
      description='ziggurat_cms',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      extras_require={
          'testing': requires_dev,
      },
      install_requires=requires,
      entry_points={
          'paste.app_factory': [
              'main = ziggurat_cms:main',
          ],
          'console_scripts': [
              'ziggurat_cms_db_migrate = ziggurat_cms.scripts.migratedb:main',
              'ziggurat_cms_db_initialize = ziggurat_cms.scripts.initializedb:main',
              'ziggurat_cms_statics = ziggurat_cms.scripts.statics:main',
          ]
      }
      )
