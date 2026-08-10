# Linux Notes

## Objective

To understand the Linux operating system, navigate its file system, manage files and directories, and work with permissions using the command line.

## What is Linux?

Linux is an open-source operating system that manages a computer's hardware and software resources. It allows users to interact with the system through both a graphical interface and the command line (terminal). Linux is widely used for servers, cloud computing, software development, cybersecurity, networking, and embedded systems because of its stability, security, and flexibility.

## Why is Linux Important?

Linux is one of the most widely used operating systems in the IT industry. It powers web servers, cloud platforms, networking devices, supercomputers, and many developer environments. Learning Linux is important because many IT tasks are performed through the command line, making automation and system administration more efficient.


## Key Concepts

### Terminal

The terminal is a command-line interface that allows users to interact directly with the operating system by typing commands.

### Working Directory

The current location in the file system where commands are executed.

### File

A file stores data such as text, images, programs, or configuration information.

### Directory

A directory (folder) is used to organize files and other directories.

### Absolute Path

A path that starts from the root directory (`/`) and specifies the complete location of a file or directory.

Example:

```
/home/donel/Intern/Week1
```

### Relative Path

A path that is based on the current working directory.

Example:

```
Week1/Linux
```

### Hidden Files

Files or directories whose names begin with a period (`.`). These are commonly used for configuration files.

Example:

```
.ssh
.bashrc
```

### File Permissions

Linux controls access to files and directories using three permissions:

- Read (r) – View the contents of a file.
- Write (w) – Modify the contents of a file.
- Execute (x) – Run a file as a program or allow entering a directory.

Permissions are assigned separately to:

- Owner (u)
- Group (g)
- Others (o)

## Common Linux Commands

| pwd | Display the current working directory. |
| ls | List files and directories. |
| ls -la | List all files, including hidden files, with detailed information. |
| cd | Change the current directory. |
| mkdir | Create a new directory. |
| touch | Create a new empty file. |
| rm | Delete a file. |
| rm -r | Delete a directory and its contents. |
| mv | Move or rename files and directories. |
| cat | Display the contents of a file. |
| chmod | Change file permissions. |


## Real-World Application

Linux is widely used by system administrators, software developers, DevOps engineers, cloud engineers, cybersecurity professionals, and network engineers. Daily tasks such as managing servers, configuring services, writing automation scripts, troubleshooting systems, and deploying applications are commonly performed through the Linux terminal.

## What I Learned

During this week, I learned how to navigate the Linux file system, create and organize files and directories, rename and delete files, understand absolute and relative paths, and manage file permissions using `chmod`. I also learned the difference between files and directories, the purpose of hidden files such as `.ssh`, and why permissions are important for system security.


