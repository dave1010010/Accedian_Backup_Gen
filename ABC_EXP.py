import json

FILENAME = "backup.conf"


def load_data(delimeter="=") -> dict[str, dict]:

    data = {}
    section = None

    with open(FILENAME, "r") as file:
        for line in file:
            line.strip()
            # filters the file names and adds to the data dictionary
            if line.startswith("#_***_"):
                index = line.split("#_***_")
                section = index[-1].strip()
                data[section] = {}
                continue

            if line.startswith("["):
                sub_section = line.strip()
                sub_section_filtered = sub_section.replace("[", "")
                new_sub_section = sub_section_filtered.replace("]", "")
                data[section][new_sub_section] = {}
                continue

            if section and delimeter in line:
                key, value = line.split(delimeter, 1)
                data[section][new_sub_section][key.strip()] = value.strip()

    return data


def parse_data(data:dict) -> dict[str, dict]:
    """
    Reads in and parses data: Dict into separate dictionaries based on each defined category.

    Args: data (dict)
    Parsed configuration data.

    Returns: dict
    Filtered data containing only the selected categories and their
    associated nested dictionaries.
    """
    vid_sets = {}
    port_inst = {}
    bandwidths_profiles = {}

    for key, value in data.items():
        vid_sets = {
            key: value
            for key, value in data.items()
                for k, v in value.items()
                    if k.startswith("vid_set_")
        }

    for key, value in data.items():
        port_inst = {
            key: value
            for key, value in data.items()
            for k, v in value.items()
                if k.startswith("port_inst")
        }

    for key, value in data.items():
        bandwidths_profiles = {
            key: value
            for key, value in data.items()
            for k, v in value.items()
                if k.startswith("bwp_")
        }

    return vid_sets, port_inst, bandwidths_profiles


def filter_data(vids:dict[str, dict], ports:dict[str,dict], bandwidths:dict[str,dict]):
    """
    Extract and normalize VLAN, port, and bandwidth configuration data.

    Arg: vids (dict):
    Dictionary containing VLAN service definitions and associated
    VLAN IDs.

    Arg: ports (dict):
    Dictionary containing port configuration objects such as
    port instances, administrative state, MTU, port index, and
    interface names.

    Arg: bandwidths (dict):
    Dictionary containing bandwidth profile objects including CIR,
    EIR, CBS, EBS, and related rate-limiting parameters.

    Returns: Dict
    """
    filtered_vid_sets = {}
    filtered_ports = {}
    filtered_bandwidths = {}

    # Vid Sets
    for key, value in vids.items():
        for k,v in value.items():
            if k.startswith("vid_set_"):
                filtered_vid_sets[k] = {
                    "name": v['pvs_name'],
                    "port": v['pvs_card'],
                    "policy_list": v['pvs_policy_list'],
                    "pvs_vids": v['pvs_vids'],
                    "pvs_vlan_type": v['pvs_vlan_type'],
                    "pvs_outer_vid": v['pvs_outer_vid'],
                    "pvs-outer_vlan_type": v['pvs_outer_vlan_type'],
                }

    # Ports
    for key, value in ports.items():
        for k,v in value.items():
            if k.startswith("port_inst"):
                filtered_ports[k] = {
                    "name": v['cfg_name'],
                    "default_name": v['cfg_default_name'],
                    "enabled": v['cfg_enable'],
                    "index": v['cfg_port_idx'],
                    "mtu": v['cfg_mtu']
                }

            if k.startswith("port_nego"):
                pass

    # Bandwidth
    for key, value in bandwidths.items():
        for k,v in value.items():
            if k.startswith("bwp_"):
                filtered_bandwidths[k] = {
                    "name": v['cfg_name'],
                    "cir": v['cfg_cir'],
                    "cir_max": v['cfg_cir_max'],
                    "cfg_cbs": v['cfg_cbs'],
                    "cfg_eir": v['cfg_eir'],
                    "cfg_eir_max": v['cfg_eir_max'],
                    "cfg_ebs": v['cfg_ebs'],
                }

    print(filtered_vid_sets)
    print(filtered_ports)
    print(filtered_bandwidths)

if __name__ == '__main__':
    data = (load_data())
    vids, ports, bandwidth = parse_data(data)
    filter_data(vids, ports, bandwidth)