# Week 5 — Backend (Flask, Project Structure, Password Hashing, JWT)

Documentation and test collection for the Week 5 SIWES mini project: an Authentication API with Register, Login, and a JWT-protected route.

## Prerequisites
- Python 3.11+ (built and tested on Python 3.14)
- PostgreSQL, reachable either locally or through an SSH tunnel to a remote host
- `pip` and `venv` available on the machine running the app

## Reading order
The four topic notes are self-contained reference material — read them in this order if new to the material, or jump to whichever you need a refresher on:

1. **Flask** — the framework itself: routing, request/response handling, running the dev server
2. **Project Structure** — organizing a Flask app across multiple files as it grows (app factory, blueprints)
3. **Password Hashing** — bcrypt, salting, why general-purpose hashes aren't suitable for passwords
4. **JWT** — token-based authentication, protecting routes, revocation (logout)

**Authentication API** is the applied case study — the actual build, in order, including every real error hit during setup and how it was fixed. Read this after the four topic notes, or use it standalone as a build log.

## Files in this set
```
Flask/note.md
Project Structure/note.md
Password Hashing/note.md
JWT/note.md
Authentication API/note.md
Authentication-API.postman_collection.json
```

## Testing
Import `Authentication-API.postman_collection.json` into Postman. It covers:
- Register (success, duplicate email, missing fields, weak password, empty body)
- Login (success, wrong password, unknown email)
- Protected route access (valid token, no token, invalid token)

The Login request automatically saves its `access_token` into a collection variable, used by the Profile requests that follow it — run requests top to bottom on a fresh collection run.
