#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: ucs_service_profile_info
short_description: Returns facts about the service profiles in UCS
description:
- Returns facts about the service profiles in UCS.
- Examples can be used with the UCS Platform Emulator U(https://communities.cisco.com/ucspe).
extends_documentation_fragment: ucs
options:
  name:
    description:
    - 
'''

EXAMPLES = r'''
#
'''

RETURN = r'''
#
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.remote_management.ucs import UCSModule, ucs_argument_spec


def main():
    argument_spec = ucs_argument_spec
    argument_spec.update(
        org_dn=dict(type='str', default='org-root'),
        name=dict(type='str', required=False),
    )

    module = AnsibleModule(
        argument_spec,
        supports_check_mode=True,
    )
    ucs = UCSModule(module)

    server_profiles = ucs.login_handle.query_classid("LsServer")

    spDict = dict()

    for server_profile in server_profiles:
        spDict[server_profile.name] = server_profile.__json__()
        sp_dn_filter = '(dn, "^' + server_profile.dn + '/")'
        vnics = ucs.login_handle.query_classid(class_id="VnicEther", filter_str=sp_dn_filter)
        vnicDict = dict()
        for vnic in vnics:
            vnicDict[vnic.name] = vnic.__json__()
        spDict[server_profile.name]["vnics"] = vnicDict


    ucs.result['changed'] = False
    ucs.result['ansible_facts'] = dict(ucs_sp=spDict)

    module.exit_json(**ucs.result)

if __name__ == '__main__':
    main()
