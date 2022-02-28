# Tutorial 3 - WorkFunctions

The problem with the workflow produced in Tutorial 2 is that we miss the provenance of the data. To anyone except the person who actually ran these calculations, they will be just 5 unrelated pw.x calculations. The logic behind doing those calculations and the relation between them is not recorder anywhere, and consequently lost.

In this tutorial, we will address this issue of data provenance. This will be done by means of python decorators and AiiDA data types. In principle, we can use the same workflow as in Tutorial 2, with the following changes:
- the functions that create data must be decorated as @calcfunctions
- the functions that call other processes must be decorated as @workfunctions
- the data passed to and returned by these functions must belong to an AiiDA data type
  - in some cases, we are already using AiiDA data types, e.g., StructureData
  - all python data types (int, float, dict, etc) must be turned into AiiDA data types (Int, Float, Dict, etc) 

These simple changes will ensure that the data is tracked and the provenance is stored. Hence, we will get the provenance for free.

## For the patient

## For the inpatient


