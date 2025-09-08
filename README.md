# peruse

Quickly parse a file and inspect its contents from a Python prompt.

Written by Fred Thomas

## Installation

Install with:
```shell
git clone git@github.com:thomas-fred/peruse.git
cd peruse
micromamba create -f env.yaml -y
```

Then add this folder to your `PATH`. Or alternatively, add a symlink to
the `peruse` script from a directory already on your `$PATH`.

## Usage

Invoke peruse with the paths to data files you want to inspect:
```
peruse <file_0> <file_1> <...> <file_n>
```

You'll be given a Python prompt with the deserialized files available as values
in the `data` dictionary. Keys to `data` are the index of the respective script
argument, e.g. `0`, `1`, etc.
