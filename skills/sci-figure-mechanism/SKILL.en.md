---
name: sci-figure-mechanism
description: Create editable diagrams of transport, energy levels, optoelectronic conversion, reactions and competing mechanisms. Check coordinate meaning, charge/current signs, conservation and evidence strength.
---

# Mechanisms: give every line a physical meaning

List objects, initial/final states, driving forces, boundaries, observables and changes. Separate observation, computational constraint, proposed explanation and competing explanation, attaching specific sources where available. Show unresolved paths as unresolved, rather than as measured facts. Do not manufacture support by hiding unfavorable groups or emphasizing unsupported routes.

## Separate representation spaces
Distinguish device position, electron energy, reciprocal space, state barriers and reaction coordinates. State energy reference and units; identify a wave-vector path or state variable as needed. Reaction coordinates are not automatically time or distance, and energy ladders do not encode layer thickness.

Build a state table and then a process table. Injection, transport, trapping, detrapping, recombination, energy transfer and reactions are different operations. Every arrow needs an object, start, end and driving rationale. Sequence is not causation; width encodes rate only when supported.

## Physical checks
Use e− and h+ consistently. Electron particle flux and its conventional-current contribution have opposite signs; holes have the same sign. E = −∇φ; ordinary electron drift opposes E and hole drift follows it, but diffusion, built-in fields, ions and boundary conditions can change net flux. Positive applied bias alone does not determine every arrow. Open circuit means zero external net current, not zero internal transfer.

Plot higher energy upward; less-negative vacuum-referenced electron levels are higher. Separate radiative recombination from emitted photons, and carrier transport from exciton energy transfer. Check charge/material conservation, selective barriers and competing leakage/non-radiative routes. Quasi-2D n labels inorganic-layer count or phase, not spatial dimension. See [references/physics-grammar.md](references/physics-grammar.md), [references/task-cases.md](references/task-cases.md) and [references/reconstruction.md](references/reconstruction.md) as needed.

## Production and review
Choose vector, structural or 3D tools by the objects. Exact molecules/lattices require coordinates; quantitative fields require actual calculations. Generated imagery must not substitute for measurements or exact structure. Define object colors and process line styles; dashed lines need an explicit legend rather than an assumed meaning.

Read each arrow aloud: what moves from where to where, why, and with what evidence? Check polarity, frame, layer sequence, units and stoichiometry. Render and inspect at final size. Deliver editable sources, preview, state/symbol definitions and a caption distinguishing measured constraints, model and proposal. Bundled examples are DEMO, not actual devices or fixed templates.
