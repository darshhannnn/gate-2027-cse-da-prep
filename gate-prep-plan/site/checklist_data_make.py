#!/usr/bin/env python3
"""Generate checklist_data.json for the GATE plan website.

Content basis: official GATE 2027 syllabi (CS + DA), PYQ pattern analysis of
CSE 2017-2026 and the three DA papers (2024-2026), and the user's master
checklist structure + tier colours (kept exactly as provided).
PYQ frequencies are approximate (coaching-analysed, +-1); subtopic notes cite
only patterns that recur in the analysed papers.
"""
import json

def T(tier, topic, subs, freq, patterns, tests):
    return {"tier": tier, "topic": topic,
            "subs": [{"n": n, "p": p} for n, p in subs],
            "freq": freq, "patterns": patterns, "tests": tests}

G = []

# 1 ------------------------------------------------------------------ EM+DM
G.append({"name": "1. Engineering Mathematics & Discrete Mathematics", "note": "Common to both papers (~13-mark block in CS; feeds DA maths)",
"rows": [
T(1, "Propositional Logic and First-Order Logic", [
    ("Truth tables, connectives, tautologies", "Warm-up 1-mark material; rarely alone"),
    ("Validity, satisfiability, counter-models", "Near-yearly: decide whether a formula set is valid/satisfiable"),
    ("Equivalences, CNF/DNF, logical consequence", "Feeds resolution questions and digital-logic minimisation"),
    ("FOL: quantifiers, negation, translation", "Alternate years; 2026 CSE and DA both had FOL validity questions")],
    "7/10 years · 1–2 Qs",
    ["Decide validity/satisfiability of given formulas", "Translate English statements into FOL and negate them", "Count truth assignments / models"],
    ["20-min topic quiz after first pass (mix NAT+MSQ) — target 90%", "Add to Sunday mixed set until two clean passes"]),
T(1, "Sets, Relations, Functions, Partial Orders and Lattices", [
    ("Set operations and counting on sets", "Basic 1-mark fodder inside combinatorics"),
    ("Relations: closures, equivalence classes", "Number of equivalence relations / class sizes recur"),
    ("Functions: injective, surjective, composition", "Counting functions with constraints (DA 2026: f(f(n))=n bijections)"),
    ("POSETs, Hasse diagrams, LUB/GLB", "Hasse-diagram questions alternate years"),
    ("Lattices, monoids, groups (axioms)", "Group-axiom checks appear as quick 1-markers")],
    "6/10 years · 1–2 Qs",
    ["Hasse diagram reading", "Classify relation properties", "Count functions/relations with constraints"],
    ["Include in the weekly sectional rotation"]),
T(1, "Graphs — Connectivity, Matching, Colouring", [
    ("Handshaking, degree sequences, walks", "Degree-sum numericals are quick marks"),
    ("Connectivity, Euler and Hamiltonian", "Existence-style concept questions"),
    ("Bipartite graphs and matching (Hall's)", "Matching-size questions appear with DA graph theory"),
    ("Chromatic number and colouring bounds", "Chromatic number of standard graphs — recurring 1-mark"),
    ("Trees and basic properties", "n−1 edges, leaf counts — feeds DS tree questions")],
    "6/10 years · 1–2 Qs",
    ["Chromatic/connectivity properties", "Matching in bipartite graphs", "Counting labelled structures"],
    ["Weekly sectional inclusion"]),
T(1, "Combinatorics — Counting, Recurrence Relations, Generating Functions", [
    ("Permutations/combinations with constraints", "Every year somewhere (CSE math or DA P&S)"),
    ("Pigeonhole and inclusion–exclusion", "Standard small numericals"),
    ("Stars-and-bars / integer solutions", "DA 2026 asked it directly"),
    ("Linear recurrences (characteristic roots)", "Solve-the-recurrence appears most years"),
    ("Generating functions, coefficient extraction", "Alternate years; the classic differentiator")],
    "8/10 years · 1–2 Qs",
    ["Count with constraints", "Solve recurrences", "Extract coefficients from generating functions"],
    ["Timed 10-question counting drill weekly in Phase 1"]),
T(1, "Linear Algebra — Matrices, Determinants, Systems of Linear Equations", [
    ("Rank and consistency of linear systems", "Consistency/parametric solutions recur in both papers"),
    ("Determinants and their properties", "Trick determinants (DA 2024: det(M²+12M))"),
    ("Special matrices: idempotent, orthogonal, I+uvᵀ", "DA 2025: rank of I+xxᵀ; shortcut family worth memorising"),
    ("Gaussian elimination", "DA 2025 asked its operation count")],
    "8/10 years · 2 Qs",
    ["Solve/characterise systems", "Determinant shortcuts", "Rank arguments without full computation"],
    ["20-min quiz after first pass; re-solve misses at day 7"]),
T(1, "Linear Algebra — Eigenvalues and Eigenvectors", [
    ("Computing eigenvalues (2×2/3×3)", "Direct computation almost every year across both papers"),
    ("Diagonalization and powers Aⁿ", "DA 2026: rotation matrix M^2026"),
    ("Trace/det = sum/product of eigenvalues", "Shortcut used inside many numericals"),
    ("Eigen-structure of projections/stochastic matrices", "Ties into PCA (DA ML) questions")],
    "8/10 years · 1–2 Qs",
    ["Compute eigen-pairs fast", "Aⁿ without multiplying", "Eigen-based arguments about rank/invertibility"],
    ["Include in Saturday mixed set"]),
T(2, "Linear Algebra — LU Decomposition, Rank, Nullity", [
    ("LU decomposition steps", "Mechanical; know the count of operations"),
    ("Rank–nullity theorem", "Direct application numericals"),
    ("Subspace dimensions in R³", "DA 2024 and 2026 both asked subspace identification")],
    "4/10 years · 1 Q",
    ["Dimension counting", "Decomposition mechanics"],
    ["Fold into the Linear Algebra topic quiz"]),
T(1, "Probability — Conditional Probability and Bayes Theorem", [
    ("Conditional probability and independence", "Foundation for nearly every probability question"),
    ("Bayes theorem (boxes, disease tests)", "DA 2025 3-boxes; DA 2026 disease testing; CSE recurring"),
    ("Law of total probability", "Inside most Bayes numericals"),
    ("Joint, marginal, conditional probability", "DA asks marginal/conditional nearly every year")],
    "9/10 years · 2–3 Qs",
    ["Bayes with base rates", "Independence factorisation checks (DA 2024)", "Total-probability partitions"],
    ["This is the highest-ROI quiz in the plan — 20-min drill weekly"]),
T(1, "Probability Distributions — Uniform, Normal, Exponential, Poisson, Binomial", [
    ("Bernoulli and binomial", "Estimator-style questions (DA 2025 unbiased p̂)"),
    ("Poisson: mean=variance, merging, limits", "DA 2024 identity; DA 2026 Poisson-limit sum"),
    ("Exponential and memorylessness", "DA 2026: P(X>10|X>5) — the classic trap"),
    ("Normal and standard normal", "Standardisation numericals; ties into CLT"),
    ("Uniform (discrete/continuous)", "Baseline for conditional-uniform questions (DA 2026)")],
    "9/10 years · 2–3 Qs",
    ["Recognise the distribution, then compute", "Memorylessness and merging properties", "Standardisation"],
    ["Distribution-recognition drill: 15 mixed questions weekly"]),
T(1, "Mean, Median, Mode, Standard Deviation, Variance", [
    ("Descriptive statistics computation", "Quick 1-markers in both papers"),
    ("Variance identities: E[X²], ΣΣ(xᵢ−xⱼ)²", "DA 2026 used the pairwise-sum identity"),
    ("Correlation and covariance basics", "DA 2024 and 2026 correlation questions")],
    "6/10 years · 1 Q",
    ["Compute/compare moments", "Variance identity shortcuts"],
    ["Fold into probability drill"]),
T(2, "Calculus — Limits, Continuity, Differentiability, Maxima and Minima", [
    ("Algebraic limits and expansions", "DA 2025: lim(√(t²+t)−t); CSE lighter"),
    ("Piecewise continuity/differentiability", "DA 2024 piecewise continuity; 2025 product/composition"),
    ("Maxima/minima via second-derivative test", "DA all three years (quartic/cubic/cubic)"),
    ("Mean value theorem (use, not proof)", "Occasional concept question")],
    "5/10 years (CS) · heavier in DA",
    ["Critical points and classification", "Differentiability checks at joints"],
    ["Fold into Calculus & Optimisation quiz (DA group 12)"]),
T(3, "Calculus — Mean Value Theorem, Integration", [
    ("Definite integral properties", "Occasional 1-mark"),
    ("Area under simple curves", "Rare direct; supports probability densities"),
    ("MVT applications", "Statement-level questions only")],
    "3/10 years · ≤1 Q",
    ["Integral properties", "Density-based areas"],
    ["Low priority: solve PYQs once, no drill needed"]),
]})

