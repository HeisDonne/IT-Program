# JWT

## Definition
JWT (JSON Web Token) is a compact, self-contained string used to prove a user's identity on each request, without the server needing to store anything about active sessions. It solves the problem created by HTTP being **stateless** — by default, every request is treated as if the server has never seen the client before, so some proof of identity needs to travel with every single request.

## The alternative it replaces: server-side sessions
The traditional approach stores a list of "who's currently logged in" on the server (in memory or a database), and gives the client a cookie containing just an ID pointing into that list. This works, but requires the server to maintain and look up that list on every request. JWT's approach avoids that storage entirely — the proof of identity is carried inside the token itself.

## Structure of a JWT
A JWT is three base64-encoded segments joined by dots:
```
eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIzIn0.4f8a9c...
   header          .    payload      .  signature
```
| Segment | Contains |
|---|---|
| Header | Token type and the signing algorithm used |
| Payload | The claims — data about the token, e.g. `sub` (subject/identity), `exp` (expiry timestamp), `jti` (a unique ID for this specific token) |
| Signature | A cryptographic signature over the header + payload, generated using a secret key known only to the server |

**Important distinction:** the payload is *encoded*, not *encrypted* — anyone can decode and read it (it's just base64). What can't be faked is the signature: changing anything in the payload invalidates the signature unless you also have the secret key to regenerate it correctly. Never place sensitive data (passwords, etc.) inside the payload.

## Installing and configuring

```bash
pip install flask-jwt-extended
```
```python
from flask_jwt_extended import JWTManager
jwt = JWTManager(app)   # or jwt.init_app(app), see Project Structure
```
```python
app.config["JWT_SECRET_KEY"] = "a-long-random-secret"
```
- `JWT_SECRET_KEY` — the key used to sign and verify tokens. Should be a long random value (32+ bytes recommended for the default signing algorithm), and should come from an environment variable in any real deployment, never hardcoded.

## Issuing a token (on login)

```python
from flask_jwt_extended import create_access_token
access_token = create_access_token(identity=str(user_id))
```
- `identity=...` — the value baked into the token's `sub` claim. **Must be a string** in current versions of `flask-jwt-extended` — passing a raw integer raises `"Subject must be a string"` when the token is later decoded.
- The returned `access_token` is the full three-part signed string, sent back to the client (typically in the login response body).

## Protecting a route

```python
from flask_jwt_extended import jwt_required, get_jwt_identity

@app.route("/resource", methods=["GET"])
@jwt_required()
def protected_route():
    user_id = get_jwt_identity()
    ...
```
- `@jwt_required()` — runs *before* the route function body, on every request to this route. Checks, in order: an `Authorization` header is present, its signature is valid against `JWT_SECRET_KEY`, and it hasn't expired. If any check fails, the request is rejected with `401` and the route function never executes.
- `get_jwt_identity()` — once past the check above, returns the `sub` value from the token's payload — here, the string identity that was set at login. If your identity is a numeric ID stored as a string, cast it back: `int(get_jwt_identity())`.

## Reading the full payload

```python
from flask_jwt_extended import get_jwt
claims = get_jwt()
token_id = claims["jti"]
```
- `get_jwt()` — returns the entire decoded payload dict, not just the identity. Needed for claims like `jti` (unique per-token ID) or any custom claims added at token creation.

## Logout / revocation
JWTs cannot be individually "deleted" from the client side by the server by default — they remain valid until they expire, since validity is proven purely by signature, not by a server-side lookup. Implementing logout requires explicitly tracking revoked tokens:

```python
BLOCKLIST = set()

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST

@app.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    BLOCKLIST.add(jti)
    return {"message": "logged out"}, 200
```
- `@jwt.token_in_blocklist_loader` — registers a callback run on every protected request, after the normal signature/expiry checks. Returning `True` rejects the request even for an otherwise-valid token.
- An **in-memory `set()`** is the simplest possible blocklist — sufficient for learning and single-process development, but resets on every restart and isn't shared across multiple worker processes. A production system would use a shared store (Redis, or a database table) instead.

## Common pitfalls
| Symptom | Cause |
|---|---|
| `"Subject must be a string"` | Passed a non-string (e.g. an integer ID) to `identity=` in `create_access_token` |
| `InsecureKeyLengthWarning` | `JWT_SECRET_KEY` is shorter than the recommended 32 bytes for the signing algorithm |
| A token that "should" work still fails after a code fix | Old tokens were signed/issued *before* the fix — a JWT is a fixed string once issued; changing server code doesn't retroactively alter tokens already handed out. Log in again to get a freshly issued token |


