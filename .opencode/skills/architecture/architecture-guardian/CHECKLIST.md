# Architecture Guardian Checklist

## Architecture

* [ ] Matches ARCHITECTURE.md
* [ ] No architectural drift
* [ ] Responsibilities remain clear
* [ ] Modules remain cohesive
* [ ] Coupling remains low

## Interfaces

* [ ] Interfaces remain small
* [ ] Interfaces are implementation independent
* [ ] No leaking abstractions
* [ ] No circular dependencies

## Experience

* [ ] Produces Experience objects
* [ ] Can Experiences be stored?
* [ ] Can Experiences be benchmarked?

## Assets

* [ ] Should this become a Skill?
* [ ] Should this become a Prompt?
* [ ] Should this become a Workflow?
* [ ] Should this become a Policy?
* [ ] Should this become a Benchmark?

## Evolution

* [ ] Is it versioned?
* [ ] Is it benchmarkable?
* [ ] Can it evolve?
* [ ] Can it be rolled back?

## Complexity

* [ ] Is there a simpler solution?
* [ ] Is this abstraction necessary?
* [ ] Could two modules be merged?
* [ ] Could one module be split?
