# SSH (Secure Shell)

## What is SSH?

SSH (Secure Shell) is a network protocol that allows a client to securely connect and communicate with another computer over a network.

It is mainly used by system administrators and IT engineers to remotely manage Linux servers and virtual machines.


## Why is SSH Used?

SSH is used because it provides a secure way to access another computer remotely. Instead of being physically present at the server, an administrator can log in from anywhere and perform tasks such as installing software, editing files, checking logs, and troubleshooting problems.


## How SSH Works

1. The client starts an SSH connection to the server.
2. The server identifies itself using its host key.
3. The client checks the server's identity.
4. The server asks the client to authenticate.
5. Authentication is completed using a password or SSH key.
6. A secure encrypted connection is established.
7. The client can now execute commands on the remote machine.

## Authentication Methods

### Password Authentication

The user enters their Linux account password. The server verifies the password before allowing access.

### SSH Key Authentication

SSH uses a pair of keys:

* **Private Key** – Stored securely on the client's computer and never shared.
* **Public Key** – Stored on the server in the `authorized_keys` file.

When connecting, the server verifies that the client owns the matching private key before granting access.

## Difference Between SSH and HTTP

| SSH                                                  | HTTP                                          |
| ---------------------------------------------------- | --------------------------------------------- |
| Used to securely access and manage another computer. | Used to request and receive web content.      |
| Encrypted by default.                                | HTTP is not encrypted; HTTPS adds encryption. |
| Used by system administrators and engineers.         | Used by web browsers and websites.            |

## SSH COmmands
| ls -la ~/.ssh | View SSH directory contents |
| ssh-keygen -t ed25519 -C "email@example.com" | Generate SSH keys |
| cat ~/.ssh/id_ed25519.pub | Display the public key |
| ssh -T git@github.com | Test GitHub authentication |
| git remote set-url origin git@github.com:user/repository.git | Change Git Remote from HTTPS to SSH |
| E.g: git remote set_url origin git@github.com:HeisDonne/IT-Program.git |
| git remote -v | To check if connected |
| hostname -I | View your computer IP address |
| ssh username@ip_address | connect to another computer |
| exit | Exit an SSH session |

## What I Learned
I learned that SSH authentication uses a public and private key pair instead of passwords. I also learned how GitHub verifies my identity using my SSH key without exposing my private key.

