# Tutorial 2 - workflow

Of course, running one or two calculations is never the case. The prediction of one single quantity, e.g., the magnetic anisotropy of a material, will typically require tens or hundreds of calculations. We normally organise these calculations in workflows that follow a certain logic derived from phsyical and numerical considerations.

In this tutorial, we will look at a simple example of a workflow concerning the vacuum required to model a 2D material like graphene. Plane wave codes as QE's pw.x consider periodic boundary conditions in all directions since they make use of Bloch's theorem. This is very well suited for solids, which replicate the unit cell periodically in all directions. However, 2D materials extend periodically only in the in-plane directions (x and y), and the z direction should not be replicated.

Unfortunately, pw.x will also replicate the system in the z coordinate, generating graphene layers that should not be there. Furthermore, the grphene layer we want to study will interact with these unphysical layers, so we need to maker sure to suppress those interactions. One way of doing this is extending the unit cell vertically to include a vacuum (i.e., empty space) large enough to prevent interactions between these layers. 

Computationally, we will run several calculations with increasing vacuum up to the point where the energy difference between two successive calcualations is below an acceptable threshold. At this point, we consider the vacuum to be converged, we take that structure and continue with our calculations.

## Instructions

Start from the file provided and make the following additions

- write a python function that stretches/compresses a unit cell vertically, changing amount of vacuum
  - input: an original structure (variable `aiida_datatype_structure`)
  - input: a factor by which it should affect the z direction (type float)
  - output: a new, modified structure (of data type `StructureData`) 
  - output: the magnitude of the vacuum in Angstroms
- write a python function that generates the builder for a calculation
  - input: variable `aiida_datatype_structure`
  - input: variable `aiida_datatype_kpoints`
  - input: variable `aiida_datatype_parameters`
  - input: variable `aiida_datatype_pseudos` (optional)
  - output: builder
- write a function that loops over a number of factors, e.g., 5 factors in [0.6,1.2] and, in each instance of the loops
  - calls the function to stretch the structure
  - calls the functions to generate the builder
  - runs the builder
  - processes the results
  - input: minimum factor
  - input: maximum factor
  - input: number of factors
  - output: list of dictionaries, one dictionary per calculation
    - each dictionary contains the energy and the vacuum of the calculation
- execute the function and plot the results (energy vs vacuum).

## Shortcut instructions

To simplify the tutorial, you will not have to code the whole thing, but rather complete the blanks on a half-coded version of the solution that is provided - look for the string 'complete'.

However, I strongly encourage you to have a go at writing the functions yourself. Look at the code and you'll see where to start. 

## Inspect the results

Use `verdi process list -ap1` and note that, as far as AiiDA is concerned, five PwCalculations is all there is. 

Use `verdi node graph generate <pk>` with the `pk` of one PwCalculation.
See that the logic behind why we chose to do those calculations is not registered anywhere, nor are the arithmetic operations we did to stretch the cells, e.g., we do not know where the structure came from.

