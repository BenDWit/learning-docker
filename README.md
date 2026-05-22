# Learning Docker

This is a simple project with a small Python API that just checks uptime, which we then collect with Prometheus. The goal was to build a full environment with monitoring, a reverse proxy, and metrics.

## The Web App

First I built the web app with FastAPI. The app itself isn't that important — Docker was the focus of this project. Once I had the script working, I moved on to writing the Dockerfile.

## The Dockerfile

I started by choosing a base image. I went with `uv` since I like it better than `pip`.

**The basics:**

- `FROM` imports a base image.
- `RUN` executes commands during the build. I started with a small `python3` test, then moved to `pip install`, and eventually settled on copying a `requirements.txt` and running `uv pip install` against it.

**Best practices:**

It's still basically Linux under the hood, so I added a user and a group, then switched to that user with `USER`. Easy enough once you think of it that way.

**Putting it together:**

- `COPY` brings the actual app into the image.
- `EXPOSE` documents what port this image will use.
- `CMD` runs the app. This one matters you can't use `RUN` here, because `RUN` is only for the build stage. `CMD` is your deploy command.

**Healthcheck:**

I started with just `uv --version` as a healthcheck, then upgraded it to a `curl` against the running app to actually verify the deploy.


# Docker Compose
Next up is actually making something cool using Docker Compose. This is like the connecting layer defining how containers should connect and store data.

Gotta set:
- `name:` name of this stack
- `services:` all the images you actually want to deploy
    - `nameofservice:` name of the service — for this example we'll use nginx or "webserver"
    - `image:` `nginx:latest`, where the first is the name of the image and the second is the version
    - `ports:` port routing — for this we'll use `- 8080:80`
    - `volumes:` persistent storage
    - `networks:` what networks should this container be part of?
- `volumes:` where persistent storage should be on the host's filesystem
- `networks:` internal network and configuration

You can also pass environmental variables with `environment:`.


## Best practices

I also learned some best practices like multistage building, where you use `FROM` to have multiple build stages so you can import dependencies in a different environment than the deployment for debloat purposes. You can use `COPY --from:` to copy over needed files, and if you have multiple stages you can number them starting from 0.

Service DNS: every service name is resolvable by other hosts in the network.

## what i want to learn next:
Second docker session planned where i will dig into these topics:
- [ ] Resource limits
- [ ] Logging
- [ ] Override files
- [ ] profiles
- [ ] prune/cleanup
- [ ] ARG vs ENV
- [ ] image registries
- [ ] security

Also K8's writeup coming soon.s
