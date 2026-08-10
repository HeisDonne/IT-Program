# Git Lab

## Objective
Create a Git repository, track changes, commit them, and push the repository to GitHUb. 
## Environment

OS:
Ubuntu

Git Version:
2.53.0

## Commands Used
| Command
git --version
git init
git status
git add .
git commit -m "message"
git log --oneline
git branch
git remote -v
git remote add origin 
git remote set-url origin git@github.com:HeisDonne/IT-Program.git
git push -u origin main
git push



## Procedure

1. Navigated to the Week1 project directory using the terminal.

2. Initialized a new Git repository.

3. Checked the repository status to confirm it was initialized correctly.

4. Added the project files to the staging area.

5. Created the first commit with an appropriate commit message.

6. Connected the local repository to the GitHub remote repository.

7. Verified the configured remote repository.

8. Changed the remote URL from HTTPS to SSH after configuring SSH authentication.

9. Pushed the repository to GitHub.

10. Verified that the repository and commits appeared on GitHub successfully.

## Result
Successfully created a local Git repository, tracked project files, committed changes, configured GitHub as the remote repository, and pushed the project using SSH authentication.

## Challenges Encountered
Authentication failed when pushing with HTTPS.

## How I Solved Them
I set up SSH instead. changed the remote repository URL from HTTPS to SSH
## Lessons Learned
I learned the complete Git workflow from initializing a repository to pushing changes to GitHub. I also learned the difference between local repositories and remote repositories and why SSH is preferred for authentication.
 
