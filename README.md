# Split Screen Plugin for Daydream Scope

Produces a split-screen output from two video inputs:

- **video**: one frame is used for the **top** half of the output.
- **video2**: one frame is used for the **bottom** half of the output.

If only one stream is connected, the other half is filled with black. Output is a single stream (one split-screen frame per call).

Scope currently passes only the primary stream as `video`. To use two physical streams, Scope would need to support a second input (e.g. a second track) and pass it as `video2` to the pipeline.
