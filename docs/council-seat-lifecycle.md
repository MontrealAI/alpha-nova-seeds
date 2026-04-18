# Council Seat Lifecycle (v2.6 RC)

## Lifecycle states
1. **Assigned**: seat has occupant and weight.
2. **Active delegation window**: delegations recorded for term.
3. **Challenge opened**: seat challenge bond posted.
4. **Challenge resolved**:
   - upheld => seat deactivated, challenger bond returned,
   - rejected => bond routed to treasury owner.

## Visibility requirements
- Track each challenge with open/resolved timestamps.
- Track seat active flag transitions.
- Expose open challenge count and term-level seat status.
