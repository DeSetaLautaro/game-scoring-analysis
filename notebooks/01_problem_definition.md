# Game Scoring Analysis – Problem Definition

## Objective
Evaluate whether the current scoring system of the game produces
fair and engaging outcomes for players.

## Game Description
- Multiplayer social game
- One or more impostors per match
- Players vote to eliminate impostors
- Points are awarded or penalized based on outcomes

## Scoring Rules (Initial Assumptions)
- Correct vote: +R points
- Incorrect vote: -P points
- Impostor survives a round: +S points

## Key Questions
1. Is voting accurately always the optimal strategy?
2. Do impostors gain a disproportionate advantage?
3. How does player count affect balance?
4. Are there parameter ranges that break fairness?

## Metrics to Evaluate
- Average score by role
- Score variance
- Win probability by role
- Incentive alignment

## Next Steps
- Implement a simulation of game rounds
- Run Monte Carlo experiments
- Compare different parameter settings

  ## Experiment Plan

We will compare scoring configurations defined by:
- R: points for a correct vote
- P: points penalty for an incorrect vote
- S: points for impostor survival per round

We will run Monte Carlo simulations across:
- number of players (e.g., 4 to 10)
- number of rounds (fixed or variable)
- player skill profiles (low/medium/high accuracy)

Primary outputs:
- win rate by role
- score distribution by role
- ranking stability
- incentive alignment (expected value of voting)

