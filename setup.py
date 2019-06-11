from setuptools import setup

setup(
    name='alice',
    packages=['alice'],
    include_package_data=True,
    install_requires=[
        'sqlalchemy>=1.3.1',
        'flask>=1.0.2',
        'flask-migrate',
        'sqlalchemy_utils',
        'pymystem3',
    ],
)
