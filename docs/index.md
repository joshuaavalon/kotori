# Introduction

[![License][license-badge]][license]
[![Docker Pulls][docker-pull]][docker] 
[![Docker Stars][docker-star]][docker] 
[![Docker Image Size][docker-size]][docker-tag] 
[![Docker Layer][docker-layer]][docker-tag]

Kotori is self-hosted image manipulation proxy based on Python.

To improve websites performance, images are advised to be served with the exact size.
The common solutions are using a image hosting service like Cloudinary or ImageKit.

However, the price is much more expensive than host images on your storage (local or S3) 
and it is impossible to use your CDN, like Cloudflare.

Kotori is designed to read from you storage and serve the image to through any CDN and any domain.

# Features

* Read from different storage (Current support local and S3)
* Different configurations based on urls
* Dynamic transformation queries
* Alias for predefine transformations
* Limit transforms allowed

# Limitations

* No support for files with the same name (`foo.png` and `foo.jpg` are considered the same file)

# Deployment

Please read on [FLask document](http://flask.pocoo.org/docs/1.0/deploying/) on how to deploy.

Or you can use the [Docker image](docker.md).

[docker]: https://hub.docker.com/r/joshava/kotori/
[docker-tag]: https://hub.docker.com/r/joshava/kotori/tags/
[docker-pull]: https://img.shields.io/docker/pulls/joshava/kotori.svg
[docker-star]: https://img.shields.io/docker/stars/joshava/kotori.svg
[docker-size]: https://img.shields.io/microbadger/image-size/joshava/kotori.svg
[docker-layer]: https://img.shields.io/microbadger/layers/joshava/kotori.svg
[license]: https://github.com/joshuaavalon/kotori/blob/master/LICENSE
[license-badge]: https://img.shields.io/github/license/joshuaavalon/kotori.svg
