from setuptools import setup, find_packages

setup(
    name='CellPhoneDB',
    author='TeichLab',
    author_email='contact@cellphonedb.org',
    version='0.0.1',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    maintainer='Miquel Vento',
    maintainer_email='miquel@ydevs.com',
    url='https://cellphonedb.org',
    license='MIT',
    exclude_package_data={'': ['tools']},
    install_requires=[
        'click',
        'pandas>=0.23',
        'flask>=1.0',
        'Flask-RESTful>=0.3.6',
        'Flask-Testing>=0.7.1',
        'SQLAlchemy==1.2.8',
        'PyYAML==3.12',
    ],
)