# 2 ------------------------------------------------------------------ PDSA
G.append({"name": "2. Programming, Data Structures and Algorithms", "note": "Common core — highest return for both papers (~16–18 marks in CS)",
"rows": [
T(1, "Programming in C (and Python for the DA paper) — Recursion", [
    ("C: pointers, arrays, parameter passing, scope", "C output-tracing is asked every single year (3–5 Qs)"),
    ("C: dynamic memory, structs, sizeof traps", "sizeof array-vs-pointer and malloc patterns recur"),
    ("Recursion: call trees, counting calls", "Call-count and return-value tracing every year"),
    ("Python: closures, mutable default arguments", "DA 2026: mutable default — the classic trap"),
    ("Python: list/set/dict behaviour, slicing", "2–4 Python output questions per DA paper")],
    "10/10 years · 3–5 Qs",
    ["Trace the exact output", "Count recursive calls", "Spot aliasing/mutation effects"],
    ["Daily 30-min tracing drill through Phase 1–2 (this tab's single best habit)"]),
T(1, "Arrays, Stacks, Queues, Linked Lists", [
    ("Multi-dimensional array addressing", "Row/column-major address numericals, alternate years"),
    ("Stack applications: expression evaluation", "Postfix/infix evaluation and stack traces"),
    ("Circular queues and deques", "DA 2024 asked deque operation sequences"),
    ("Linked-list pointer manipulation", "Pointer-swap/output questions alternate years")],
    "8/10 years · 1–2 Qs",
    ["Trace data-structure operation sequences", "Address calculation", "Spot pointer bugs"],
    ["Include in the weekly programming drill"]),
T(1, "Trees — Binary Trees, Binary Search Trees", [
    ("Traversals (pre/in/post/level)", "Every year in some form across both papers"),
    ("BST insert/delete/search", "Comparison counts and resulting shapes"),
    ("Construction from pre+in / post+in", "DA 2026 asked reconstruction"),
    ("Full/complete binary tree relations", "DA 2024: height vs internal vs leaf counts"),
    ("Heaps as trees (bridge to next topic)", "Feeds priority-queue questions")],
    "9/10 years · 1–2 Qs",
    ["Reconstruct trees from orders", "Count comparisons/nodes", "Identify valid BST sequences"],
    ["Topic quiz after first pass; add to Sunday mixed set"]),
T(1, "Heaps and Priority Queues", [
    ("Heapify, insert, delete-min", "Element-comparison counting recurs"),
    ("Build-heap complexity", "O(n) vs O(n log n) distinction — classic MCQ"),
    ("Heapsort and k-largest elements", "Conceptual frequency"),
    ("d-heaps / k-way merge (light)", "Rare; know the idea")],
    "6/10 years · 1 Q",
    ["Trace heap operations", "Count comparisons", "Complexity distinctions"],
    ["Include in DS sectional"]),
T(1, "Graphs — Representation, Traversals (BFS, DFS)", [
    ("Adjacency matrix vs list trade-offs", "1-mark property questions"),
    ("BFS/DFS mechanics and complexity", "DA 2024 DFS properties; DA 2026 DFS question"),
    ("Connected components, cycles, bipartiteness", "Applications appear as twist questions"),
    ("Topological sort of DAGs", "DA 2024: count valid orderings")],
    "8/10 years · 1–2 Qs",
    ["Trace traversal orders", "Count orderings/components", "Complexity under both representations"],
    ["Graph drill fortnightly"]),
T(1, "Hashing", [
    ("Chaining and load factor", "Expected search cost numericals"),
    ("Open addressing: linear/double/uniform probing", "DA 2024 uniform hashing; DA 2025 linear-probing trace"),
    ("Hash function properties", "Simple 1-markers")],
    "6/10 years · 1 Q",
    ["Count probes exactly", "Load-factor formulas"],
    ["Trace 20 probe-sequence problems across prep"]),
T(1, "Searching and Sorting Algorithms", [
    ("Binary search variants and comparison counts", "DA 2025: array vs linked-list binary search"),
    ("Insertion/selection/bubble counts", "DA 2025: insertion-sort swap count; DA 2026 bubble vs insertion"),
    ("Merge sort and quicksort behaviour", "DA 2026: first-element-pivot quicksort; 2024 in-place quicksort"),
    ("Stability and in-place properties", "DA 2024 sort-stability question; recurring MCQ")],
    "9/10 years · 1–2 Qs",
    ["Count comparisons/swaps exactly", "Match algorithm to property", "Trace one partition pass"],
    ["Sorting-property flashcards + fortnightly drill"]),
T(1, "Asymptotic Worst-Case Time and Space Complexity", [
    ("O/Ω/Θ comparisons of functions", "Near-every-year ranking question"),
    ("Running time of code snippets", "Loop-analysis 1–2 markers"),
    ("Best vs worst vs average case", "Sorting/algorithm-specific cases")],
    "9/10 years · 1–2 Qs",
    ["Rank functions by growth", "Analyse nested loops", "Identify amortised twists"],
    ["Flashcards + include in every sectional"]),
T(1, "Algorithm Design — Divide and Conquer", [
    ("Merge sort recurrence", "Standard Master-theorem application"),
    ("Master theorem cases", "Recurrence questions most years"),
    ("Recursion-tree/substitution methods", "When Master theorem doesn't apply — CSE 2026 favourite")],
    "6/10 years · 1 Q",
    ["Solve recurrences", "Recognise non-standard forms"],
    ["Fold into complexity drill"]),
T(1, "Algorithm Design — Greedy Algorithms", [
    ("Huffman coding cost", "Huffman tree construction numericals recur"),
    ("Activity selection / interval scheduling", "Conceptual exchange-argument questions"),
    ("Greedy correctness intuition", "2026 CSE-style: when greedy fails"),
    ("Greedy basis of MST", "Bridge to graph algorithms")],
    "6/10 years · 1 Q",
    ["Build Huffman trees", "Spot greedy counter-examples"],
    ["Include in algorithms sectional"]),
T(1, "Algorithm Design — Dynamic Programming", [
    ("Standard DP problems (knapsack family)", "Conceptual state-design questions"),
    ("Counting with DP", "Number-of-ways formulations"),
    ("DP vs greedy vs divide-conquer", "2026 CSE asked a non-standard DP — the separator"),
    ("Memoisation mechanics", "Subdependency tracing")],
    "5/10 years · 1–2 Qs",
    ["Define states correctly", "Count solutions", "Prove optimal substructure informally"],
    ["Solve 30 classic DP PYQs topic-wise; no cramming"]),
T(1, "Graph Algorithms — Minimum Spanning Tree, Shortest Paths", [
    ("Prim and Kruskal traces", "MST edge-selection and uniqueness questions"),
    ("Dijkstra", "2026 CSE: modified Dijkstra — hardest question of the paper"),
    ("Dijkstra with negative edges", "Why-it-fails conceptual staple"),
    ("Bellman-Ford and unweighted BFS shortest paths", "Property comparisons recur"),
    ("Topological shortest paths (DAG)", "Occasional twist")],
    "9/10 years · 1–2 Qs",
    ["Trace algorithms step-by-step", "Prove/disprove properties", "Modified-algorithm analysis"],
    ["The single most important algorithms quiz — fortnightly full drill"]),
]})

