import packet
import os

# Collect input variables from workflow
API_key = os.getenv("INPUT_API_KEY") or "No key supplied"
group_names_list = os.getenv("INPUT_GROUP_NAMES") or "misc"
project_name = os.getenv("INPUT_PROJECT_NAME") or "default"

# Check if required inputs have been received
if API_key == "No key supplied":
    raise ValueError(
        f"Cannot supply empty API key. Current key is: %s" % API_key)

if project_name == "default":
    raise ValueError("Must supply an existing project ID for this device")


# Create Packet.com API client
manager = packet.Manager(auth_token=API_key)

# Store project_id for later API call
project_id = ""

# Check for valid project name
projects = manager.list_projects()

for p in projects:
    if p.name == project_name:
        project_id = p.id
    else:
        raise ValueError(
            "Supplied project name does not match any valid projects for this API key")

# Get batch information for later parsing
batch_id = ''
batch_dev_ids = []
project_batches = manager.list_batches(project_id)

# Parse hostnames
group_arr = group_names_list.split(',')
group_names = []
for group in group_arr:
    group_names.append(group.strip().replace(' ', '-'))

# Prepare the writable object with supplied group names
groups = {}

for gname in group_names:
    groups[gname] = []

# Open the inventory file for writing
f = open("hosts", "w+")

# Get devices for project and add them to respective group names
# Desired group names is a part of the host name
# group name: master  host name: k8s-master
# group name: bread  host name: bread-crumb-host
dev = manager.list_devices(project_id)
for d in dev:
    for b in project_batches:
        for ref in b.devices:
            if "/devices/"+d.id == ref['href']:
                serv = manager.get_device(d.id)
                ip_addrs = serv.ip_addresses
                for addr in ip_addrs:
                    if addr["address_family"] == 4:
                        for n in group_names:
                            if n in d.hostname.lower() and addr["public"] == True:
                                groups[n].append(addr['address'])
                            else:
                                groups["misc"].append(addr['address'])

# Write the created groups from the object into a file
for g in groups:
    f.write("[%s]\r" % g)
    for members in groups[g]:
        f.write("%s\r" % members)

# Close the inventory now that we are done with it.
f.close()

# Profit
