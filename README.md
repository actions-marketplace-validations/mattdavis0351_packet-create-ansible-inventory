# GitHub Actions for generating an Ansible inventory file for a batch of devices within projects on Packet.com

## Automate your infrastructure

This GitHub Action will create a new inventory file for a device batch in an existing project on [packet.com](https://packet.com). Devices are compute resources available within your organization projects.

# Creating devices

With this action you can automate your workflow to by building an Ansible inventory file to configure the multiple devices inside of projects using the [packet.com api](https://api.packet.net).

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
      - name: Create Ansible Inventory File
        uses: mattdavis0351/packet-create-ansible-inventory@v1
        if: success()
        with:
          API_key: ${{ secrets.PACKET_API_KEY }}
          project_name: My-project-name
          group_names: "webservers, databases"
```

## Available Inputs

| Input          | Description                                                                                           | Default Value       | Required           |
| -------------- | ----------------------------------------------------------------------------------------------------- | ------------------- | ------------------ |
| `API_key`      | Packet.com API authorization token                                                                    | No key supplied     | :white_check_mark: |
| `project_name` | Existing project name you wish to add to inventory                                                    | default             | :white_check_mark: |
| `group_names`  | Desired group names for inventory file. If specifying more than one device us a comma separated list. | GitHub Actions Host | :white_check_mark: |

## Outputs from action

This action does not supply any outputs

## Notes

This action depends on the availability of your packet.com resources. If they are currently being created and this actions runs before their status becomes active you may end up with an empty inventory file. This will be addressed in future releases of this action.
