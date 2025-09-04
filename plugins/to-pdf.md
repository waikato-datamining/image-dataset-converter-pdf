# to-pdf

* accepts: idc.api.ImageData

Saves the images in a PDF.

```
usage: to-pdf [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [-N LOGGER_NAME]
              [--skip] -o OUTPUT_FILE [-t] [-s IMAGE_SCALE] [-m METADATA_KEYS]
              [-x OFFSET_X] [-y OFFSET_Y] [-g GAP]

Saves the images in a PDF.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        The PDF file to write the images to. Supported
                        placeholders: {HOME}, {CWD}, {TMP}, {INPUT_PATH},
                        {INPUT_NAMEEXT}, {INPUT_NAMENOEXT}, {INPUT_EXT},
                        {INPUT_PARENT_PATH}, {INPUT_PARENT_NAME} (default:
                        None)
  -t, --image_name_as_title
                        Whether to use the image name as the title for the
                        image. (default: False)
  -s IMAGE_SCALE, --image_scale IMAGE_SCALE
                        The scale factor to apply to the image (1.0=100%,
                        -1=best fit). (default: 1.0)
  -m METADATA_KEYS, --metadata_keys METADATA_KEYS
                        The keys of meta-data values to display below the
                        image (comma-separated list). (default: None)
  -x OFFSET_X, --offset_x OFFSET_X
                        The horizontal offset on the page. (default: 50)
  -y OFFSET_Y, --offset_y OFFSET_Y
                        The vertical offset on the page. (default: 50)
  -g GAP, --gap GAP     The vertical gap between title, image, meta-data.
                        (default: 50)
```

Available placeholders:

* `{HOME}`: The home directory of the current user.
* `{CWD}`: The current working directory.
* `{TMP}`: The temp directory.
* `{INPUT_PATH}`: The directory part of the current input, i.e., `/some/where` of input `/some/where/file.txt`.
* `{INPUT_NAMEEXT}`: The name (incl extension) of the current input, i.e., `file.txt` of input `/some/where/file.txt`.
* `{INPUT_NAMENOEXT}`: The name (excl extension) of the current input, i.e., `file` of input `/some/where/file.txt`.
* `{INPUT_EXT}`: The extension of the current input (incl dot), i.e., `.txt` of input `/some/where/file.txt`.
* `{INPUT_PARENT_PATH}`: The directory part of the parent directory of the current input, i.e., `/some` of input `/some/where/file.txt`.
* `{INPUT_PARENT_NAME}`: The name of the parent directory of the current input, i.e., `where` of input `/some/where/file.txt`.