# 3 ------------------------------------------------------------------ COA
G.append({"name": "3. Computer Organization and Architecture", "note": "Mainly Computer Science paper (~9 marks; the rank-decider)",
"rows": [
T(1, "Machine Instructions and Addressing Modes", [
    ("Instruction formats and encoding", "Instruction-size/field numericals"),
    ("Addressing modes and effective addresses", "Identify mode / compute EA — recurring"),
    ("Instruction counts and CPI", "Program-mix CPI numericals")],
    "6/10 years · 1 Q",
    ["Compute effective addresses", "CPI from instruction mix"],
    ["Topic quiz after first pass"]),
T(1, "Arithmetic Logic Unit, Datapath and Control Unit", [
    ("Ripple-carry vs carry-lookahead adders", "Delay-comparison numericals"),
    ("ALU operations and flags", "Occasional 1-mark"),
    ("Hardwired vs microprogrammed control", "Microinstruction sequencing appears alternate years")],
    "4/10 years · 1 Q",
    ["Adder delay arithmetic", "Micro-program sequencing"],
    ["Light drill; fold into COA sectional"]),
T(1, "Instruction Pipelining and Pipeline Hazards", [
    ("Ideal speedup and stage balancing", "Speedup numericals nearly every year"),
    ("Data hazards, forwarding, stalls", "The signature COA question — ~9/10 years"),
    ("Control hazards and branch handling", "Branch-penalty calculations"),
    ("Structural hazards and multi-cycle units", "Occasional twist"),
    ("Operand forwarding vs register-file write", "Exact-cycle tracing in 2026-style questions")],
    "9/10 years · 2 Qs",
    ["Count exact cycles with/without forwarding", "Compute throughput/speedup", "Reorder code to avoid stalls"],
    ["COA's must-drill: 25 numericals topic-wise, re-solve misses weekly"]),
T(1, "Memory Hierarchy — Cache Memory", [
    ("Direct/set-associative mapping and fields", "Tag/index/offset split — near-every-year"),
    ("Hit/miss, AMAT, multi-level caches", "2026 CSE: multi-level cache numerical"),
    ("Replacement and write policies", "Write-through vs write-back effects"),
    ("Cache vs virtual-memory interplay", "2026 cross-subject: cache + multi-level paging")],
    "9/10 years · 2 Qs",
    ["Compute AMAT exactly", "Split address fields", "Count misses for access patterns"],
    ["Second must-drill: 25 numericals + formula card"]),
T(2, "Main Memory and Secondary Storage", [
    ("DRAM vs SRAM organisation", "Occasional 1-mark"),
    ("Memory interfacing and chip selection", "Rare direct"),
    ("Disk geometry, access time", "Disk-parameters numericals alternate years")],
    "3/10 years · 1 Q",
    ["Access-time decomposition", "Bandwidth calculations"],
    ["PYQs once; skip deep drilling"]),
T(2, "I/O Interface — Interrupt and DMA", [
    ("Interrupt-driven I/O and overhead", "Cycle-count numericals alternate years"),
    ("DMA cycle stealing", "Transfer-time numericals"),
    ("Polling vs vectored interrupts", "Conceptual 1-mark")],
    "4/10 years · 1 Q",
    ["Count I/O cycles", "Compare polling/interrupt/DMA overhead"],
    ["Fold into COA sectional"]),
]})

