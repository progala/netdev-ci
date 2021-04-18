from pathlib import Path

import yaml


def build_dev_conns(host_vars_dir="host_vars"):
    """
    Build data structure used for creating vr-xcon containers

    vr-xcon containers link virtual routers together

    This filter assumes leaf-spine topology and data models stored in spine[0-9].yml host_vars

    Link will be auto-created for each of spine interfaces containing "peer" and "peer_intf" attributes

    Ethernet1:
        ip_add: 10.1.1.0/31
        peer: leaf1
        peer_intf: Ethernet1
    Ethernet2:
        ip_add: 10.1.1.2/31
        peer: leaf2
        peer_intf: Ethernet1
    """
    host_vars_dir = Path(host_vars_dir)
    dev_conns = []

    for host_file in host_vars_dir.glob("spine[0-9].yml"):
        with host_file.open() as fin:
            host_vars = yaml.safe_load(fin)

        our_name = host_vars["hostname"]
        for ifname, ifdata in host_vars["interfaces"].items():
            if "peer" in ifdata and "peer_intf" in ifdata:
                our_if_no = int(ifname.replace("Ethernet", "")) + 1
                peer = ifdata["peer"]
                peer_if_no = int(ifdata["peer_intf"].replace("Ethernet", "")) + 1
                conn_name = "vr-xcon-{}_{}--{}_{}".format(
                    our_name, our_if_no, peer, peer_if_no
                )
                conn_cmd = "--p2p {}/{}--{}/{}".format(
                    our_name, our_if_no, peer, peer_if_no
                )
                conn_links = [our_name, peer]
                dev_conns.append(
                    {"name": conn_name, "command": conn_cmd, "links": conn_links}
                )

    return dev_conns


class FilterModule(object):
    def filters(self):
        return {"build_dev_conns": build_dev_conns}
