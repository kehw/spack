# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Genfit(CMakePackage):
    """GenFit is an experiment-independent framework for track reconstruction in
        particle and nuclear physics"""

    homepage = "https://github.com/GenFit/GenFit"
    url      = "https://github.com/GenFit/GenFit/archive/master.tar.gz"
    git      = "https://github.com/GenFit/GenFit.git"

    maintainers = ['mirguest']

    version('master', branch='master')
    version('2017-06-23', commit='b496504a739382e8043c38c893d8df6eed20e560')

    depends_on('root')
    depends_on('eigen')

    conflicts('root@6.18.00:', when='@2017-06-23')