# 4 ------------------------------------------------------------------ OS
G.append({"name": "4. Operating Systems", "note": "Mainly Computer Science paper (~8–9 marks, consistently high)",
"rows": [
T(1, "Processes, Threads and Inter-Process Communication", [
    ("Process states and transitions", "State-diagram questions occasionally"),
    ("fork() and process trees", "fork-output counting is a recurring favourite"),
    ("Threads: user vs kernel, shared state", "Conceptual 1–2 marks"),
    ("System calls and IPC primitives", "Light conceptual")],
    "5/10 years · 1 Q",
    ["Count fork-created processes", "Identify shared vs private memory"],
    ["Fold into OS sectional"]),
T(1, "CPU Scheduling Algorithms", [
    ("FCFS, SJF, SRTF, Priority, Round-Robin", "Gantt-chart numericals nearly every year"),
    ("Waiting/turnaround/response time", "Always part of the above"),
    ("Preemption effects and convoy avoidance", "Comparison questions"),
    ("Context switches and quantum choice", "Counting context switches — trap-rich")],
    "8/10 years · 1–2 Qs",
    ["Build exact Gantt charts", "Compute all three time metrics", "RR quantum effects"],
    ["Scheduling drill: 20 numericals topic-wise"]),
T(1, "Concurrency, Synchronisation and Deadlock", [
    ("Critical-section requirements", "Property-checking questions"),
    ("Semaphores and classical problems", "Producer-consumer/reader-writer variants recur"),
    ("Race-condition analysis", "2026 CSE: interleaving analysis"),
    ("Deadlock conditions and RAG", "RAG cycle questions alternate years"),
    ("Banker's algorithm, safe sequences", "Safe-sequence numericals; 'safe ≠ all orders' trap")],
    "9/10 years · 2 Qs",
    ["Trace semaphore-guided executions", "Detect race conditions", "Banker's safe-sequence check"],
    ["Sync drill: 20 problems + trap list review"]),
T(1, "Memory Management and Virtual Memory", [
    ("Paging and address translation", "Page-number/offset split numericals"),
    ("Page replacement: FIFO/LRU/Optimal, Belady", "Reference-string traces nearly every year"),
    ("TLB, EMAT, multi-level paging", "2026 CSE: multi-level paging + cache combined"),
    ("Segmentation and fragmentation", "Conceptual + small numericals"),
    ("Demand paging and thrashing", "Working-set concept questions")],
    "8/10 years · 2 Qs",
    ["EMAT with TLB hit ratios (don't double-count!)", "Replacement traces", "Multi-level translation"],
    ["Paired with COA cache drill — same formula family"]),
T(2, "File Systems", [
    ("Allocation: contiguous, linked, indexed", "Max-file-size indexed numericals"),
    ("Unix inodes", "Inode pointer-structure questions — rising trend"),
    ("Directories and free-space management", "Light conceptual")],
    "5/10 years · 1 Q",
    ["Compute max file sizes", "Count disk accesses for a path lookup"],
    ["Rising topic: solve all decade PYQs here"]),
]})

# 5 ------------------------------------------------------------------ CN
G.append({"name": "5. Computer Networks", "note": "Mainly Computer Science paper (~8 marks); 2027 syllabus trimmed — follow this list",
"rows": [
T(1, "Layering and Protocol Principles", [
    ("OSI vs TCP/IP layering", "1-mark conceptual; know what each layer does"),
    ("Encapsulation and header overhead", "Small efficiency numericals"),
    ("Circuit vs packet vs virtual-circuit switching", "Delay-comparison numericals alternate years")],
    "4/10 years · 1 Q",
    ["Map functions to layers", "Switching delay comparisons"],
    ["Fold into CN sectional"]),
T(1, "IP Addressing, CIDR and NAT", [
    ("Subnetting and host counts", "The perennial quick-mark numerical"),
    ("CIDR aggregation/supernetting", "Prefix-merging questions"),
    ("Fragmentation and MTU", "Fragment-offset/size numericals"),
    ("NAT translation basics", "Light; in 2027 syllabus explicitly")],
    "8/10 years · 1–2 Qs",
    ["Subnet math without a calculator", "Aggregate prefixes", "Fragment reassembly sizing"],
    ["30-problem subnetting drill until 100% automatic"]),
T(1, "Routing — Distance Vector and Link State", [
    ("DV table updates", "Distance-vector iteration questions"),
    ("Count-to-infinity and fixes", "Classic conceptual"),
    ("Link-state + Dijkstra", "Overlaps algorithms; cost numericals")],
    "6/10 years · 1 Q",
    ["One DV exchange trace", "LS vs DV property comparison"],
    ["Fold into CN sectional"]),
T(1, "TCP and UDP — Flow Control and Congestion Control", [
    ("Sliding window and sequence numbers", "Window-size/throughput numericals; SYN/FIN counting trap"),
    ("Slow start and AIMD traces", "2026 CSE: congestion-window tracing"),
    ("RTT, timeouts, retransmission", "RTO arithmetic numericals"),
    ("TCP connection management", "Handshake sequence-number trap"),
    ("UDP basics", "Trimmed in 2027 syllabus — light prep")],
    "8/10 years · 1–2 Qs",
    ["Trace cwnd evolution", "Window/throughput math", "Seq/ack number accounting"],
    ["TCP drill: 20 numericals; pair with subnetting drill"]),
T(2, "Data Link Layer — Framing, Error Detection, MAC", [
    ("Framing, byte/bit stuffing", "Stuffing-count questions alternate years"),
    ("CRC and checksum division", "CRC-polynomial division numericals"),
    ("Hamming distance and codes", "Min-distance/parity questions"),
    ("Ethernet CSMA-CD and backoff", "Backoff-window conceptual numericals")],
    "5/10 years · 1 Q",
    ["CRC division without errors", "Hamming-distance arguments"],
    ["Fold into CN sectional"]),
T(3, "Application Layer — DNS, HTTP, SMTP, FTP", [
    ("DNS resolution flow", "1-mark conceptual"),
    ("HTTP basics and pipelining", "Object-fetch time numericals occasionally"),
    ("SMTP/FTP/email flow", "Trimmed in 2027 syllabus — skim only")],
    "4/10 years · ≤1 Q",
    ["Resolution order", "HTTP timing basics"],
    ["PYQs once; no drilling"]),
]})

