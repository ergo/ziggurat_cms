import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

setup(name='ziggurat_cms_front_front',
      version='0.0',
      description='Front js for Ziggurat CMS',
      long_description='Front js for Ziggurat CMS',
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi javascript polymer pyramid ziggurat cms ziggurat_cms',
      package_dir={'': 'src'},
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      extras_require={
          'testing': [],
      },
      install_requires=[],
      entry_points={
          'ziggurat_cms.packages': {
              'ziggurat_cms_front_front = ziggurat_cms_front_front'
          }
      }
      )
