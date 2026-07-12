# Mechanism Design — GUI Thin-Client Proof v0.12.11

The GUI is an interface adapter, not a simulation layer:

1. `renderEnvelope` consumes existing observation/history/debrief fields;
2. `validateCommand` checks only empty input and displays server-authoritative
   command hints;
3. `createThinClient` calls an injected `submitTurn` adapter;
4. the returned envelope replaces the current display; and
5. no local state transition or parser exists.

The demo envelope is explicitly display fixture data. Production wiring remains
an adapter integration decision outside this proof.