# 6 ------------------------------------------------------------------ DBMS
G.append({"name": "6. Database Management Systems", "note": "Common — extra warehousing for the DA paper; DA's fastest-rising section (8→18 marks)",
"rows": [
T(1, "Entity Relationship Model", [
    ("Entities, attributes, key constraints", "Foundational for mapping questions"),
    ("Cardinality and participation", "DA 2026: referential-integrity question"),
    ("ER-to-relational mapping", "DA 2026: ER→3NF with multivalued attribute"),
    ("Weak entities and ISA hierarchies", "Occasional conceptual")],
    "5/10 years · 1 Q",
    ["Convert ER → tables correctly", "Handle multivalued/weak constructs"],
    ["Fold into DBMS sectional"]),
T(1, "Relational Model — Relational Algebra, Tuple Calculus, SQL", [
    ("Relational algebra operators", "Both papers nearly every year; DA 2025 division"),
    ("Tuple relational calculus", "DA 2026 TRC count question"),
    ("SQL joins and nested/correlated subqueries", "Every year; DA 2026 correlated COUNT"),
    ("Aggregation, GROUP BY, HAVING", "Combined with joins in most SQL questions"),
    ("NULL semantics and DDL", "DA 2025: DDL/keys/NULL question")],
    "9/10 years · 2 Qs",
    ["Translate SQL ↔ algebra", "Evaluate correlated subqueries row-by-row", "NULL three-valued logic"],
    ["SQL drill weekly — write every query by hand"]),
T(1, "Integrity Constraints and Normal Forms", [
    ("PK/FK/CHECK constraints", "Quick conceptual marks"),
    ("FDs and Armstrong closure", "Closure arithmetic — where silly marks die"),
    ("Candidate keys", "Key-finding under partial FDs — every year"),
    ("2NF/3NF/BCNF decomposition", "Lossless + dependency-preserving checks; DA 2025 JOIN decomposition"),
    ("Multivalued dependencies / 4NF (light)", "Rare; know the definition")],
    "9/10 years · 2 Qs",
    ["Compute closures fast and clean", "Find all candidate keys", "Judge decompositions"],
    ["Normalization drill: 25 problems; show every closure step"]),
T(1, "Indexing — B Trees and B+ Trees", [
    ("Order, max keys/pointers", "DA 2026 asked two B+ tree questions"),
    ("Height and occupancy", "Height-bound numericals"),
    ("B+ tree insert/delete and splits", "Structure-tracing questions"),
    ("Index vs scan cost", "Query-cost comparison occasionally")],
    "6/10 years · 1–2 Qs",
    ["Order/height arithmetic", "Trace insertions with splits"],
    ["Include in DBMS sectional"]),
T(1, "Transactions and Concurrency Control", [
    ("ACID properties", "1-mark conceptual"),
    ("Conflict and view serializability", "Schedule analysis nearly every year"),
    ("Recoverability, cascadeless schedules", "Classification questions"),
    ("2PL and lock variants", "2PL-strictness comparisons")],
    "8/10 years · 1–2 Qs",
    ["Build precedence graphs", "Classify schedules", "Spot blind writes"],
    ["Serializability drill: 20 schedules"]),
T(2, "File Organisation", [
    ("Heap/sorted/hash file organisation", "Light conceptual"),
    ("Records, blocking factor", "Occasional small numerical"),
    ("Unspanned vs spanned records", "1-mark")],
    "3/10 years · ≤1 Q",
    ["Blocking-factor arithmetic"],
    ["PYQs once"]),
T(2, "Data Warehousing — Multidimensional Models (DA paper)", [
    ("Star and snowflake schemas", "Schema-identification questions"),
    ("Concept hierarchies and cuboid counts", "DA 2026: number of data cuboids"),
    ("OLAP: ROLLUP/CUBE", "DA 2025: GROUP BY CUBE tuple count"),
    ("Measures: categorisation and computation", "Additive/semi-additive distinctions")],
    "2/3 DA years · 2–4 Qs and rising",
    ["Count cuboids from hierarchies", "Predict CUBE output sizes"],
    ["DA-specific: make a 1-page cuboid-formula card"]),
]})

# 7 ------------------------------------------------------------------ TOC
G.append({"name": "7. Theory of Computation", "note": "Mainly Computer Science paper (~8 marks; most stable subject)",
"rows": [
T(1, "Regular Expressions and Finite Automata", [
    ("RE ↔ NFA ↔ DFA conversions", "Design questions nearly every year"),
    ("DFA minimisation", "Minimum-state questions alternate years"),
    ("Closure properties of regular languages", "Closure-trap MCQs (complement/intersection)"),
    ("Language descriptions from REs", "Which-language-is-this MCQs"),
    ("Number of states / Myhill-Nerode intuition", "Occasional counting question")],
    "9/10 years · 2 Qs",
    ["Convert and minimise quickly", "Apply closure rules correctly"],
    ["TOC drill: 30 design problems topic-wise"]),
T(1, "Context-Free Grammars and Push-Down Automata", [
    ("Derivations, parse trees, ambiguity", "Ambiguity demonstration recurs"),
    ("CFG simplification and CNF", "Conversion numericals"),
    ("PDA design and acceptance modes", "Design + language matching"),
    ("DPDA vs NPDA, DCFLs", "Property MCQs"),
    ("Closure properties of CFLs", "The complement/intersection trap — recurring")],
    "8/10 years · 2 Qs",
    ["Design grammars for languages", "Check ambiguity", "Apply CFL closures correctly"],
    ["Pair with regular-language drill"]),
T(2, "Pumping Lemma", [
    ("Regular pumping lemma proofs", "Non-regularity proofs alternate years"),
    ("CFL pumping lemma", "Same trap structure for CFLs"),
    ("Logic-direction pitfalls", "The lemma disproves, never proves — classic trap")],
    "5/10 years · 1 Q",
    ["Choose the right decomposition", "Contradiction structure"],
    ["Do all decade pumping-lemma PYQs once"]),
T(2, "Turing Machines and Undecidability", [
    ("TM model, RE vs recursive languages", "Language-class membership MCQs"),
    ("Decidability and reductions", "Rising trend in the last 5 years"),
    ("Rice's theorem", "2026 CSE: direct Rice's theorem question"),
    ("Closure of language classes", "Decidable/recognizable closure traps")],
    "6/10 years · 1 Q and rising",
    ["Classify languages", "Build simple reductions", "Apply Rice's theorem correctly"],
    ["Don't skip this — it's the modern differentiator"]),
]})

