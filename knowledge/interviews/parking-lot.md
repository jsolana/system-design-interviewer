---
title: Parking Lot
type: interview
sources: [Cracking the Coding Interview, 6th ed., ch. 7 pp. 125-129 and solutions pp. 305-341 (problem 7.4)]
concepts: [object-oriented-design]
difficulty: medium
---

# Parking Lot

## Prompt
Design a parking lot using object-oriented principles.

## Functional requirements
- Multiple levels, each with rows of spots.
- Parks motorcycles, cars and buses.
- Spot sizes: motorcycle, compact, large. A motorcycle fits any spot; a car fits compact or large; a bus needs five consecutive large spots in one row.

## Non-functional requirements
Not covered in the source (object-oriented design; ask clarifying questions first).

## Estimations
Not covered in the source.

## API
park vehicle, find spots, clear spots, canFitInSpot(spot), level availability updates.

## Data model
Vehicle (abstract; Car, Bus, Motorcycle each implement canFitInSpot and spots needed), ParkingSpot (size, row, spotNumber, level, vehicle), Level (spots, available count, parkVehicle), ParkingLot (array of Levels).

## Architecture (high-level design)
ParkingLot is a thin wrapper over Levels; Level finds free spots (including consecutive ones for buses) and parks; ParkingSpot parks/removes a vehicle and notifies the level.

## Deep dives
- One ParkingSpot class with a size field rather than subclasses per size (spots have no different behavior).
- Separate ParkingLot from Level to keep spot-finding logic out of the top class.

## Trade-offs and decisions
- Size field vs subclasses; Vehicle-specific fit logic vs central logic.

## Related concepts
[[object-oriented-design]]

## Follow-up questions
Not covered in the source.

## Variants
Not covered in the source.
