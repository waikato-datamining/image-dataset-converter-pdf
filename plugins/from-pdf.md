# from-pdf

* generates: idc.api.ImageData

Extracts the images from the PDF file(s) and forwards them as the specified data type.

```
usage: from-pdf [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [-N LOGGER_NAME]
                [-i [INPUT ...]] [-I [INPUT_LIST ...]]
                [--resume_from RESUME_FROM] -t {dp,ic,is,od}

Extracts the images from the PDF file(s) and forwards them as the specified
data type.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -i [INPUT ...], --input [INPUT ...]
                        Path to the PDF file(s) to extract the images from;
                        glob syntax is supported; Supported placeholders:
                        {HOME}, {CWD}, {TMP} (default: None)
  -I [INPUT_LIST ...], --input_list [INPUT_LIST ...]
                        Path to the text file(s) listing the PDF files to use;
                        Supported placeholders: {HOME}, {CWD}, {TMP} (default:
                        None)
  --resume_from RESUME_FROM
                        Glob expression matching the file to resume from,
                        e.g., '*/012345.pdf' (default: None)
  -t {dp,ic,is,od}, --data_type {dp,ic,is,od}
                        The type of data to forward (default: None)
```

The following data types are available:

* dp: depth
* ic: image classification
* is: image segmentation
* od: object detection


Available placeholders:

* `{HOME}`: The home directory of the current user.
* `{CWD}`: The current working directory.
* `{TMP}`: The temp directory.