# 8 ------------------------------------------------------------------ CD
G.append({"name": "8. Compiler Design", "note": "Mainly Computer Science paper (~5–6 marks; parsing carries most of it)",
"rows": [
T(3, "Lexical Analysis", [
    ("Tokens, lexemes, patterns", "1-mark conceptual"),
    ("Regex → NFA (Thompson construction)", "Overlaps TOC; occasional construction question"),
    ("Symbol table and buffering", "Skim-level")],
    "4/10 years · ≤1 Q",
    ["Tokenise a snippet", "Recognise lexical vs syntax errors"],
    ["PYQs once"]),
T(2, "Parsing — Top-Down and Bottom-Up", [
    ("FIRST/FOLLOW computation", "Feeds every parsing question — arithmetic must be clean"),
    ("LL(1) conditions and tables", "2026 CSE: LL(1) preconditions question"),
    ("LR(0) items and SLR tables", "Item-set construction numericals"),
    ("CLR(1)/LALR construction and conflicts", "2026 CSE: LALR conflict question; conflict counting recurs"),
    ("Shift-reduce mechanics", "Handle-pricing traces occasionally")],
    "8/10 years · 1–2 Qs",
    ["Build tables without arithmetic slips", "Count and classify conflicts"],
    ["Parsing drill: 20 table problems — CD's marks live here"]),
T(3, "Intermediate Code Generation", [
    ("Three-address code, quadruples", "Translate-snippet questions alternate years"),
    ("Assignment/loop translation", "Standard forms"),
    ("Boolean expression code", "Backpatching idea occasionally")],
    "5/10 years · 1 Q",
    ["Emit 3-address code by hand"],
    ["PYQs once + one practice set"]),
T(3, "Runtime Environments", [
    ("Activation records and call stacks", "Activation-tree questions occasionally"),
    ("Parameter passing conventions", "Value vs reference effects — ties to C tracing"),
    ("Heap management basics", "Skim")],
    "3/10 years · ≤1 Q",
    ["Track activation records across calls"],
    ["PYQs once"]),
T(3, "Data Flow Analysis — Liveness, Constant Propagation", [
    ("Liveness and live ranges", "New explicit syllabus item — expect growth"),
    ("Constant propagation", "Same"),
    ("Available expressions / CSE", "Same"),
    ("Reaching definitions (idea)", "Foundation for the above")],
    "2/10 years · new in syllabus",
    ["Compute IN/OUT sets on small CFGs"],
    ["Learn the framework once; do whatever PYQs exist"]),
]})

# 9 ------------------------------------------------------------------ DL
G.append({"name": "9. Digital Logic", "note": "Mainly Computer Science paper (~5 marks; highest marks-per-hour in the paper)",
"rows": [
T(3, "Boolean Algebra and Minimisation", [
    ("Algebraic simplification", "Warm-up for K-map questions"),
    ("K-maps with don't-cares", "Nearly every year — fast marks"),
    ("SOP/POS forms and tabulation idea", "Occasional direct question")],
    "7/10 years · 1 Q",
    ["Minimise 3–4 variable functions", "Handle don't-cares correctly"],
    ["Speed drill: 15 K-maps"]),
T(3, "Combinational and Sequential Circuits", [
    ("Adders, MUX, decoders", "MUX-implementation-of-function questions"),
    ("Flip-flops and excitation tables", "State-tracing foundations"),
    ("Counters and sequence generators", "Counter-state tracing alternate years"),
    ("State machines and diagrams", "FSM design occasionally")],
    "6/10 years · 1 Q",
    ["Trace flip-flop outputs cycle-by-cycle", "Implement functions with MUXes"],
    ["Include in DL sectional"]),
T(3, "Number Representations and Computer Arithmetic", [
    ("1's/2's complement and ranges", "Range/overflow numericals nearly every year"),
    ("Overflow detection", "Signed-arithmetic trap questions"),
    ("IEEE-754 single/double", "Bias, normalisation, denormals — recurring numerical"),
    ("Fixed-point representation", "Occasional")],
    "6/10 years · 1 Q",
    ["Convert/represent exactly", "IEEE-754 encode-decode both ways"],
    ["Make the IEEE-754 formula card — it always pays"]),
]})

# 10 ----------------------------------------------------------------- P&S
G.append({"name": "10. Probability and Statistics", "note": "Extra depth for the DA paper (~16–19 marks — its anchor section); also helps CS",
"rows": [
T(1, "Random Variables — Discrete and Continuous", [
    ("PMF/PDF/CDF and their properties", "DA 2026: CDF property statements"),
    ("Expectation and variance", "Core of most DA probability numericals"),
    ("Transformations of RVs", "DA 2025: floor of exponential → geometric"),
    ("Functions of RVs (Z=X+Y etc.)", "Moment computations recur")],
    "3/3 DA years · 3–4 Qs",
    ["Switch between PMF/PDF/CDF fluidly", "Compute moments of transformed RVs"],
    ["The DA anchor drill: 20 problems weekly until Phase 3"]),
T(1, "Joint, Marginal and Conditional Distributions", [
    ("Joint PMF/PDF tables and functions", "Normalisation numericals"),
    ("Marginalisation", "Always part of joint questions"),
    ("Conditional distributions and PDFs", "DA 2024: E[Y|X] from joint pdf"),
    ("Independence verification", "Factorisation checks (DA 2024)")],
    "3/3 DA years · 2–3 Qs",
    ["Marginalise correctly", "Condition and renormalise"],
    ["Include in the DA anchor drill"]),
T(1, "Correlation, Covariance, Conditional Expectation", [
    ("Covariance and correlation computation", "DA 2024 coin-RV correlation; DA 2026 conditional-uniform correlation"),
    ("Tower rule: E[E[X|Y]]", "DA 2025 direct question"),
    ("Conditional variance", "Pairs with tower rule"),
    ("Variance identities", "DA 2026 ΣΣ(xᵢ−xⱼ)² identity")],
    "3/3 DA years · 2 Qs",
    ["Apply tower rule cleanly", "Expand variances via identities"],
    ["Add to anchor drill"]),
T(1, "Central Limit Theorem", [
    ("Sums and means of i.i.d. RVs", "DA 2025: CLT for a Bernoulli(0.25) sum"),
    ("Normal approximation validity", "n-too-small trap"),
    ("Sample-mean distribution", "DA 2026: distribution of the sample mean")],
    "2/3 DA years · 1 Q",
    ["Standardise sums/means", "Judge when CLT applies"],
    ["Include in anchor drill"]),
T(2, "Confidence Intervals and Hypothesis Testing", [
    ("z and t intervals", "Syllabus-explicit; expect growth"),
    ("One/two-tailed tests, p-values", "Direction traps"),
    ("Type I/II errors", "Conceptual 1-markers"),
    ("Choosing the right test", "z vs t vs χ² decision rule")],
    "2/3 DA years · 1–2 Qs",
    ["Pick test and df correctly", "Read p-value direction"],
    ["Make a test-selection decision card"]),
T(2, "t-distribution and Chi-squared Distribution", [
    ("t distribution shape and use cases", "Small-sample tests"),
    ("χ² goodness-of-fit and independence", "df rules are the trap"),
    ("Sampling distributions (idea)", "Underpins the above")],
    "1/3 DA years · ≤1 Q",
    ["df arithmetic", "Match distribution to scenario"],
    ["Fold into hypothesis-testing drill"]),
]})

