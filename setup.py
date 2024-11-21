"""
 setup.py for GSOF_3dWireFram

    This file is part of GSOF_3dWireFram.

    GSOF_3dWireFram is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    GSOF_3dWireFram is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with GSOF_3dWireFram.  If not, see <https://www.gnu.org/licenses/>.

 Under windows install:
   "setup.bat"

 Direct install for all systems:
   "python setup.py install"
"""


from setuptools import setup

def readme():
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()

setup(
      name='GSOF_3dWireFrame',
      version='0.1',
      description='Protocol stack to bridge between an Arduino and Python',
      long_description=readme(),
      long_description_content_type='text/markdown',
      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Multimedia :: Graphics :: 3D Rendering',
      ],
      platforms = 'any',
      keywords='3dWireFrame',
      url = 'https://github.com/mrGSOF/3dWireFrame.git',
      author='Guy Soffer',
      author_email='gsoffer@yahoo.com',
      license='GPL-3.0-or-later',
      packages=['GSOF_3dWireFrame',
                'GSOF_3dWireFrame.Lib3D',
                'GSOF_3dWireFrame.MathLib',
                'GSOF_3dWireFrame.modules'],
      include_package_data=True,
      package_data={'GSOF_3dWireFrame': ['./objects/*.*']},
      install_requires=[
        'pyserial>=2.7',
    ]
)
