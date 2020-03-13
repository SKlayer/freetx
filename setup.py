from setuptools import find_packages, setup

with open('freetx/__init__.py', 'r') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.strip().split('= ')[1].strip("'")
            break

try:
    long_description = open('README.md', 'r').read()
except Exception:
    long_description = 'Bitcoin Cash... failed to read README.md'

setup(
    name='freetx',
    version=version,
    description='Freecash made easier.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Sklayer',
    author_email='sklayer@qq.com',
    maintainer='Sklayer',
    maintainer_email='sklayer@qq.com',
    url='https://github.com/SKlayer/freetx',
    download_url='https://github.com/SKlayer/freetx/tarball/{}'.format(
        version),
    license='MIT',

    keywords=[
        'freecash',
        'cryptocurrency',
        'payments',
        'tools',
        'wallet',
    ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],

    install_requires=['freecrypto', 'requests'],
    extras_require={
        'cli': ('appdirs', 'click', 'privy', 'tinydb'),
        'cache': ('lmdb', ),
    },
    tests_require=['pytest'],

    packages=find_packages(),
    entry_points={
        'console_scripts': (
            'freetx = freetx.cli:freetx',
        ),
    },
)