# 11 ----------------------------------------------------------------- LA
G.append({"name": "11. Linear Algebra", "note": "Extra depth for the DA paper (~8–11 marks); shared with CS maths",
"rows": [
T(1, "Vector Spaces, Subspaces, Linear Dependence and Independence", [
    ("Subspaces of R³", "DA 2024 and 2026 both asked subspace identification"),
    ("Spanning sets and bases", "DA 2025: orthonormal bases"),
    ("Rank–nullity and dimension counting", "Direct numericals"),
    ("Row-stochastic matrices and systems", "DA 2025: Bx=0 structure question")],
    "3/3 DA years · 2 Qs",
    ["Test subspace axioms fast", "Count dimensions"],
    ["20-problem drill after first pass"]),
T(1, "Eigenvalues, Eigenvectors, Determinant", [
    ("Eigen computation and properties", "DA eigen questions every year"),
    ("Powers via diagonalization", "DA 2026: rotation matrix M^2026"),
    ("Determinant tricks", "DA 2024: det(M²+12M)"),
    ("Polynomial constraints on A", "DA 2025: A³=A structure"),
    ("Gram matrices and quadratic forms", "DA 2025/2026; Rayleigh quotient 2026")],
    "3/3 DA years · 2–3 Qs",
    ["Shortcut eigen-arguments", "Avoid full computation where possible"],
    ["Make the special-matrices card (rotation/idempotent/orthogonal/projection)"]),
T(2, "Singular Value Decomposition and Projections", [
    ("Singular values", "DA 2024: rank-1 uuᵀ; DA 2025: singular values of a projection"),
    ("Projection matrices and least squares", "Bridge into regression"),
    ("Norm-preservation and orthogonality", "DA 2025: norm-preserving ⟹ orthogonal"),
    ("Quadratic forms and Rayleigh quotient", "DA 2026: max xᵀAx")],
    "2/3 DA years · 1–2 Qs",
    ["Compute singular values of small matrices", "Project vectors correctly"],
    ["Include in LA drill"]),
]})

# 12 ----------------------------------------------------------------- Calc
G.append({"name": "12. Calculus and Optimisation", "note": "Data Science paper (~5–9 marks, shrinking — cap your time here)",
"rows": [
T(2, "Functions of a Single Variable — Limits, Continuity, Differentiability", [
    ("Algebraic limits and expansions", "DA 2025: lim(√(t²+t)−t)"),
    ("Piecewise continuity", "DA 2024 continuity question"),
    ("Differentiability of products/compositions", "DA 2025 statement question"),
    ("Lipschitz-style statements", "DA 2025: |f(x)−f(y)|≤(x−y)²")],
    "3/3 DA years · 1–2 Qs",
    ["Expand near the point", "Check joints piecewise"],
    ["Fold into the optimisation quiz"]),
T(2, "Taylor Series", [
    ("Standard expansions (eˣ, sin, cos, sinh, ln)", "DA 2025: 10th derivative of sinh"),
    ("nth-derivative-at-a-point tricks", "Read coefficients off the series"),
    ("Derivatives of ML functions", "DA 2024: sigmoid derivative at a point")],
    "1–2/3 DA years · 1 Q",
    ["Know 6 expansions cold", "Match coefficient ↔ derivative"],
    ["Flashcard the expansions"]),
T(2, "Maxima, Minima and Optimisation of Single-Variable Functions", [
    ("Critical points and second-derivative test", "DA all three years (quartic/cubic/cubic)"),
    ("Convexity and global minima", "DA 2025: at-most-one-global-min statement"),
    ("ReLU/non-smooth differentiability", "DA 2025: ReLU differentiability question")],
    "3/3 DA years · 1–2 Qs",
    ["Classify stationary points", "Argue convexity when asked"],
    ["Topic quiz after PYQ pass"]),
]})

# 13 ----------------------------------------------------------------- ML
G.append({"name": "13. Machine Learning", "note": "Data Science paper (~11–14 marks, steady top-3 section)",
"rows": [
T(1, "Simple and Multiple Linear Regression, Ridge Regression", [
    ("Least squares closed form", "DA 2025: y=wx fitting"),
    ("Multiple regression interpretation", "Coefficient meaning questions"),
    ("Ridge regression: λ effect and solution", "DA 2026 asked Ridge twice (incl. MAE objective)"),
    ("Residuals and assumptions", "Light conceptual")],
    "3/3 DA years · 2 Qs",
    ["Derive/apply closed forms", "Reason about λ and shrinkage"],
    ["Regression drill: 15 numericals"]),
T(1, "Logistic Regression", [
    ("Sigmoid and log-odds", "Threshold/boundary questions"),
    ("Decision boundary geometry", "Linearity of the boundary"),
    ("Loss and gradient (idea)", "Conceptual")],
    "2/3 DA years · 1 Q",
    ["Compute probabilities at thresholds"],
    ["Fold into classification drill"]),
T(1, "k-Nearest Neighbours, Naive Bayes, Linear Discriminant Analysis", [
    ("kNN classification and distances", "DA 2024 kNN question"),
    ("Naive Bayes parameter counts", "DA 2024: parameter count for K binary attributes"),
    ("Naive Bayes misclassification", "DA 2025: which-class prediction"),
    ("LDA and nearest-mean classifiers", "DA 2025: linearity of nearest-mean classifier")],
    "3/3 DA years · 1–2 Qs",
    ["Count NB parameters", "Apply kNN by hand"],
    ["Include in ML sectional"]),
T(1, "Support Vector Machine", [
    ("Hard margin, support vectors", "DA 2025: margin √2, identify SVs"),
    ("Margin = 2/‖w‖", "The core formula"),
    ("Kernels (idea only)", "Not heavily asked — know the concept")],
    "1–2/3 DA years · 1 Q",
    ["Find SVs and compute margins"],
    ["Make the SVM formula card"]),
T(1, "Decision Trees", [
    ("Entropy and information gain", "Split-selection numericals"),
    ("Gini impurity", "Alternative impurity"),
    ("Depth and overfitting", "Conceptual")],
    "2/3 DA years · 1 Q",
    ["Compute gain for one split by hand"],
    ["Include in ML sectional"]),
T(1, "Bias-Variance Trade-off and Cross-Validation", [
    ("Bias-variance decomposition", "Conceptual staple"),
    ("LOO and k-fold CV", "Syllabus-explicit; estimate-computation questions"),
    ("Regularisation link", "Connects to Ridge")],
    "2/3 DA years · 1 Q",
    ["Estimate LOO/k-fold errors", "Classify high-bias vs high-variance"],
    ["Conceptual flashcards"]),
T(2, "Multi-Layer Perceptron and Feed-Forward Neural Networks", [
    ("Perceptron update rule", "DA 2025: update-direction question"),
    ("ReLU networks and gradients", "DA 2025: ∂y/∂a backprop; ReLU differentiability"),
    ("MLP parameter counting", "DA 2026: parameter-count question; DA 2024 two-network comparison"),
    ("Activation functions", "Sigmoid/ReLU properties")],
    "3/3 DA years · 1–2 Qs",
    ["Count parameters exactly", "One backprop step by hand"],
    ["NN drill: 15 problems"]),
T(2, "Clustering — k-Means, k-Medoids, Hierarchical", [
    ("k-means iterations and assignments", "DA 2024: k=3 same-cluster question"),
    ("k-medoids difference", "Conceptual 1-mark"),
    ("Hierarchical: single/complete linkage", "DA 2024/2025 linkage traces; DA 2026 agglomerative with Manhattan"),
    ("Initialisation dependence", "k-means trap question")],
    "3/3 DA years · 1–2 Qs",
    ["Trace one k-means iteration", "Merge clusters by linkage rule"],
    ["Clustering drill: 12 traces"]),
T(2, "Principal Component Analysis", [
    ("Covariance eigen-decomposition", "DA 2025: eigenvalues λᵢ=100^(2−i)"),
    ("Explained variance and projections", "Projection computation"),
    ("PCA for classification", "DA 2026: PCA-for-classification question"),
    ("Scatter matrices", "DA 2024: between/within-class scatter"),
    ("Eigenvector sign/scaling traps", "Recurring conceptual trap")],
    "3/3 DA years · 1–2 Qs — ask every year",
    ["Eigenvectors of 2×2 covariance by hand", "Explain what PCA maximises"],
    ["PCA drill — never skip, it appears every year"]),
]})

