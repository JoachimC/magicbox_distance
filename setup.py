import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

INSTALL_REQUIRES = [
    'geopy',
]

setuptools.setup(name='magicbox_distance',
                 version='0.0.1',
                 description='measure distance between points of interest',
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 author='Joachim Chapman <https://github.com/JoachimC>',
                 url='https://github.com/JoachimC/magicbox_distance',
                 packages=setuptools.find_packages(),

                 install_requires=INSTALL_REQUIRES
                 )
