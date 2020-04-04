# GitHub Actions for creating a batch of devices within projects on Packet.com

## Automate your infrastructure

This GitHub Action will create a new device batch in an existing project on [packet.com](https://packet.com). Devices are compute resources available within your organization projects.

# Creating devices

With this action you can automate your workflow to by provisioning multiple devices inside of projects using the [packet.com api](https://api.packet.net).

To use this action you will first need an [authentication token](https://www.packet.com/developers/api/authentication/) which can be generated through the [Packet Portal](https://app.packet.net/login?redirect=%2F%3F__woopraid%3DjUPDKi0tqtym).

You will also need a public/private key pair. [Learn how to generate keys](https://www.packet.com/developers/docs/servers/key-features/ssh-keys/) for either a user or a project.

**NEVER share your private key with anyone!**

**Packet.com is NOT a free service, so you will be asked to provide billing information. This action will NOT have access to that information.**

## Sample workflow that uses the packet-create-project action

```yaml
# File: .github/workflows/workflow.yml

on: [push]

name: Packet Project Sample

jobs:
  create-new-device:
    runs-on: ubuntu-latest
    name: Creating new device in existing packet project
    steps:
      - uses: mattdavis0351/packet-create-device-batch@v1
        with:
          API_key: ${{ secrets.PACKET_API_KEY }}
          project_name: my-project
          host_names: "Host-1, Host-2, Host-3"
          plan: "t3.small.x86"
          facility: "sjc1"
          operating_system: "ubuntu_19_04"
          quantity: 3
          spot_instance: true
          spot_price_max: .50
          user_ssh_keys: ${{ secrets.PACKET_PUBLIC_KEY }}
```

## Available Inputs

| Input              | Description                                                                                                                       | Default Value       | Required           |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------- | ------------------- | ------------------ |
| `API_key`          | Packet.com API authorization token                                                                                                | No key supplied     | :white_check_mark: |
| `project_name`     | Desired name for new project                                                                                                      | default             | :white_check_mark: |
| `host_names`       | Desired host names for new device. If specifying more than one device us a comma separated list.                                  | GitHub Actions Host | :white_check_mark: |
| `plan`             | Desired server type for device                                                                                                    | default             | :white_check_mark: |
| `facility`         | Geographical location for device                                                                                                  | default             | :white_check_mark: |
| `operating_system` | Desired operating system for device                                                                                               | default             | :white_check_mark: |
| `quantity`         | Number of desired devices in the batch. **if you specify more than one host name this number must match the amount of hostnames** | 1                   | :x:                |
| `spot_instance`    | Create devices as spot instances                                                                                                  | false               | :x:                |
| `spot_price_max`   | Maximum bid for spot instances                                                                                                    | 1                   | :x:                |
| `user_ssh_keys`    | SSH keys for any user account you wish to add to device                                                                           |                     | :x:                |
| `project_ssh_keys` | Project level SSH keys for device                                                                                                 |                     | :x:                |

## Outputs from action

This action does not supply any outputs
