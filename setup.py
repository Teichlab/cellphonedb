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
        'click>=6.7,<6.7.99',
        'pandas>=0.23,<0.23.99',
        'flask>=1.0,<1.0.99',
        'Flask-RESTful>=0.3,<0.3.99',
        'Flask-Testing>=0.7,<0.7.99',
        'SQLAlchemy>=1.3,<1.3.99',
        'PyYAML>=5.1,<5.1.99',
        'requests>=2.19,<2.19.99',
        'pika>=0.12,<0.12.99',
        'boto3>=1.7,<1.7.99',
        'geosketch==0.3',
        'rpy2>=3.0.4,<3.0.99',
        'tqdm>=4.32,<4.32.99',
        'cython>=0.29,<0.29.99'
    ],
)
