# peruse

Quickly parse files and inspect the contents from a Python prompt.

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
in the `x` obj; paths are in `p`. Keys to these are short string references.

```
fred@pwlldu:data$ peruse direct_damages_summary/irrigation*
2025-09-17 12:00:10,136 x.a = direct_damages_summary/irrigation_edges_damages.parquet
2025-09-17 12:00:10,143 x.b = direct_damages_summary/irrigation_edges_EAD_EAEL.csv
2025-09-17 12:00:10,155 x.c = direct_damages_summary/irrigation_edges_exposures.parquet
2025-09-17 12:00:10,187 x.d = direct_damages_summary/irrigation_edges_losses.parquet
2025-09-17 12:00:10,214 x.e = direct_damages_summary/irrigation_nodes_damages.parquet
2025-09-17 12:00:10,216 x.f = direct_damages_summary/irrigation_nodes_EAD_EAEL.csv
2025-09-17 12:00:10,228 x.g = direct_damages_summary/irrigation_nodes_exposures.parquet
2025-09-17 12:00:10,265 x.h = direct_damages_summary/irrigation_nodes_losses.parquet

>>> x.c
          edge_id exposure_unit  ...  surface__rp_500__rcp_8.5__epoch_2080_conf_None
0      pipeline_1             m  ...                                      119.541937
1     pipeline_10             m  ...                                        0.000000
2    pipeline_101             m  ...                                       87.322512
3    pipeline_102             m  ...                                        0.000000
4    pipeline_103             m  ...                                        0.000000
..            ...           ...  ...                                             ...
177   pipeline_94             m  ...                                       65.596002
178   pipeline_95             m  ...                                       89.161340
179   pipeline_96             m  ...                                        0.000000
180   pipeline_97             m  ...                                       14.612505
181   pipeline_99             m  ...                                       39.975951

[182 rows x 94 columns]

>>> p.c
PosixPath('/data/direct_damages_summary/irrigation_edges_exposures.parquet')
```
