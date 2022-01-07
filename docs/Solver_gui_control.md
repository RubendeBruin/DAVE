# Interactive control of the solver

It is very easy to create a model without a static equilibrium position. For example a weight without connections (falling box).

This means we need to be able to interactively stop the solver.

The `scene._solve_statics_with_optional_control` function provides that:

```
Solves statics with a time-out and feedback/terminate functions.

Specifying a time-out means that feedback / termination is evaluated every timeout_s seconds. This does not mean that the function terminates after timeout_s. In fact the function will keep trying indefinitely (no maximum number of iterations)

1. Reduce degrees of freedom: Freezes all vessels at their current heel and trim
2. Solve statics

3. Restore original degrees of freedom
4. Solve statics

5. Check geometric contacts
    if ok: Done
    if not ok: Correct and go back to 4

Options for feedback to user and termination control during solving:

feedback_func     : func(str)
do_terminate_func : func() -> bool
```

- For quick solves we
  - Do not want to show the dialog
  - Want to animate the change afterwards
- For long solves:
  - On intervals:
    - Update the scene visual
    - Update feedback
    - Evaluate possible breaks



