# Creative system

This profile uses a **Research Mission Control** visual language rather than a generic badge wall.

## Original local assets

All primary visuals are generated deterministically from `data/profile.json` by:

```bash
python scripts/generate_visuals.py
```

The hero, current-signal panel, route cards, project covers, evidence strip, research constellation, signal path, and career timeline remain available if every external widget fails.

## External elements and graceful degradation

- **Readme Typing SVG:** a small, non-critical motion line below the hero.
- **Shields / Komarev / Skill Icons:** lightweight contact, location, view-count, and technology signals. Text around them carries the real meaning.
- **GitHub Profile 3D Contrib:** generated daily inside the repository with the built-in `GITHUB_TOKEN`; no personal access token is required for the public contribution visual.
- **GitHub Readme Stats and Streak Stats:** placed inside a collapsed secondary section because public hosted endpoints can be unavailable or rate-limited.

## Visual rules

- The primary visual hierarchy is local and original.
- Animated SVGs respect reduced-motion preferences.
- Light and dark variants use GitHub's supported `<picture>` pattern.
- Project status and metrics are manually verified before publication.
- No dynamic widget is allowed to carry a critical claim.
