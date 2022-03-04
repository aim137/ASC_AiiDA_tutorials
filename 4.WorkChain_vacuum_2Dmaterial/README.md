# Tutorial 4 - WorkChains

Even though the WorkFunction produced in Tutorial 3 tracks provenance as intended, it still has a major flaw that will ultimately result in the introduction of WorkChains. 
WorkFunctions run blockingly - you might have noticed that the terminal where the WorkFunction ran remained blocked until the full process had finished. 
This may not have been a noticeable problem, but only because each `pw.x` calculation took less than a minute, and the whole process, around 10 minutes. 
However, most workflows will typically take hours if not days, and at some point during their execution, we want to be able to shut down the computer and leave.
Also, should the workflow be interrupted at any point, we would like to pick-up from where it stopped in a future run.
These are the motivations behind WorkChains:
- one can *submit* a WorkChain to the daemon and continue using the terminal or shut down the computer.
- WorkChains can have checkpoints to save any intermediate result before it eventually crashes, and restart from there.

In this tutorial, we will turn our WorkFunction into a WorkChain.

## Instructions

In principle, we can start from the code in Tutorial 3 and do some changes. The following is a non-exhaustive and non-detailed list of those changes:
- Instead of decorating the main function with @workfunction, WorkChains are defined as a sub-class of the class WorkChain.
- In a separate file to the one where the WorkChain was defined, one has to instantiate the WorkChain and submit it.
- The entire algorithm that was inside the WorkFunction must be broken down in methods of the new sub-class being defined,
  - The WorkChain will have an outline, where a series of steps calling those methods is defined - this outline *is* the workflow.
  - The methods of the WorkChain will call the functions and @calcfuncions used in Tutorial 2, which will remain unchanged.
- The input and output of the WorkChain will also be stated in the definition of this sub-class.
- The WorkChain sub-class we defined will inherit some methods and attributes from the WorkChain class, importantly:
  - `self.out` can be used to output information at any point along the WorkChain
  - the attribute `self.ctx` can be used to pass a result between methods 
  - `self.submit` must be used for any calculation being launched from within the WorkChain
- WorkChains introduce the concept of the *context*
  - the calcjob nodes returned by the calculations must be passed to the context at the end of one method
  - then, in a subsequent method, they can be used by calling `self.ctx[label_of_the_calcjob]`
  - in this way, the WorkChain knows that it has to wait for the calculations to finish before excecuting the method where `self.ctx.` is used

## Shortcut instructions

In order to code this yourself, you will need to read the AiiDA documentation on WorkChains as this list of instructions is not exhaustive and does not indicate any syntax explicitely. 
For the purpose of this tutorial, you will have to complete some statements in the code provided for this tutorial. Search for the string 'complete'.

**I strongly recommend you to identify all the changes described before in the new code.** 🧐

## Inspect the results

Use `verdi process list -ap1` and note that the WorkChain has submitted all the calculations at once and no longer blocks the termian/python interpreter.
Use `verdi process status <pk>` with the `pk` of the WorkFunction to see a tree representation of what it does, i.e., what processes it calls.

Once the WorkChain has finished, use `verdi node graph generate <pk>` with the `pk` of the WorkChain and that of one PwCalculation. See how the relationship between the different PwCalculations is displayed.
