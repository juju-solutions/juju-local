from setuptools import setup

install_requires = [
    # 'lxc',
    'jujuclient',
    'click',
    'clint',
]

tests_require = [
    'coverage',
    'nose',
    'pep8',
]


setup(
    name='jujulocal',
    version='0.0.1',
    description='Juju local plugin, powertools for local provider users',
    install_requires=install_requires,
    author='Marco Ceppi',
    author_email='marco@ceppi.net',
    url="https://github.com/juju-solutions/juju-local",
    packages=['jujulocal'],
    entry_points={
        'console_scripts': [
            'juju-local=jujulocal.cli:main',
        ]
    }
)
