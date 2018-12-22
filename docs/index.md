# Introduction

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
