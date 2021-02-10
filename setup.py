from setuptools import setup, find_packages

with open("requirements.txt", "rt", encoding="utf-8") as fh:
    install_requirements_txt = [line.strip() for line in fh.readlines()]

setup(
    name='CellPhoneDB',
    author='TeichLab',
    author_email='contact@cellphonedb.org',
    version='2.1.5',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    maintainer='TeichLab',
    maintainer_email='contact@cellphonedb.org',
    url='https://cellphonedb.org',
    license='MIT',
    exclude_package_data={'': ['tools']},
    entry_points={
        'console_scripts':
            [
                'cellphonedb = cellphonedb.cellphonedb_cli:cli'
            ]
    },
    install_requires=install_requirements_txt,
)
