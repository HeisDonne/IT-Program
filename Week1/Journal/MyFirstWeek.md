# My First Week - Linux & Git

Today being 13th August 2026, I started my SIWES training.

At first, Linux felt strange because I was used to clicking around with a mouse even though i had linux installed on my pc. Navigating directories through the terminal was confusing, especially understanding that folders can contain other folders and files.

One thing that really stood out to me was Linux permissions. Initially, I thought removing write permission would completely stop a file from being edited, but after experimenting, I discovered that GUI editors can sometimes replace a file instead of modifying it directly. That led me to learn the difference between file permissions, directory permissions, and even immutable files using `chattr`.

I also learned that on (Tuesday) the 14th when i started with Git, that  Git isn't just a backup tool—it's a way of recording the history of a project. Understanding the flow from Working Directory → Staging Area → Repository made Git much easier to understand.

# - SSH and Networking Fundamentals (Wednesday)

Today, I learned about SSH (Secure Shell) and how it is used to securely connect and communicate with another computer over a network. I learned that SSH uses encryption and authentication methods to verify users and protect communication between a client and a server.

I practiced generating SSH key pairs using ssh-keygen, which created a private key and a public key. I learned that the private key stays on my computer and should not be shared, while the public key can be shared with services like GitHub for authentication.

I also practiced connecting GitHub using SSH authentication and changed my Git repository connection from HTTPS to SSH using Git commands.

I also learned networking fundamentals, including IP addresses, DNS, routing, and client-server communication. I learned that an IP address identifies a device on a network, while DNS translates domain names into IP addresses so computers can locate servers.

I practiced using networking commands such as:

whoami — to check the current user
hostname — to check my computer name
hostname -I — to view my IP address
ip addr — to view network interfaces and IP addresses
ping — to test communication with another device/server
ip route — to view routing information and understand how packets are sent

SSH is like a secure way that allows me to access another computer remotely. The server checks my identity using authentication methods before allowing access.

Networking is how computers communicate with each other. My computer uses DNS to find the IP address of a server, then uses routing to decide where to send packets. If the destination is outside my local network, the packet is sent through the router before reaching the server.


Things I learned this week:
- Linux file navigation
- File and directory management
- File permissions (`chmod`)
- Ownership (`chown`, `chgrp`)
- Searching with `find` and `grep`
- Installing software with `apt`
- Git basics
- Commits
- Branches
