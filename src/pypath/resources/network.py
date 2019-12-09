#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#  This file is part of the `pypath` python module
#  (Planned for) centrally handling cache for all databases/resources.
#
#  Copyright
#  2014-2019
#  EMBL, EMBL-EBI, Uniklinik RWTH Aachen, Heidelberg University
#
#  File author(s): Dénes Türei (turei.denes@gmail.com)
#                  Nicolàs Palacio
#                  Olga Ivanova
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  Website: http://pypath.omnipathdb.org/
#

from future.utils import iteritems

import pypath.resource as resource
import pypath.data_formats as data_formats


_data_models = {
    'interaction': 'interaction',
    'interaction_misc': 'interaction',
    'interaction_htp': 'interaction',
    'ligand_receptor': 'activity_flow',
    'pathway': 'activity_flow',
    'pathway_all': 'activity_flow',
    'pathway_noref': 'activity_flow',
    'activity_flow': 'activity_flow',
    'dorothea': 'activity_flow',
    'transcription': 'activity_flow',
    'transcription_dorothea': 'activity_flow',
    'transcription_onebyone': 'activity_flow',
    'tfregulons': 'activity_flow',
    'mirna_target': 'activity_flow',
    'lncrna_target': 'activity_flow',
    'tf_mirna': 'activity_flow',
    'enzyme_substrate': 'enzyme_substrate',
    'ptm': 'enzyme_substrate',
    'ptm_all': 'enzyme_substrate',
    'ptm_misc': 'enzyme_substrate',
    'ptm_noref': 'enzyme_substrate',
    'reaction': 'process_description',
    'reaction_misc': 'process_description',
    'reaction_pc': 'process_description',
}


def _readsettings_to_networkresource(readsettings, data_model = None):
    
    return resource.NetworkResource(
        name = readsettings.name,
        interaction_type = readsettings.interaction_type,
        readsettings = readsettings,
        data_model = data_model,
    )


for resource_set_label in dir(data_formats):
    
    resource_set = getattr(data_formats, resource_set_label)
    
    if not isinstance(resource_set, dict):
        
        continue
    
    new_resource_set = {}
    
    for resource_label, input_def in iteritems(resource_set):
        
        if not isinstance(input_def, data_formats.input_formats.ReadSettings):
            
            continue
        
        data_model = (
            input_def.data_model or
            (
                _data_models[resource_set_label]
                    if resource_set_label in _data_models else
                'unknown'
            )
        )
        
        new_resource_set[resource_label] = _readsettings_to_networkresource(
            readsettings = input_def,
            data_model = data_model,
        )
    
    if new_resource_set:
        
        globals()[resource_set_label] = new_resource_set
