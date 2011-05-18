#!/usr/bin/env python

from distutils.core import setup
from distutils.command.install_scripts import install_scripts

class post_install(install_scripts):

    def run(self):
        install_scripts.run(self)

        from shutil import move
        for i in self.get_outputs():
            n = i.replace('.py', '')
            move(i, n)
            print "moving '{0}' to '{1}'".format(i, n)

ID = 'org.sbillaudelle.VolumeControlService'

data_files = [
    ('share/cream/{0}'.format(ID), ['src/manifest.xml']),
    ('share/cream/{0}/configuration'.format(ID), ['src/configuration/scheme.xml']),
]

setup(
    name = 'volume-control-service',
    version = '0.1.1',
    author = 'Sebastian Billaudelle',
    url = 'http://github.com/sbillaudelle/volume-control',
    data_files = data_files,
    cmdclass={'install_scripts': post_install},
    scripts = ['src/volume-control-service.py']
)
