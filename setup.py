from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='guardpost',
      version='1.0.0',
      description='Implementation of dependency injection for Python 3',
      long_description=readme(),
      long_description_content_type='text/markdown',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Operating System :: OS Independent'
      ],
      url='https://github.com/RobertoPrevato/GuardPost',
      author='RobertoPrevato',
      author_email='roberto.prevato@gmail.com',
      keywords='authentication authorization identity claims strategy framework asyncio synchronous',
      license='MIT',
      packages=['guardpost'],
      install_requires=[],
      include_package_data=True,
      zip_safe=False)