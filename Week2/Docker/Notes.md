# Docker

## Definition

Docker is a platform used to package and run applications in isolated environments called containers.

## NB

Docker helps applications run consistently by packaging the application and its required dependencies together.

### Important Terms

**Image:** A packaged template used to create a container.

**Container:** A running instance created from an image.

**Docker Engine:** The software that manages Docker containers.

**Docker Hub:** A registry where Docker images can be stored and downloaded.

### Image vs Container

An image is like a blueprint, while a container is the running environment created from that blueprint.

### Docker vs Virtual Machine

A VM includes a complete operating system and its own kernel.

A Docker container is lighter and shares the host's kernel.

```
VM:
Physical Server → Hypervisor → VM → Full OS

Docker:
Physical Server → Docker → Container → Application
```

### Basic Docker Commands

```
docker --version
```

Checks the installed Docker version.

```
docker ps
```

Shows running containers.

```
docker ps -a
```

Shows all containers, including stopped containers.

```
docker images
```

Shows images stored locally.

```
docker pull nginx
```

Downloads the Nginx image.

```
docker run
```

Creates and starts a container from an image.

### Simple Explanation

Docker allows me to run applications inside isolated containers without installing and configuring the application directly on the host system.

