from setuptools import setup
import setuptools

requires = [
    'Flask>=0.9',
    'Flask-Router',
    'Flask-Negotiation',
    'SQLAlchemy',
    'Flask-Admin>=1.0.1',
    'FormEncode-Jinja2',
    'wand',
    'SQLAlchemy-ImageAttach==0.8.0.dev-20130531',
]

setup(
    name='Issue',
    version='0.1.0',
    author='GunWoo Choi',
    author_email='6566gun@gmail.com',
    description='Server',
    long_description=__doc__,
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=requires,
    classifiers=[
        'Environment :: Web Environment',
    ],
)
