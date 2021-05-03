# PyPlanet
Procedurally generated planets

## Goals
To generate psuedo-random planets from first principles and base values (planet, star and orbit details)

## Principle
Planetary surfaces are determined by two major mechanics
- Plate tectonics
- Erosion

These systems are driven by two separate sources (core heat and solar energy), so at the very least tectonics can be considered independent. Can theorise a system "stack":
- (souce) Solar energy
- (system) Weather/erosion
- (model) Land model (height offset)
- (model/system) Tectonic plates (global movement and drives volcanic and tectonic systems)
- (system) Mantle convection cells
- (source) Core heat

## Tectonics
Core heat powered, convection currents cause surface movement. Thus can simplify driving system down to a 2D convection cell "surface"
