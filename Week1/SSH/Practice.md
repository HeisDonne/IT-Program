# SSH Lab

## Objective

Generate an SSH key pair, configure GitHub authentication, and securely connect Git to GitHub using SSH.


## Environment

Operating System:
Ubuntu Linux


## Commands Used

ls -la ~/.ssh

ssh-keygen -t ed25519 -C "ybdy331@gmail.com"

cat ~/.ssh/id_ed25519.pub

ssh -T git@github.com

git remote set-url origin git@github.com:HeisDonne/IT-Program.git

git push


## Procedure

1. Checked the existing SSH directory and its contents.
2. Generated a new Ed25519 SSH key pair.
3. Accepted the default storage location and configured a passphrase.
4. Displayed the public key.
5. Added the public key to the GitHub account.(In github setting).
6. Tested the SSH connection to GitHub.
7. Changed the Git remote repository from HTTPS to SSH.
8. Successfully pushed the project to GitHub using SSH authentication.

## Result

Successfully generated SSH keys, authenticated with GitHub using SSH, and configured Git to communicate securely without using passwords.


## Challenges Encountered

Git initially attempted to use HTTPS for authentication, resulting in an authentication failure.

## Solution

Updated the remote repository URL to use SSH, verified the SSH connection, and pushed the repository successfully.

## Lessons Learned

I learned how SSH authenticates users using public and private keys and how GitHub uses SSH keys to securely verify a user's identity without requiring a password.
