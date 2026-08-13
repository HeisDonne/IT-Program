# Docker and Nginx Practical

## Objective

The objective of this practical was to verify Docker, download an Nginx image, create an Nginx container, expose the web server through a port, test the server, and inspect its logs.

## 1. Check Docker Installation

I first checked whether Docker was installed.

```
docker --version
```
The output confirmed it was not installed, so i run:

```
sudo apt install docker.io -y
```
---

## 2. Check Docker Service

I checked whether the Docker service was running.

```
sudo systemctl status docker
```

The service was not running, so i run:

```
sudo systemctl start docker
```
And enable it at start up:

```
sudo systemctl enable docker
```

## 3. Check Docker Information

I used:

```
docker info
```

This displayed information about the Docker Engine, including the number of containers and images, storage driver, networking, and other configuration details.

---

## 4. Check Existing Containers

I checked the containers already present on the system.

```
docker ps -a
```
## 5. Check Existing Images

I checked the Docker images stored locally.

```
docker images
```
## 6. Download the Nginx Image

I downloaded the Nginx image from Docker Hub.

```
docker pull nginx
```
The image was successfully downloaded.

### What This Does

`docker pull` downloads an image from a container registry and stores it locally so that it can be used to create a container.

## 7. Create and Start the Nginx Container

I created and started the Nginx container using:

```
docker run -d -p 8080:80 --name IT-nginx nginx
```

### Explanation

* `docker run` — creates and starts a container.
* `-d` — runs the container in the background.
* `-p 8080:80` — maps port 8080 on the host to port 80 inside the container.
* `--name IT-nginx` — gives the container a name.
* `nginx` — specifies the Nginx image.

The command returned a long string of characters, which was the container ID.
## 8. Verify the Container

I checked whether the Nginx container was running.

```
docker ps
```

The `IT-nginx` container appeared as running.

The port mapping showed that:

```
Host port 8080 → Container port 80
```
## 9. Test Nginx in a Browser

I opened:

```
http://VM_IP:8080
```
While on my local pc

```
http://localhost:8080
```
The Nginx welcome page was displayed.

This confirmed that the Nginx web server was accessible through the mapped port.


## 10. Test Nginx Using curl

I also tested the web server from the terminal.

```
curl -I http://localhost:8080
```

The response included:

```
HTTP/1.1 200 OK
Server: nginx/1.31.3
Content-Type: text/html
```

This confirmed that Nginx successfully received and responded to the HTTP request
## 11. Check Container Logs

I checked the Nginx container logs using:

```
docker logs IT-nginx
```

The logs showed that Nginx started successfully and recorded requests made to the web server.

For example:

```
GET / HTTP/1.1" 200 896
```

The `200` response showed that the request for the homepage was successful.

## 12. Stop and Start the Nginx container

To stop it:
```
sudo docker stop IT-nginx
```
Check:

```
sudo docker ps
```

To start it:

```
sudo docker start IT-nginx
```
## To remove the container
```
sudo docker rm nginx-server
```
The Nginx image will still be there 
check with:
```
sudo docker images
```
## To remove the images
```
sudo docker rmi nginx
```

## Result

The practical was completed successfully.

I installed and verified Docker, downloaded the Nginx image, created and started an Nginx container, mapped the host port to the container port, accessed the web server through a browser, tested it using `curl`, and inspected the container logs.
