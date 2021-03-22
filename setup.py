from setuptools import setup

setup(
    name='NCAABracketMaker',
    version='0.0.1',
    packages=['NCAABracketMaker'],
    package_dir={'NCAABracketMaker': 'NCAABracketMaker'},
    package_data={'NCAABracketMaker': [
        "data/*.*"]},
    include_package_data=True,
    install_requires=[
        'pandas>=1.1.0',
        'pip>=9',
        'setuptools>=41',
        'pyyaml>=5.3',
        'requests>=2.22.0',
        'numpy>=1.18.0',
        'PyPDF2>=1.26.0'
    ],
    url='https://github.com/hillaxj/NCAABracketMaker',
    license='MIT',
    author='hillajx',
    author_email='',
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Environment :: IDE",
        "Intended Audience :: Science/Research",
        "License :: CC0",
        "Programming Language :: Python :: 3.x",
        "Topic :: Utilities",
    ],
    description='Generates NCAA March Madness Brackets'
)