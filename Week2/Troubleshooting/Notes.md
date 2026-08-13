# Troubleshooting Methodology

## Definition

Troubleshooting is the systematic process of identifying, investigating, and fixing problems in a system, application, network, or service.

## Troubleshooting Process

A simple troubleshooting process I learned is:

### 1. Identify the Problem

First, determine exactly what is not working.

For example:

> The Nginx webpage is not loading.

### 2. Check the System

Check the relevant components to determine where the problem may be.

For Docker, useful commands include:

```
docker ps
```

This checks whether the container is running.

```
docker ps -a
```

This shows all containers, including stopped ones.

### 3. Find the Cause

Look for evidence that can explain the problem.

For example:

```
docker logs IT-nginx
```

This can show errors or requests handled by the container.

```
curl -I http://localhost:8080
```

This checks whether the web server is responding.

### 4. Apply a Fix

Once the cause has been identified, make the appropriate change.

### 5. Test Again

After making the change, test the system again to confirm that the problem has been resolved.

## NB

I learned that troubleshooting should be systematic rather than based on randomly changing settings. Checking the system, collecting evidence, identifying the cause, applying a fix, and testing the result makes troubleshooting more effective.
