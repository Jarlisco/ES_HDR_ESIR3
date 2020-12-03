
# INTRO


This project revolves around processing HDR images.
Could be generating HDR images from multiple LDR images or
tone mapping HDR images to display it on your screen.


# INSTALLATION


To install this project with it's virtual env you will need pipenv:
- pip install pipenv
In the project folder, you should see a Pipfile
- pipenv install -> to install the env and requirements
Start a new shell using this env
- pipenv shell
Run python file
- python run.py

# CLI

Awesome CLI user manager.

**Usage**:

```console
$ [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `crf-hdr-tmo-ldr`: Uses images of diffrent exposure to create...
* `hdr-tmo-durand`: We tried to implement and homemade Durand...
* `hdr-tmo-exp`: Tone map HDR images using exponential...
* `hdr-tmo-gamma`: Tone map HDR images using gamma operator.
* `hdr-tmo-ldr`
* `hdr-tmo-local`: This a local based method to tone map HDR...
* `hdr-tmo-log`: Tone map HDR images using log operator.
* `hdr-tmo-norm`: Tone map HDR images by norming aroung the...
* `ldr-fusion-ldr`

## `crf-hdr-tmo-ldr`

Uses images of diffrent exposure to create HDR image and then it is tone mapped to let you see the result.

**Usage**:

```console
$ crf-hdr-tmo-ldr [OPTIONS] [FUSION_TYPE] PATHPREFIX COUNT EXTENSION
```

**Arguments**:

* `[FUSION_TYPE]`: Choose between debevec or mentens fusion.  [default: debevec]
* `PATHPREFIX`: Path prefix to images to merge. Path prefix is then completed with a number and the file extension ex: .img/img(1.jpg)  [required]
* `COUNT`: Number of images to merge. It will complete the path prefix starting from 1 to 'count' included.  [required]
* `EXTENSION`: Image file extension it will complete the path prefix  [required]

**Options**:

* `--help`: Show this message and exit.

## `hdr-tmo-durand`

We tried to implement and homemade Durand tone mapping. 
It uses bilateral filtering and base logarithme (log2).

**Usage**:

```console
$ hdr-tmo-durand [OPTIONS] FN
```

**Arguments**:

* `FN`: Path to hdr image file.  [required]

**Options**:

* `--help`: Show this message and exit.

## `hdr-tmo-exp`

Tone map HDR images using exponential operator.

**Usage**:

```console
$ hdr-tmo-exp [OPTIONS] FN K Q
```

**Arguments**:

* `FN`: Path to HDR image.  [required]
* `K`: Luminance multiplier.  [required]
* `Q`: Average Luminance mitiplier.  [required]

**Options**:

* `--help`: Show this message and exit.

## `hdr-tmo-gamma`

Tone map HDR images using gamma operator.

**Usage**:

```console
$ hdr-tmo-gamma [OPTIONS] FN GAMMA
```

**Arguments**:

* `FN`: Path to HDR image.  [required]
* `GAMMA`: 1/gamma is used as exponent.  [required]

**Options**:

* `--help`: Show this message and exit.

## `hdr-tmo-ldr`

**Usage**:

```console
$ hdr-tmo-ldr [OPTIONS] NAME FN GAMMA
```

**Arguments**:

* `NAME`: [required]
* `FN`: [required]
* `GAMMA`: [required]

**Options**:

* `--help`: Show this message and exit.

## `hdr-tmo-local`

This a local based method to tone map HDR images.
It uses local luminance normalization.

**Usage**:

```console
$ hdr-tmo-local [OPTIONS] FN [ALPHA]
```

**Arguments**:

* `FN`: Path to hdr image file.  [required]
* `[ALPHA]`: 1-alpha is luminance denominator exponent  [default: 1.0]

**Options**:

* `--help`: Show this message and exit.

## `hdr-tmo-log`

Tone map HDR images using log operator.

**Usage**:

```console
$ hdr-tmo-log [OPTIONS] FN K Q
```

**Arguments**:

* `FN`: Path to hdr image file.  [required]
* `K`: Luminance multiplier.  [required]
* `Q`: Max Luminance multiplier.  [required]

**Options**:

* `--help`: Show this message and exit.

## `hdr-tmo-norm`

Tone map HDR images by norming aroung the maximum of luminance.

**Usage**:

```console
$ hdr-tmo-norm [OPTIONS] FN
```

**Arguments**:

* `FN`: Path to HDR image.  [required]

**Options**:

* `--help`: Show this message and exit.

## `ldr-fusion-ldr`

**Usage**:

```console
$ ldr-fusion-ldr [OPTIONS] [FUSION_TYPE]
```

**Arguments**:

* `[FUSION_TYPE]`: [default: debevec]

**Options**:

* `--help`: Show this message and exit.
