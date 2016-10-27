from setuptools import setup

setup(
    name='manifest-reader',
    version='0.1',
    py_modules=['manifest_reader'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        manifest-reader=manifest_reader:tool
    ''',
)