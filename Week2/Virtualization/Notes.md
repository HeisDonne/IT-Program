## Virtualization Definition

Virtualization is the process of using software to create virtual versions of computers, servers, storage, or networks on a physical computer.

It allows one physical server to run multiple virtual machines (VMs), with each VM operating like a separate computer.

## Use of virtualization?
Instead of having one physical server running only one system, virtualization allows organizations to use their hardware more efficiently and run different operating systems and applications on the same physical server. 
# Virtualization

## Definition

Virtualization is the process of creating virtual computers or resources inside a physical computer. It allows one physical server to run multiple virtual machines.

## VM

A Virtual Machine (VM) is a software-based computer that runs on a physical computer through a hypervisor.

A VM can have its own:

* CPU
* RAM
* Storage
* Network interface
* Operating system

A **hypervisor** is software that creates and manages virtual machines.

### Proxmox

Proxmox VE is a virtualization platform used to manage virtual machines and containers.

It allows an administrator to:

* Create and manage VMs
* Allocate CPU and RAM
* Configure storage
* Configure networking
* Start and stop VMs
* Access VM consoles

### VM Networking

A VM has a virtual network interface. Proxmox can connect this interface to a network bridge, allowing the VM to communicate with the physical network.

### VM vs Container

A VM runs a complete operating system, while a container is a lighter isolated environment that shares the host's kernel.

### Simple Explanation

Virtualization allows one physical server to act as several separate computers. Proxmox manages those virtual computers and gives each one the resources it needs.

