from setuptools import setup

setup(name='cappy',
      version='1.0.0',
      description='The redcap api you build yourself',
      url='http://github.com/pfwhite/cappy',
      author='Patrick White',
      author_email='pfwhite9@gmail.com',
      license='MIT',
      packages=['cappy'],
      include_package_data=True,
      install_requires=['requests'],
      zip_safe=False)
