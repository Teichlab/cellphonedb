from setuptools import setup, find_packages

setup(
    name='CellPhoneDB',
    author='TeichLab',
    author_email='contact@cellphonedb.org',
    version='2.1.4',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    maintainer='YDEVS CONSULTING',
    maintainer_email='hi@ydevs.com',
    url='https://cellphonedb.org',
    license='MIT',
    exclude_package_data={'': ['tools']},
    entry_points={
        'console_scripts':
            [
                'cellphonedb = cellphonedb.cellphonedb_cli:cli'
            ]
    },
    install_requires=[
        'click>=6.7',
        'pandas>=0.23',
        'flask>=1.0',
        'Flask-RESTful>=0.3',
        'Flask-Testing>=0.7',
        'SQLAlchemy>=1.3',
        'PyYAML>=5.1',
        'requests>=2.19',
        'pika>=0.12',
        'boto3>=1.7',
        'geosketch==0.3',
        'rpy2>=3.0.4',
        'tqdm>=4.32',
        'cython>=0.29'
    ],
)
