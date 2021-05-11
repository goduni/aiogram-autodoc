from setuptools import setup, find_packages

setup(
    name='aiogram_autodoc',
    version='0.0.2',
    url='https://github.com/viuipan/aiogram-autodoc',
    author_email='viuipan@gmail.com',
    license='MIT',
    description='Generates command documentation from handlers',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    packages=['aiogram_autodoc'],
    setup_requires=['aiogram<3']
)
