import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

found_packages = find_packages('src')

setup(name='ziggurat_cms_front_admin',
      version='0.0',
      description='Admin panel for Ziggurat CMS',
      long_description='Admin panel for Ziggurat CMS',
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
      packages=found_packages,
      include_package_data=True,
      zip_safe=False,
      extras_require={
          'testing': [],
      },
      install_requires=[],
      entry_points={
          'ziggurat_cms.packages': {
              'ziggurat_cms_front_admin = ziggurat_cms_front_admin'
          }
      }
      )
