# Logs

## Definition

A log is a record of events, activities, requests, or errors produced by a system, application, or service.

## NB

Logs help administrators understand what a system is doing and can be used to find problems when something goes wrong.

For example, if a web server stops working, its logs may show an error that helps identify the cause.

### Docker Logs

Docker can display the logs produced by a container.

```
docker logs week2-nginx
```

This displays the logs from my Nginx container.

### Example

I found successful requests such as:

```text
"GET / HTTP/1.1" 200 896
```

This means:

* `GET /` — the client requested the homepage
* `HTTP/1.1` — HTTP version
* `200` — request was successful
* `896` — size of the response

### Simple Explanation

Logs are like a history of what happened inside a system. They are useful for monitoring and troubleshooting.
