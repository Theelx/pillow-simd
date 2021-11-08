<<<<<<< HEAD
# Pillow-SIMD

Pillow-SIMD is "following" [Pillow][original-docs].
Pillow-SIMD versions are 100% compatible
drop-in replacements for Pillow of the same version.
For example, `Pillow-SIMD 3.2.0.post3` is a drop-in replacement for
`Pillow 3.2.0`, and  `Pillow-SIMD 3.3.3.post0` — for `Pillow 3.3.3`.

For more information on the original Pillow, please refer to:
[read the documentation][original-docs],
[check the changelog][original-changelog] and
[find out how to contribute][original-contribute].


## Why SIMD

There are multiple ways to tweak image processing performance.
To name a few, such ways can be: utilizing better algorithms, optimizing existing implementations, 
using more processing power and/or resources. 
One of the great examples of using a more efficient algorithm is [replacing][gaussian-blur-changes] 
a convolution-based Gaussian blur with a sequential-box one.

Such examples are rather rare, though. It is also known, that certain processes might be optimized 
by using parallel processing to run the respective routines.
But a more practical key to optimizations might be making things work faster 
using the resources at hand. For instance, SIMD computing might be the case.

SIMD stands for "single instruction, multiple data" and its essence is 
in performing the same operation on multiple data points simultaneously 
by using multiple processing elements. 
Common CPU SIMD instruction sets are MMX, SSE-SSE4, AVX, AVX2, AVX512, NEON.

