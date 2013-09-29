from setuptools import setup
import os.path

__version__ = '1.4.0'

descr_file = os.path.join(os.path.dirname(__file__), 'README.rst')

setup(
    name='actr6_jni',
    version=__version__,
    
    packages=['actr6_jni'],

    description='A high level library wrapper for the ACT-R JNI using Twisted.',
    long_description=open(descr_file).read(),
    author='Ryan Hope',
    author_email='rmh3093@gmail.com',
    url='https://github.com/RyanHope/json-network-interface',
    classifiers=[
				'License :: OSI Approved :: GNU General Public License (GPL)',
				'Framework :: Twisted',
				'Programming Language :: Python :: 2',
				'Topic :: Scientific/Engineering',
				'Topic :: Utilities'
    ],
	license='GPL-3',
	install_requires=[
					'panglery',
					'twisted'
	],
 )
