# Time Series Ensemble Format

![alt text](images/illustration.png)

## What is the time series ensemble format?

**It is a format for storing a set of parameters and associated output time series.**

It is intended as a format for datasets of input-output data, of the type used to study a model, or process, generating time series outputs.  It is a data structure for, for example, **sensitivity analysis** of epidemiological models.

### Time series ensemble format datasets adhere to the following:

1. Each dataset contains the files: 
   
   i. `parameters.csv`
   
   ii. `parameters_metadata.csv`
   
   iii. `output_i.csv`for every `i`, where `i` is an `index` in `parameters.csv`
   
   iv. `output_metadata.csv` 

2. `parameters.csv` contains an `index` field. with a unique integer for matching the parameters with their output.

3. `parameters_metadata.csv` contains the fields: `parameter`: name of the parameter matching `parameters.csv`,`description`: plain text description, `unit`.

4. `output_metadata.csv` contains the fields: `output`: name of the parameter matching `parameters.csv`,`description`: plain text description, `unit`.

5. `output_metadata.csv` contains **1** output with the description `time_unit`.

6. Each dataset is located in a separate folder containing the files prescribed in (1).

### Example

For a model with parameters `foo` and `bar`, evaluted three times `parameters.csv` and `parameters_metadata.csv` are:

parameters.csv

```parameters.csv
index,foo,bar
0,1,2
1,1.5,2
42,2,1.5
```

`parameters_metadata.csv`

```
parameter,description,unit
foo,Example variable,meter
bar,"Elevated region of sediment, deposited by flow",Gunter's chain
```

The model outputs are time series with values: `baz_mean`, `baz_variance`, `qux` at two weeks. Thus, `output_metadata.csv` and `output_i.csv` are

`output_metadata.csv`

```
output,description,unit
week,time_unit,week
baz_mean,Mean of output baz,dimensionless
baz_variance,Variance of output baz,dimensionless
qux,Alternative form of quux,meter
```

`output_0.csv`

```
week,baz_mean,baz_variance,qux
0,0.5,0.2,3
1,0.7,0.3,1
```

`output_1.csv`

```
week,baz_mean,baz_variance,qux
0,0.2,0.3,2
1,0.4,0.5,1
```

`output_42.csv`

```
week,baz_mean,baz_variance,qux
0,-1.0,0.1,3
1,-0.4,0.4,2
```

**Example datadset**

An larger example with real data can be found [here]( ).

## Parsers

**Sandu**

[Here]() is a parser to create **sandu sensitivty input objects**, for use with any of [sandu's](https://github.com/ErikRZH/sandu) functionality. 

#### Advantages

The format is *Human readable* and *widely compatible* due to containg data in the comma separated values format (CSV). 