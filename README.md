# ludograph
An open-source graph database that rips games into tiny pieces, so we can properly see and track each idea’s path through the gaming world - how it evolves and transforms, and what it influences.

## project philosophy
- Aspects of game design are represented in a succint set of atomic node classes
- Graph architecture correlates graph distance with semantic closeness
- Academic citation-esque system for relations between nodes
    - Sequels point to their predecessor, not the other way around
        - Game concepts point to their influences,
        - Compilations point to their contents, etc.
        - Games point to their corresponding supergroups (ie. series/franchise) only if the IP already existed. Inaugural games point to the supergroup(s) which they can be said to have “founded”.
    - Essentially, all things do not point “forward" in time
- Genres are not real - or rather, they have to be proven with specific mutual concepts
    - Sort of like unsupervised machine learning, we’re going to inadvertently “create” the likeness groups by way of their atomic parts, not shuffle games into pre-existing labels.
    - Historical nomenclature for genre ideas will be included as footnotes
- Any “games within games” have to be explicitly separated out
    - This includes game modes, puzzles, minigames, really anything that can be seen as an isolated challenge separate from the main gameplay loop.
    - Games with more than one disjoint gameplay style will then be treated like a compilation.


## project goals
- design a suitable graph database ontology for representing the medium of games
- create a suitable web interface for browsing and querying the database
- construct a user-driven contribution model for database additions and changes
- make the contents of the database accessible through GraphQL or similar API interface