# 14 ----------------------------------------------------------------- AI
G.append({"name": "14. Artificial Intelligence", "note": "Data Science paper (~6–11 marks, smallest section — efficient study wins here)",
"rows": [
T(3, "Uninformed Search (BFS, DFS)", [
    ("BFS/DFS/UCS properties", "Completeness/optimality MCQs"),
    ("State-space counting", "DA 2024: successor counting"),
    ("DFS discovery/finish counts", "DA 2025: discovery-count question")],
    "2–3/3 DA years · 1 Q",
    ["Count nodes expanded", "Compare algorithm properties"],
    ["Include in AI quiz"]),
T(3, "Informed Search — A* and Heuristics", [
    ("Admissibility and consistency", "DA 2024: admissibility of h1+h2, max, min"),
    ("A* expansion order", "DA 2025: expansion-sequence question"),
    ("Heuristic dominance", "Conceptual 1-mark")],
    "3/3 DA years · 1 Q",
    ["Check admissibility against h*", "Trace expansions with f=g+h"],
    ["A* drill: 10 traces — always asked"]),
T(3, "Adversarial Search — Minimax", [
    ("Minimax tree values", "DA 2026: game-tree value question"),
    ("Alpha-beta pruning", "DA 2024/2025: pruning ranges; ordering matters trap"),
    ("Move-ordering effects", "Why prune counts differ")],
    "3/3 DA years · 1 Q",
    ["Evaluate game trees", "Mark pruned branches correctly"],
    ["Include in AI quiz"]),
T(3, "Propositional Logic and Predicate Logic (AI section)", [
    ("Entailment and validity", "DA 2026: two FOL validity questions"),
    ("Equivalences and tautologies", "DA 2025: equivalence question"),
    ("FOL predicates and quantifiers", "DA 2024: game/shape predicates"),
    ("Shared with CSE discrete maths", "Study once, credit twice")],
    "3/3 DA years · 1–2 Qs",
    ["Same skill as CS logic topic"],
    ["Shared with group 1 drill — no separate study"]),
T(3, "Reasoning under Uncertainty — Conditional Independence, Variable Elimination, Sampling", [
    ("Conditional independence factorisation", "DA 2024: P(U,V,W,X,Y) factorisation"),
    ("Bayes-net CPT computations", "DA 2024: CPT inference question"),
    ("Variable elimination", "DA 2025: exact-inference question"),
    ("Sampling: rejection and Gibbs", "DA 2025: approximate-inference comparison")],
    "2/3 DA years · 1 Q",
    ["Read factorisations off the graph", "One VE elimination by hand"],
    ["Make a Bayes-net worked-example card"]),
]})

# 15 ----------------------------------------------------------------- GA
G.append({"name": "15. General Aptitude", "note": "Common to both papers — fixed 15 marks, identical syllabus, study once",
"rows": [
T(1, "Verbal Ability — Grammar, Vocabulary, Reading Comprehension", [
    ("Grammar: tenses, articles, prepositions, agreement", "Error-spotting questions"),
    ("Vocabulary and idioms in context", "Word-meaning questions"),
    ("Reading comprehension and sequencing", "Short-passage questions every year")],
    "Every year · 4–6 marks",
    ["Error spotting", "Cloze/vocab in context"],
    ["30-min GA block alternate days — no separate theory phase"]),
T(1, "Numerical Ability — Quantitative Aptitude and Data Interpretation", [
    ("Ratios, percentages, powers, logarithms", "Bulk of quant marks"),
    ("Permutations/combinations and series", "Feeds from maths prep"),
    ("Data interpretation: graphs, tables, maps", "Every year 2–3 questions"),
    ("Mensuration and geometry basics", "Occasional")],
    "Every year · 5–7 marks",
    ["Speed arithmetic", "DI extraction accuracy"],
    ["Daily 15-question GA set"]),
T(1, "Logical Reasoning and Analytical Ability", [
    ("Deduction/induction puzzles", "Constraint-satisfaction style puzzles"),
    ("Analogies and numerical relations", "Quick marks"),
    ("Spatial: folding, rotation, patterns", "Paper-folding questions — practice-based only")],
    "Every year · 4–5 marks",
    ["Constraint grids", "Visual rotation"],
    ["Alternate-day GA block"]),
]})

data = {"groups": G,
        "meta": {"disclaimer": "PYQ frequencies are approximate (coaching-analysed, ±1 year). DA notes cite the three existing papers (2024–2026). Solve the actual topic-wise PYQ bank for the real questions.",
                 "solveCSE": "CSE: topic-wise PYQs 2017–2026 (oldest → newest when learning)",
                 "solveDA": "DA: all questions from the 2024, 2025, 2026 papers"}}

out = __import__("pathlib").Path(__file__).resolve().parent / "checklist_data.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
print("wrote", out.name + ":", sum(len(g["rows"]) for g in G), "topics,",
      sum(len(r["subs"]) for g in G for r in g["rows"]), "subtopics")
