# Juju local

Real magic for the local provider

# Installation

`sudo pip install -U jujulocal`

# Usage

Not all features have been created. This is both a README and Roadmap

## `juju local images [--update]`

Show current cached cloud image

* `--update` - update the cloud images currently cached

## `juju local templates [--upgrade] [--rebuild] <series>`

Show current LXC templates

* `--upgrade` - launch the template and run a dist-upgrade
* `--rebuild` - rebuild series template

## juju local remove

## `juju local debug`

Local provider not working? Run this to validate and troubleshoot common issues

## `juju local btrfs [--enable] [--disable]`

Shows the current status of BTRFS backed LXC images

* `--enable` - Enable BTRFS backed LXC images
* `--disable` - Disable BTRFS backed LXC

## `juju local mount-charm <service> <mount-point>`

Mount the charm-dir for a service locally to allow easier access

* `service` - Deployed service to mount
* `mount-point` - Where to mount the service's CHARM_DIR

## `juju local encrypted-home`

Enable work-arounds for users with encrypted-home drives

## `juju local suspend`

Suspend a local deployment

## `juju local resume`

Resume a previously suspended deployment

# Hacking

```
make
make coverage
```
