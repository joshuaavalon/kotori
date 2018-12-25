# Configuration

This part will teach you how to customize your configuration file.

By default, Kotori come with two configuration loader: YAML and JSON.
Here is a example configuration in YAML.

The configuration location should be set by environment variable `KOTORI_CONFIG`.

```yml
storage:
  local:
    type: file
    options:
      root: /var/www/html/image
  amazon:
    type: s3
    options:
      region_name: us-east-1
      endpoint_url: https://s3.amazonaws.com
      bucket: image-bucket
      aws_access_key_id: aws_access_key_id
      aws_secret_access_key: aws_secret_access_key
      root: foo/
transform:
  blog:
    - type: t
      options:
        - 800
        - 400
route:
  "/":
    storage: local
    transform:
      - r
      - original
  "/blog":
    storage: amazon
    transform: blog
    expire: 86400
    save:
      JPEG:
        progressive: true
        quality: 80
  "/private":
    storage: local
    transform:  false
cache:
  CACHE_TYPE: "filesystem"
  CACHE_DIR: /var/www/html/cache
  CACHE_DEFAULT_TIMEOUT: 600
  CACHE_THRESHOLD: 100
```

At root level, configuration contains 4 elements: `storage`, `transform`, `route` and `cache`.

## Storage

`storage` should contains configuration of storage endpoint.
In the example, `amazon` and `local` are the names of the storage endpoints.

Kotori supports two types of endpoint: `file` and `s3`.

### File

* `root` - Root folder to search from.

For example, if the root is `/var/www/html/image` and it is used on `/foo`.
When `/foo/bar.jpg` is requested, `/var/www/html/image/bar.*` will be searched.

### S3

* `region_name` - Bucket region
* `endpoint_url` - You don't need this if you are using S3. Only change this if you are using other S3 compatible storage. 
* `bucket` - Bucket name
* `aws_access_key_id` - Access key id
* `aws_secret_access_key` - Access key secret
* `root` - Prefix of the object key. S3 use key like `foo/bar.jpg` instead of real folder. Your key should not be started with `/` but it should be ended with `/`.

## Transform

This section allows you to define alias for predefine transformation.

The key is the alias and the value should be an array of transformations definition.

## Route

The configuration define which configuration to use based on path.
It matches based how accurate it matched.

* `storage` - The name of the storage configuration that defined in storage section.
* `transform` - The name of the transform configuration that defined in transform section or type of the transform. `true` to allow any transforms and `false` to decline all transforms.
* `expire` - `max-age` for `Cache-Control` header.
* `save` - Please refer to [Pillow](https://pillow.readthedocs.io/en/5.3.x/handbook/image-file-formats.html) for formats and options.

## Cache

Please refer to [Flask-Caching](https://pythonhosted.org/Flask-Caching/#configuring-flask-caching) for options.

