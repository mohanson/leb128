import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='leb128',
    version='1.0.3',
    url='https://github.com/mohanson/leb128',
    license='MIT',
    author='Mohanson',
    author_email='mohanson@outlook.com',
    description='LEB128(Little Endian Base 128)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['leb128'],
)
