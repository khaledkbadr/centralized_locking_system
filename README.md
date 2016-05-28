# Centralized Locking System
REST Centralized Locking System for distributed systems that provide

## Requirements

1. 100% guarantee of exclusive access. If 2 separate system managed to get access to the same resource, an unrecoverable corruption might occur. (Done)

2. If an exclusive access is granted to one of the services, and the service crashed or died without releasing the locks, the locking system must free the lock on that resource  (eventually), so other services doesn’t get blocked forever.

3. Support timeout, if a service can’t get an exclusive lock to a resource after the given timeout. (Done)

4. Detect deadlocks. [Optional]

5. resource is defined by it’s name. This name is used as a key to acquire the locking. (Done)


## Endpoints Specs

#### /resource/access (POST)

Accepts 2 params `id` and `resource` to ask for permission to lock that resource.

Responds with either a `success` or `timeout`

#### /resource/release (POST)

Accepts 2 params `id` and `resource` to release the resource.

Responds with either a `success` or `failure` if the caller was not locking the resource.

