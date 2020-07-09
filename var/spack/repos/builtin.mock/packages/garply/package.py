# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import os


class Garply(Package):
    """Toy package for testing dependencies"""

    homepage = "https://www.example.com"
    url      = "https://github.com/gartung/garply/archive/v3.0.0.tar.gz"

    version('3.0.0',
            sha256='534ac8ba7a6fed7e8bbb543bd43ca04999e65337445a531bd296939f5ac2f33d')

    def install(self, spec, prefix):
        garply_h = '''#ifndef GARPLY_H_

class Garply
{
private:
    static const int version_major;
    static const int version_minor;

public:
    Garply();
    int get_version() const;
    int garplinate() const;
};

#endif // GARPLY_H_
'''
        garply_cc = '''#include "garply.h"
#include "garply_version.h"
#include <iostream>

const int Garply::version_major = garply_version_major;
const int Garply::version_minor = garply_version_minor;

Garply::Garply() {}

int
Garply::get_version() const
{
    return 10 * version_major + version_minor;
}

int
Garply::garplinate() const
{
    std::cout << "Garply::garplinate version " << get_version()
              << " invoked" << std::endl;
    std::cout << "Garply config dir = %s" << std::endl;
    return get_version();
}
'''
        garplinator_cc = '''#include "garply.h"
#include <iostream>

int
main()
{
    Garply garply;
    garply.garplinate();

    return 0;
}
'''
        garply_version_h = '''const int garply_version_major = %s;
const int garply_version_minor = %s;
'''
        mkdirp(prefix.lib64)
        mkdirp('%s/garply' % prefix.include)
        mkdirp('%s/garply' % self.stage.source_path)
        with open('%s/garply_version.h' % self.stage.source_path, 'w')  as f:
            f.write(garply_version_h % (self.version[0], self.version[1:]))
        with open('%s/garply/garply.h' % self.stage.source_path, 'w') as f:
            f.write(garply_h)
        with open('%s/garply/garply.cc' % self.stage.source_path, 'w') as f:
            f.write(garply_cc % prefix.config)
        with open('%s/garply/garplinator.cc' %
                  self.stage.source_path, 'w') as f:
            f.write(garplinator_cc)
        gpp = which('/usr/bin/g++')
        gpp('-Dgarply_EXPORTS',
            '-I%s' % self.stage.source_path,
            '-O2', '-g', '-DNDEBUG', '-fPIC',
            '-o', 'garply.cc.o',
            '-c', '%s/garply/garply.cc' % self.stage.source_path)
        gpp('-Dgarply_EXPORTS',
            '-I%s' % self.stage.source_path,
            '-O2', '-g', '-DNDEBUG', '-fPIC',
            '-o', 'garplinator.cc.o',
            '-c', '%s/garply/garplinator.cc' % self.stage.source_path)
        gpp('-fPIC', '-O2', '-g', '-DNDEBUG', '-shared',
            '-Wl,-soname,libgarply.so', '-o', 'libgarply.so', 'garply.cc.o')
        gpp('-O2', '-g', '-DNDEBUG', '-rdynamic',
            'garplinator.cc.o', '-o', 'garplinator',
            '-Wl,-rpath,%s' % prefix.lib64,
            'libgarply.so')
        copy('libgarply.so', '%s/libgarply.so' % prefix.lib64)
        copy('garplinator', '%s/garplinator' % prefix.lib64)
        copy('%s/garply/garply.h' % self.stage.source_path,
             '%s/garply/garply.h' % prefix.include)
        mkdirp(prefix.bin)
        copy('garply_version.h', '%s/garply_version.h' % prefix.bin)
        os.symlink('%s/garplinator' % prefix.lib64,
                   '%s/garplinator' % prefix.bin)