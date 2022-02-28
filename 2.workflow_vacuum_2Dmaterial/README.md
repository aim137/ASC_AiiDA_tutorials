# Tutorial 2 - workflow

Of course, running one or two calculations is never the case. The prediction of one single quantity, e.g., the magnetic anisotropy of a material, will typically require tens or hundreds of calculations. We normally organise these calculations in workflows that follow a certain logic derived from phsyical and numerical considerations.
In this tutorial, we will look at a simple example of a workflow concerning the vacuum required to model a 2D material like graphene. Plane wave codes as QE's pw.x consider periodic boundary conditions in all directions since they make use of Bloch's theorem. This is very well suited for solids, which replicate the unit cell periodically in all directions. However, 2D materials extend periodically only in the in-plane directions only (x and y), the z direction should not be replicated. Unfortunately, pw.x will also replicate the system in the z coordinate, generating graphene layers that should not be there. Furthermore, the grphene layer we want to study will interact with these unphysical layers, so we need to maker sure to suppress those interactions. One way of doing this is extending the unit cell vertically to include a vacuumm (i.e., empty space) large enough to prevent interactions between these layers. 
Computationally, we will run several calculations with increasing vacuum up to the point where the energy difference between two successive calcualtions is below an acceptable threshold. At this point, we consider the vacuumm to be converged, we take that structure and continue our calculations.

## For the patient

## For the inpatient 


