""" pbsdump.py extracts data from XML formatted pbsdump command """

import re
import tools
import xml.etree.ElementTree as pbsXml

GET_NODE_ID = re.compile('\D+(\d+)')
IS_BYTE_SIZE = re.compile('^(\d+)(\D+)$')

def parse(fname):
    """ Load the content of a pbsdump xml file

    Args:
    fname: dump file name

    Returns:
    A dictionnary with node names as key and as value a dictionnary with
    node selected data (not everything is kept from the file).

    """

    tree = pbsXml.parse(fname)

    if not tree:
        tools.error('failed to parse pbsdump xml file ' + fname)
        return 0

    root = tree.getroot()

    nodes = dict() # Hold list of nodes

    # Iterate on all Node items
    for child in root.findall('Node'):
        # Get node name
        name = child.find('name').text

        # Build new entry for the given node
        nodes[name] = dict()
        node = nodes[name]
        matches = GET_NODE_ID.match(name)
        node[id] = int(matches.group(1))

        # Collect data
        node['name'] = name
        node['np'] = int(child.find('np').text)
        node['state'] = child.find('state').text
        node['power_state'] = child.find('power_state').text
        data = child.find('jobs')
        if data is not None:
            node['jobs'] = data.text
        else:
            node['jobs'] = None

        node['nb_sockets'] = child.find('total_sockets').text
        node['nb_numa_nodes'] = child.find('total_numa_nodes').text
        props = child.find('properties').text
        node['properties'] = props.split(',')

        # Get the status entries
        node['status'] = dict()
        data = child.find('status')
        if data is None:
            tools.error('Node ' + name + " has no status entry! Skipped.")
            continue

        status = data.text
        status_list = status.split(',')
        for entry in status_list:
            data = entry.split('=')
            matches = IS_BYTE_SIZE.match(data[1])
            if matches:
                # Convert whatever size in GB
                data[1] = tools.size_convert(matches.group(1), matches.group(2), 'gb')

            # Keep the data
            node['status'][data[0]] = data[1]

    return nodes

def filter_nodes(nodes, filters):
    """ Filter a nodes list and return the resulting list

    Args:
    nodes: dictionnary with the nodes (obtained from parse function)
    filters: dictionnary with filters

    Returns:
    A dictionnary with node names as key and as value a dictionnary with node data.

    Filters:
    'one-of-props': array with a list of properties that the node must include, OR operator
    'mandatory-props': array with a list of properties that the node must include, AND operator
    'exclude-props': array with a list of properties that the node cannot have, AND operator
    'mandatory-states': array with a list of states that the node must include, AND operator
    'exclude-states': array with a list of states that the node cannot have, AND operator

    """

    # print("Filtering nodes...")

    kept_nodes = dict() # New list of filtered nodes

    for node_name in nodes:
        # print("Checking node " + node_name)
        node = nodes[node_name]
        keep = True # Keep the node by default

        # Filter on properties
        # ----------------------------------------------
        if 'one-of-props' in filters:
            keep = False
            for prop in node['properties']:
                for check in filters['one-of-props']:
                    if prop == check:
                        keep = True
                        break
                if keep == True:
                    break # Stop here if node kept

            if not keep:
                continue # Move to next node

        if 'mandatory-props' in filters:
            keep = False
            for check in filters['mandatory-props']:
                for prop in node['properties']:
                    if prop == check:
                        keep = True
                        break

                if not keep:
                    break # Stop here if node kept

            if not keep:
                continue # Move to next node

        if 'exclude-props' in filters:
            for check in filters['exclude-props']:
                for prop in node['properties']:
                    if prop == check:
                        keep = False
                        break

                if not keep:
                    break # Stop here if node kept

            if not keep:
                continue # Move to next node

        # Filter on state
        # ----------------------------------------------
        if 'mandatory-states' in filters:
            keep = False
            for check in filters['mandatory-states']:
                if node['state'] == check:
                    keep = True
                    break

            if not keep:
                continue # Move to next node

        if 'exclude-states' in filters:
            for check in filters['exclude-states']:
                if node['state'] == check:
                    keep = False
                    break

            if not keep:
                continue # Move to next node

        # print("Keeping ", node_name)

        kept_nodes[node_name] = node

    return kept_nodes
