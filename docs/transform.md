# Transform

The access url is `http://<domain>/<transform>/<path>.<ext>`.

`transform` is the query the manipulate image. 
It can be either a series of queries separate by comma like `t_100_100,r_200_200` or a alias defined in configuration.

`ext` is the format it return.

## Origin

* `/origin`

This query returns the origin image. Note that it may still be modify by the format or save options.

## Thumbnail

* `/t_<width>_<height>` 
* `/t_<width>_<height>_<resample>`

This query creates a thumbnail with a maximum given width and height.
Note that this keeps the aspect ratio and does **NOT** enlarge the image.

### Resample

`resample` define what [methods][resample] to resample. Default to `NEAREST`.
Note that you need the [numeric value][filter].

## Resize

* `/r_<width>_<height>`
* `/t_<width>_<height>_<resample>`
* `/r_<width>_<height>_<resample>_<crop>`

This query resizes the image to given width and height.

### Resample

`resample` define what [methods][resample] to resample. Default to `NEAREST`.
Note that you need the [numeric value][filter].

### Crop

If you want to keep the aspect ratio, you must define how to crop the image.

* `t` - crop the top / left of the image.
* `b` - crop the bottom / right of the image.
* `c` - crop the center of the image.

[resample]: https://pillow.readthedocs.io/en/5.3.x/handbook/concepts.html#concept-filters
[filter]: https://github.com/python-pillow/Pillow/blob/master/src/PIL/Image.py#L191
