from setuptools import setup, find_packages

setup(
    name='fabric-threadsafe',
    version=__import__('fabric_threadsafe').__version__,
    description='Monkeypatch script to make Fabric thread-safe',
    author='Luka Zakrajsek',
    author_email='luka@bancek.net',
    url='https://github.com/bancek/fabric-threadsafe',
    license='Apache',
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    zip_safe=True,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Networking',
    ],
)