Currently, Pillow-SIMD can be [compiled](#installation) with SSE4 (default) or AVX2 support.


## Status

Pillow-SIMD project is production-ready.
The project is supported by Uploadcare, a SAAS for cloud-based image storing and processing.

[![Uploadcare][uploadcare.logo]][uploadcare.com]

In fact, Uploadcare has been running Pillow-SIMD since 2015.

The following image operations are currently SIMD-accelerated:

- Resize (convolution-based resampling): SSE4, AVX2
- Gaussian and box blur: SSE4
- Alpha composition: SSE4, AVX2
- RGBA → RGBa (alpha premultiplication): SSE4, AVX2
- RGBa → RGBA (division by alpha): SSE4, AVX2
- RGB → L (grayscale): SSE4
- 3x3 and 5x5 kernel filters: SSE4, AVX2
- Split and get_channel: SSE4


## Benchmarks

Tons of tests can be found on the [Pillow Performance][pillow-perf-page] page.
There are benchmarks against different versions of Pillow and Pillow-SIMD
as well as ImageMagick, Skia, OpenCV and IPP.

The results show that for resizing Pillow is always faster than ImageMagick, 
Pillow-SIMD, in turn, is even faster than the original Pillow by the factor of 4-6. 
In general, Pillow-SIMD with AVX2 is always **16 to 40 times faster** than 
ImageMagick and outperforms Skia, the high-speed graphics library used in Chromium.


## Why Pillow itself is so fast

No cheats involved. We've used identical high-quality resize and blur methods for the benchmark. 
Outcomes produced by different libraries are in almost pixel-perfect agreement. 
The difference in measured rates is only provided with the performance of every involved algorithm. 


## Why Pillow-SIMD is even faster

Because of the SIMD computing, of course. But there's more to it: 
heavy loops unrolling, specific instructions, which aren't available for scalar data types.


## Why do not contribute SIMD to the original Pillow

Well, it's not that simple. First of all, the original Pillow supports 
a large number of architectures, not just x86.
But even for x86 platforms, Pillow is often distributed via precompiled binaries.
In order for us to integrate SIMD into the precompiled binaries 
we'd need to execute runtime CPU capabilities checks.
To compile the code this way we need to pass the `-mavx2` option to the compiler.
But with the option included, a compiler will inject AVX instructions even
for SSE functions (i.e. interchange them) since every SSE instruction has its AVX equivalent.
So there is no easy way to compile such library, especially with setuptools.


## Installation

If there's a copy of the original Pillow installed, it has to be removed first
with `$ pip uninstall -y pillow`.
Please install [prerequisites](https://pillow.readthedocs.io/en/stable/installation.html#building-from-source) for your platform.
The installation itself is simple just as running `$ pip install pillow-simd`, 
and if you're using SSE4-capable CPU everything should run smoothly.
If you'd like to install the AVX2-enabled version, 
you need to pass the additional flag to a C compiler. 
The easiest way to do so is to define the `CC` variable during the compilation.

```bash
$ pip uninstall pillow
$ CC="cc -mavx2" pip install -U --force-reinstall pillow-simd
```


## Contributing to Pillow-SIMD

Please be aware that Pillow-SIMD and Pillow are two separate projects.
Please submit bugs and improvements not related to SIMD to the [original Pillow][original-issues].
All bugfixes to the original Pillow will then be transferred to the next Pillow-SIMD version automatically.


  [original-homepage]: https://python-pillow.org/
  [original-docs]: https://pillow.readthedocs.io/
  [original-issues]: https://github.com/python-pillow/Pillow/issues/new
  [original-changelog]: https://github.com/python-pillow/Pillow/blob/master/CHANGES.rst
  [original-contribute]: https://github.com/python-pillow/Pillow/blob/master/.github/CONTRIBUTING.md
  [gaussian-blur-changes]: https://pillow.readthedocs.io/en/3.2.x/releasenotes/2.7.0.html#gaussian-blur-and-unsharp-mask
  [pillow-perf-page]: https://python-pillow.github.io/pillow-perf/
  [pillow-perf-repo]: https://github.com/python-pillow/pillow-perf
  [uploadcare.com]: https://uploadcare.com/?utm_source=github&utm_medium=description&utm_campaign=pillow-simd
  [uploadcare.logo]: https://ucarecdn.com/8eca784b-bbe5-4f7e-8cdf-98d75aab8cec/logotransparent.svg
=======
<p align="center">
    <img width="248" height="250" src="https://raw.githubusercontent.com/python-pillow/pillow-logo/main/pillow-logo-248x250.png" alt="Pillow logo">
</p>

# Pillow

## Python Imaging Library (Fork)

Pillow is the friendly PIL fork by [Alex Clark and
Contributors](https://github.com/python-pillow/Pillow/graphs/contributors).
PIL is the Python Imaging Library by Fredrik Lundh and Contributors.
As of 2019, Pillow development is
[supported by Tidelift](https://tidelift.com/subscription/pkg/pypi-pillow?utm_source=pypi-pillow&utm_medium=readme&utm_campaign=enterprise).

<table>
    <tr>
        <th>docs</th>
        <td>
            <a href="https://pillow.readthedocs.io/?badge=latest"><img
                alt="Documentation Status"
                src="https://readthedocs.org/projects/pillow/badge/?version=latest"></a>
        </td>
    </tr>
    <tr>
        <th>tests</th>
        <td>
            <a href="https://github.com/python-pillow/Pillow/actions?query=workflow%3ALint"><img
                alt="GitHub Actions build status (Lint)"
                src="https://github.com/python-pillow/Pillow/workflows/Lint/badge.svg"></a>
            <a href="https://github.com/python-pillow/Pillow/actions?query=workflow%3ATest"><img
                alt="GitHub Actions build status (Test Linux and macOS)"
                src="https://github.com/python-pillow/Pillow/workflows/Test/badge.svg"></a>
            <a href="https://github.com/python-pillow/Pillow/actions?query=workflow%3A%22Test+Windows%22"><img
                alt="GitHub Actions build status (Test Windows)"
                src="https://github.com/python-pillow/Pillow/workflows/Test%20Windows/badge.svg"></a>
            <a href="https://github.com/python-pillow/Pillow/actions?query=workflow%3A%22Test+Docker%22"><img
                alt="GitHub Actions build status (Test Docker)"
                src="https://github.com/python-pillow/Pillow/workflows/Test%20Docker/badge.svg"></a>
            <a href="https://ci.appveyor.com/project/python-pillow/Pillow"><img
                alt="AppVeyor CI build status (Windows)"
                src="https://img.shields.io/appveyor/build/python-pillow/Pillow/main.svg?label=Windows%20build"></a>
            <a href="https://github.com/python-pillow/pillow-wheels/actions"><img
                alt="GitHub Actions wheels build status (Wheels)"
                src="https://github.com/python-pillow/pillow-wheels/workflows/Wheels/badge.svg"></a>
            <a href="https://travis-ci.com/github/python-pillow/pillow-wheels"><img
                alt="Travis CI wheels build status (aarch64)"
                src="https://img.shields.io/travis/com/python-pillow/pillow-wheels/main.svg?label=aarch64%20wheels"></a>
            <a href="https://codecov.io/gh/python-pillow/Pillow"><img
                alt="Code coverage"
                src="https://codecov.io/gh/python-pillow/Pillow/branch/main/graph/badge.svg"></a>
        </td>
    </tr>
    <tr>
        <th>package</th>
        <td>
            <a href="https://zenodo.org/badge/latestdoi/17549/python-pillow/Pillow"><img
                alt="Zenodo"
                src="https://zenodo.org/badge/17549/python-pillow/Pillow.svg"></a>
            <a href="https://tidelift.com/subscription/pkg/pypi-pillow?utm_source=pypi-pillow&utm_medium=badge"><img
                alt="Tidelift"
                src="https://tidelift.com/badges/package/pypi/Pillow?style=flat"></a>
            <a href="https://pypi.org/project/Pillow/"><img
                alt="Newest PyPI version"
                src="https://img.shields.io/pypi/v/pillow.svg"></a>
            <a href="https://pypi.org/project/Pillow/"><img
                alt="Number of PyPI downloads"
                src="https://img.shields.io/pypi/dm/pillow.svg"></a>
        </td>
    </tr>
    <tr>
        <th>social</th>
        <td>
            <a href="https://gitter.im/python-pillow/Pillow?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge"><img
                alt="Join the chat at https://gitter.im/python-pillow/Pillow"
                src="https://badges.gitter.im/python-pillow/Pillow.svg"></a>
            <a href="https://twitter.com/PythonPillow"><img
                alt="Follow on https://twitter.com/PythonPillow"
                src="https://img.shields.io/badge/tweet-on%20Twitter-00aced.svg"></a>
        </td>
    </tr>
</table>

## Overview

The Python Imaging Library adds image processing capabilities to your Python interpreter.

This library provides extensive file format support, an efficient internal representation, and fairly powerful image processing capabilities.

The core image library is designed for fast access to data stored in a few basic pixel formats. It should provide a solid foundation for a general image processing tool.

## More Information

- [Documentation](https://pillow.readthedocs.io/)
  - [Installation](https://pillow.readthedocs.io/en/latest/installation.html)
  - [Handbook](https://pillow.readthedocs.io/en/latest/handbook/index.html)
- [Contribute](https://github.com/python-pillow/Pillow/blob/main/.github/CONTRIBUTING.md)
  - [Issues](https://github.com/python-pillow/Pillow/issues)
  - [Pull requests](https://github.com/python-pillow/Pillow/pulls)
- [Release notes](https://pillow.readthedocs.io/en/stable/releasenotes/index.html)
- [Changelog](https://github.com/python-pillow/Pillow/blob/main/CHANGES.rst)
  - [Pre-fork](https://github.com/python-pillow/Pillow/blob/main/CHANGES.rst#pre-fork)

## Report a Vulnerability

To report a security vulnerability, please follow the procedure described in the [Tidelift security policy](https://tidelift.com/docs/security).
>>>>>>> a3d1e2f85db890c6a1623e3902711863f55cc54e
