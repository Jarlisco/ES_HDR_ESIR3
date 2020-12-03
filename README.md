
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

**Usage**:

```console
$ [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `crf-to-hdr`: Uses images of diffrent exposure to create...
* `hdr-to-ldr`: Tone mapping HDR image to LDR using opencv...
* `ldr-to-hqldr`: Fusion of mutiple LDR images to create an...

* `hdr-tmo-durand`: ~ Tone map using homemade Durand tone mapper.
* `hdr-tmo-exp`: ~ Tone map HDR images using exponential...
* `hdr-tmo-gamma`: ~ Tone map HDR images using gamma operator.
* `hdr-tmo-local`: ~ Tone map using a local based method.
* `hdr-tmo-log`: ~ Tone map HDR images using log operator.
* `hdr-tmo-norm`: ~ Tone map HDR images by norming aroung the...


## `crf-to-hdr`

Uses images of diffrent exposure to create HDR image and then it is tone mapped to let you see the result.

**Usage**:

```console
$ crf-to-hdr [OPTIONS] [FUSION_TYPE] PATHS_AND_EXPOSURES...
```

**Arguments**:

* `[FUSION_TYPE]`: Choose between debevec or mertens fusion.  [default: debevec]
* `PATHS_AND_EXPOSURES...`: List of paths to images to merge along with list of exposure times of each images in the same order. Ex: im1.jpg im2.jpg 0.005 0.015  [required]

**Options**:

* `--help`: Show this message and exit.

## `hdr-tmo-durand`

~ Tone map using homemade Durand tone mapper. 
It uses bilateral filtering and logarithme base 2 (log2).

**Usage**:

```console
$ hdr-tmo-durand [OPTIONS] FN
```

**Arguments**:

* `FN`: Path to hdr image file.  [required]

**Options**:

* `--help`: Show this message and exit.

## `hdr-tmo-exp`

~ Tone map HDR images using exponential operator.

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

~ Tone map HDR images using gamma operator.

**Usage**:

```console
$ hdr-tmo-gamma [OPTIONS] FN GAMMA
```

**Arguments**:

* `FN`: Path to HDR image.  [required]
* `GAMMA`: 1/gamma is used as exponent.  [required]

**Options**:

* `--help`: Show this message and exit.

## `hdr-tmo-local`

~ Tone map using a local based method.
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

~ Tone map HDR images using log operator.

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

~ Tone map HDR images by norming aroung the maximum of luminance.

**Usage**:

```console
$ hdr-tmo-norm [OPTIONS] FN
```

**Arguments**:

* `FN`: Path to HDR image.  [required]

**Options**:

* `--help`: Show this message and exit.

## `hdr-to-ldr`

Tone mapping HDR image to LDR using opencv implemented tone mappers.

**Usage**:

```console
$ hdr-to-ldr [OPTIONS] [TONE_MAPPER] PATH GAMMA
```

**Arguments**:

* `[TONE_MAPPER]`: Choose your tone mapper (mantiuk or reinhard)  [default: mantiuk]
* `PATH`: Path to HDR image.  [required]
* `GAMMA`: It is THE gamma.  [required]

**Options**:

* `--help`: Show this message and exit.

## `ldr-to-hqldr`

Fusion of mutiple LDR images to create an High Quality LDR image (HQLDR).

**Usage**:

```console
$ ldr-to-hqldr [OPTIONS] [FUSION_TYPE] PATHS...
```

**Arguments**:

* `[FUSION_TYPE]`: Choose your fusion algorithm (only mertens is available for now).  [default: mertens]
* `PATHS...`: List of paths to images to merge.  [required]

**Options**:

* `--help`: Show this message and exit.

