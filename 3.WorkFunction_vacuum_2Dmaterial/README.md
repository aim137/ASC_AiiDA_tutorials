# Tutorial 3 - WorkFunctions

The problem with the workflow produced in Tutorial 2 is that we miss the provenance of the data. To anyone except the person who actually ran these calculations, they will be just 5 unrelated pw.x calculations. The logic behind doing those calculations and the relation between them is not recorded anywhere, and consequently lost.

In this tutorial, we will address this issue of data provenance. This will be done by means of python decorators and AiiDA data types.
The introduction of these features will ensure that the data is tracked and the provenance is stored, while the actual workflow of calculations will not change at all. Essentially, we will be getting the provenance for free.

## Instructions

In principle, we can use the same workflow as in Tutorial 2, with the following changes:
- the functions that create data must be decorated as @calcfunctions
- the functions that call other processes must be decorated as @workfunctions
- there is no need to decorate the function that creates the builder, we are not interested in that provenance
- the data passed to and returned by these functions must belong to an AiiDA data type
  - in some cases, we are already using AiiDA data types, e.g., StructureData
  - all python data types (int, float, dict, etc) must be turned into AiiDA data types (Int, Float, Dict, etc) 

Finally, we will also add a new @calcfunction to calculate the energy difference of each run respect to the final run and choose the minimum vacuum that achieves an energy difference below a given threshold. 

## Shortcut instructions

To simplify the tutorial, you will not have to code the whole thing, but rather complete the blanks on a half-coded version of the solution that is provided - look for the string 'complete'.

However, I strongly encourage you to have a go at writing the functions yourself. Look at the code and you'll see where to start. 

## Inspect the results

Use `verdi process list -ap1` and note that not only the PwCalculations are there but also the @calcfuncions and @workfunctions we defined. This is because the provenance of those processes is now being tracked.

Use `verdi process status <pk>` with the `pk` of the WorkFunction to see a tree representation of what it does, i.e., what processes it calls.

Use `verdi node graph generate <pk>` with the `pk` of the WorkFunction and that of one PwCalculation. See how the relationship between the different PwCalculations is displayed. 


