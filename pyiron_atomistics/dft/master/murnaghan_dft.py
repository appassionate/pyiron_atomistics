# coding: utf-8
# Copyright (c) Max-Planck-Institut für Eisenforschung GmbH - Computational Materials Design (CM) Department
# Distributed under the terms of "New BSD License", see the LICENSE file.

from __future__ import print_function
from pyiron_atomistics.atomistics.master.murnaghan import Murnaghan, DebyeModel
from pyiron_base import deprecate

__author__ = "Joerg Neugebauer, Jan Janssen"
__copyright__ = (
    "Copyright 2021, Max-Planck-Institut für Eisenforschung GmbH - "
    "Computational Materials Design (CM) Department"
)
__version__ = "1.0"
__maintainer__ = "Jan Janssen"
__email__ = "janssen@mpie.de"
__status__ = "production"
__date__ = "Sep 1, 2017"


class MurnaghanDFT(Murnaghan):
    @deprecate("use standard Murnaghan instead")
    def __init__(self, project, job_name="murnaghan"):
        super(MurnaghanDFT, self).__init__(project, job_name)

        self.__version__ = "0.3.0"

    def set_kpoints(
        self,
        mesh=None,
        scheme="MP",
        center_shift=None,
        symmetry_reduction=True,
        manual_kpoints=None,
        weights=None,
        reciprocal=True,
    ):
        if self.ref_job:
            self._ref_job.set_kpoints(
                mesh=mesh,
                scheme=scheme,
                center_shift=center_shift,
                symmetry_reduction=symmetry_reduction,
                manual_kpoints=manual_kpoints,
                weights=weights,
                reciprocal=reciprocal,
            )

    def set_encut(self, encut):
        if self.ref_job:
            self._ref_job.set_encut(encut)

    def get_encut(self):
        if self.ref_job:
            return self._ref_job.get_encut()
        else:
            return None

    def _get_structure(self, frame=-1, wrap_atoms=True):
        # base class makes sure we only get called when self.structure is set already
        snapshot = self.structure.copy()
        old_vol = snapshot.get_volume()
        new_vol = self["output/equilibrium_volume"]
        k = (new_vol / old_vol) ** (1.0 / 3.0)
        new_cell = snapshot.cell * k
        snapshot.set_cell(new_cell, scale_atoms=True)
        if wrap_atoms:
            snapshot.center_coordinates_in_unit_cell()
        return snapshot
