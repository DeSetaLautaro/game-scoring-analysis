# Data Dictionary

This project uses simulated (and later real) game data.

## votes (event-level)
One row per vote, per round, per match.

Columns:
- match_id: unique match identifier
- round_id: round number within the match
- voter_id: player who casts the vote
- target_id: player being voted
- voter_role: crew / impostor
- target_role: crew / impostor
- is_correct_vote: boolean (1 if target is impostor, else 0)
- points_vote: points earned/lost from the vote
- scoring_R: reward for correct vote
- scoring_P: penalty for incorrect vote
- scoring_S: impostor survival points per round (stored for experiment tracking)

## rounds (derived)
One row per round per match. Derived from votes and game rules.

## players (derived)
One row per player per match. Derived from votes and scoring rules.

## matches (derived)
One row per match. Derived from rounds and match configuration.
