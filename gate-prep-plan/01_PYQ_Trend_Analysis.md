# GATE CSE + DA — 10-Year PYQ Trend Analysis (Sections A, B, C)

**Prepared:** 6 October 2026 · **Target exam:** GATE 2027 (IIT Madras; exams 6–7, 13–14, 20–21 Feb 2027)

---

## Data provenance & limitations (read first)

| Data type | Source quality | Caveat |
|---|---|---|
| Exam pattern, syllabi, qualifying cutoffs, candidate counts | **Official** (IIT GATE sites + statistical reports) | Reliable |
| Subject-wise marks per year | Coaching memory-based analyses (ACE, GO Classes, GfG, PW), cross-checked | ±1–4 marks; sources conflict in places — ranges given |
| DA section-wise marks | Question-by-question classification of the official 2024/25/26 papers, cross-checked | ±2 marks per section |
| Marks vs rank | Community/synthesized (no official table exists) | Indicative bands only |
| **GATE DA history** | **Only 3 papers exist: 2024, 2025, 2026** | Any "DA trend" rests on n=3 — stated wherever it matters |
| GATE CSE 2017 | Single source (ACE) | Lowest confidence |
| CSE 2021 | Two sessions + normalization | Per-subject marks less comparable |

Where official data does not exist, numbers below are marked **(approx.)**. Nothing here is invented beyond the flagged approximations.

---

# A. 10-Year PYQ Trend Analysis

## A.1 Paper structure facts (official, both papers)

- 65 questions / 100 marks / 3 hours, CBT, virtual calculator.
- **CS:** GA 15 + Engineering Mathematics 13 + subject 72 (official GATE 2027 split). GA is always 5×1 + 5×2.
- **DA:** GA 15 + subject 85 — no separate Engineering-Mathematics block; the math lives inside P&S / LA / Calculus sections.
- Question types: **MCQ** (negative: −1/3 on 1-mark, −2/3 on 2-mark), **MSQ** (no negative, no partial), **NAT** (no negative, typed answer).
- CS section list (GATE 2027 official): 1 Engineering Mathematics (incl. Discrete Mathematics), 2 Digital Logic, 3 COA, 4 Programming & Data Structures, 5 Algorithms, 6 TOC, 7 Compiler Design, 8 OS, 9 Databases, 10 Computer Networks.
- DA section list (GATE 2027 official, unchanged from 2026): 1 Probability & Statistics, 2 Linear Algebra, 3 Calculus & Optimization, 4 Programming/DS/Algorithms, 5 Database Management & Warehousing, 6 Machine Learning, 7 AI.

## A.2 CSE subject-wise marks, 2017–2026 (approx., from paper analyses)

| Subject | Typical marks | Recent avg (2022–26) | Stability | PYQ verdict |
|---|---|---|---|---|
| General Aptitude | 15 (fixed) | 15.0 | Fixed | Free-ish 15 marks; practice only |
| Engg Math + Discrete Math | 10–19 | ~12–13 | Volatile | Biggest math block; swings by year |
| Programming & Data Structures | 6–12 | ~9–10 | High | Guaranteed every year |
| COA | 4–13 | ~9 | Medium | "Rank-decider" per analysts; 2023 peak ~12 |
| Operating Systems | 6–10 | ~8 | High | Consistent top-4 |
| Algorithms | 6–11 | ~7–8 | High | P&DS + Algo ≈ 16–18 marks combined every year |
| TOC | 5–10 | ~8 | High | Most stable core subject |
| Computer Networks | 6–11 | ~8 | Medium | 2022 peak ~11 |
| DBMS | 5–8 | ~7 | High | Stable |
| Digital Logic | 3–6 | ~5 | High | Small but high-ROI |
| Compiler Design | 4–8 | ~5–6 | Most volatile | Moves with TOC |

**Combined block facts (approx.):** Math + P&DS + Algo + OS ≈ 45–50 marks every year; these four decide most ranks.

## A.3 CSE topic-level patterns (2017–2026, PYQ evidence)

**Programming & Data Structures**

- C output-prediction questions (pointers, arrays, recursion, parameter passing, scope, dynamic memory) appear **every single year, 3–5 questions** — the single most predictable pattern in the paper.
- Trees (BST operations, traversals, heap insert/delete) nearly every year; stacks/queues applications and linked-list manipulation alternate; hashing (chaining/probing counts) every other year; multi-dimensional array addressing appears regularly.
- Mostly **problem-solving/tracing**, not recall. Difficulty: medium–hard. **Traps:** post-increment evaluation order, `sizeof` array-vs-pointer, pass-by-value of pointers, recursion call-tree miscounts, integer overflow in recursion.

**Algorithms**

- Asymptotic comparison and recurrences (Master theorem style) nearly every year.
- Graph algorithms every year: Dijkstra (2026 asked a *modified* Dijkstra — hardest question of the paper), MST, BFS/DFS applications, topological sort.
- Sorting properties (stability, comparisons/swaps counts), greedy correctness, DP conceptual/counting questions steady.
- **Note:** NP-completeness appeared in ≤2023 papers but was **dropped from the 2024-restructured syllabus** — read once for background, don't invest.
- **Traps:** comparing non-polynomial functions, miscounting recursion depth, assuming stability where none exists.

**COA**

- **Pipelining numericals (hazards, stalls, forwarding, speedup) ~9 of 10 years.**
- **Cache mapping + AMAT + multi-level caches ~9 of 10 years**; often combined with OS virtual memory/TLB (2026 explicitly did multi-level cache + multi-level paging).
- IEEE-754 floating point, addressing modes, DMA/interrupts recur; microprogramming and ALU design occasional.
- Numerical-heavy. **Traps:** forgetting split of instruction vs data cache misses, ignoring forwarding in cycle counts, byte-vs-word addressing.

**OS**

- CPU scheduling numericals, semaphores/critical-section analysis (2026: race-condition analysis), Banker's algorithm/RAG, page replacement + TLB/EMAT — all perennial.
- File systems (Unix inode questions) **rising** over the last 5 years; processes/threads/system calls/fork steady.
- **Traps:** EMAT double-counting TLB and cache misses, average waiting time vs turnaround, counting context switches, Banker's "safe ≠ all sequences".

**DBMS**

- SQL (joins, nested/correlated subqueries, aggregation) every year — 2026 had correlated COUNT and a TRC question.
- Normalization (FD closure, candidate keys, BCNF/3NF decomposition, lossless/dependency-preserving) every year.
- Serializability/recoverability/2PL every year; B+ tree indexing most years; relational algebra regularly; ER occasional.
- **Traps:** FD-closure arithmetic slips, BCNF vs 3NF decomposition order, "conflict-serializable but not view-serializable" edge cases, B+ tree order convention (order = max pointers vs max keys).

**TOC**

- RE↔DFA/NFA, closure properties, pumping lemma — perennial. CFG/PDA (design, ambiguity, conversion) perennial.
- **Decidability/Rice's theorem questions rising** (2026 included Rice's theorem) — the modern differentiator.
- **Traps:** assuming CFL closures that don't exist (complement/intersection), pumping-lemma logic direction, DPDA vs NPDA.

**Compiler Design**

- **Parsing dominates:** LL(1) conditions, LR(0)/SLR/LR(1)/LALR table construction and conflict questions nearly every year.
- SDT (evaluation order, inherited/synthesized attributes), 3-address code/intermediate code, lexical analysis + regex→NFA alternate years.
- **2027 syllabus now explicitly includes data-flow analyses** (constant propagation, liveness, CSE) — expect this to grow.
- **Traps:** FIRST/FOLLOW arithmetic errors, confusing SLR vs LALR conflict counts, SDT with inherited attributes on left recursion.

**Computer Networks**

- TCP (flow control, congestion control tracing, sliding window numericals) and IPv4 (CIDR subnetting, fragmentation) — the two perennial numerical clusters.
- DV vs LS routing, CRC/error detection recurring; DNS/HTTP/socket API steady.
- **2027 syllabus was trimmed** (UDP detail, SMTP/FTP/email, ARP/DHCP/ICMP, Ethernet bridging dropped) — follow the new syllabus, ignore removed topics.
- **Traps:** counting SYN/FIN in sequence numbers, subnet-zero assumptions, RTT/timeout arithmetic, classful habits in CIDR.

**Digital Logic**

- K-map/Boolean minimization and number representation (2's complement, IEEE-754) nearly every year; counters/flip-flop state tracing and MUX-based combinational design alternate.
- Small (3–6 marks) but **highest marks-per-hour in the paper**.
- **Traps:** don't-care misuse in K-maps, floating-point bias/normalization slips, up-down counter state misreads.

**Engg Math + Discrete Math (13-mark official block)**

- Probability (conditional, Bayes, RVs, distributions, expectation) is the single largest recurring math theme — and it **overlaps DA's P&S**.
- Linear algebra (rank, eigen, systems), combinatorics (counting, recurrences, generating functions), graph theory, propositional/FOL logic, relations/partial orders/groups all recur.
- Calculus (maxima/minima, limits) lighter for CS than for DA. 2026 math was unusually tough — expect reasoning-flavored math, not formula recall.
- **Traps:** generating-function coefficient extraction, group axioms vs monoids, eigenvalue shortcuts for triangular/low-rank matrices.

## A.4 CSE question-type trend (counts from actual papers)

| Year | MCQ | MSQ | NAT | Takeaway |
|---|---|---|---|---|
| 2022 | 32 | 15 | 18 | MSQs established |
| 2023 | 34 | 15 | 16 | Stable |
| 2024 | 19 | 20 | 16 | MSQ spike — deep-concept shift |
| 2025 | 33 | 18 | 14 | Rebalanced |
| 2026 | 34 | 11 | 19 | NAT ≈ 30% of paper |

Non-MCQ (NAT+MSQ) ≈ 35–50% of questions since 2023 → **elimination-guessing is dead; concept depth and exact answers are the game.**

## A.5 CSE cutoffs (official) & marks-vs-rank (approx.)

| Year | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|
| Gen cutoff | 28.5 | 26.1 | 25.0 | 32.5 | 27.6 | 29.2 | **30.0** |

Marks vs rank (approx., community data): 85+ ≈ top 10; 75–82 ≈ AIR <100; **~70–75 ≈ AIR <500 (2025–26 era)**; ~65 ≈ AIR <1000. Same marks are buying worse ranks each year (80 marks ≈ AIR 25 in 2024 vs AIR 215 in 2025) — competition is intensifying.

## A.6 DA paper analysis (2024, 2025, 2026 — the complete history)

### Section-wise marks (approx., classified from the official papers)

| Section | 2024 | 2025 | 2026 | Signal |
|---|---|---|---|---|
| Probability & Statistics | ~16 | ~19 | ~19 | **The anchor — biggest or joint-biggest every year** |
| Programming/DS/Algorithms | ~21 | ~15 | ~14 | Eased from 2024 peak but still top-3 |
| Machine Learning | ~11–13 | ~14 | ~13 | Steady top-3 |
| Linear Algebra | ~10 | ~11 | ~8 | Steady |
| DBMS & Warehousing | ~8–9 | ~11 | **~18** | **Sharply expanding (2026: B+ trees, TRC, OLAP cuboids)** |
| Calculus & Optimization | ~8 | ~9 | ~5 | Shrinking |
| AI | ~9–11 | ~6 | ~8 | Smallest, fluctuating |
| General Aptitude | 15 | 15 | 15 | Fixed |

### Topic highlights (what was actually asked)

- **2024 (IISc, easy–moderate, NAT-heavy):** Poisson mean=variance; conditional-independence factorization; expected die throws until two consecutive evens; projection matrices; singular values of rank-1 matrix; sigmoid derivative at a point; DFS properties; uniform hashing; deque ops; DAG topological orderings; Python recursion outputs; k-means k=3; single-linkage; k-NN; Naive Bayes parameter count; PCA matching; two-ReLU-network comparison; A* admissibility (h1+h2, max, min); alpha-beta pruning; SQL joins; FDs/candidate keys; min-max normalization.
- **2025 (IIT Roorkee, moderate, most MSQs):** tower rule E[E[X|Y]]; Bayes 3 boxes; CLT for Bernoulli sum; geometric-from-exponential-floor; unbiased Bernoulli estimator; row-stochastic Bx=0; orthonormal bases; singular values of a projection; 10th derivative of sinh; convexity single-global-min; linear probing trace; binary search array-vs-linked-list; insertion-sort swap count; perceptron update direction; hard-margin SVM (support vectors, margin √2); ReLU backprop gradient; PCA via eigenvalues λᵢ=100^(2−i); OLAP GROUP BY CUBE count; dependency-preserving decomposition; relational-algebra division; variable elimination vs Gibbs/rejection sampling; A* expansion sequence.
- **2026 (IIT Guwahati, moderate-tough, math-heavy):** stars-and-bars; bijections f(f(n))=n; exponential memorylessness P(X>10|X>5); Poisson limit; Bayes disease testing; variance identity ΣΣ(xᵢ−xⱼ)²; rotation matrix M^2026; Rayleigh quotient max xᵀAx; B+ tree construction ×2; TRC count query; correlated SQL COUNT; data cuboids from concept hierarchies; ER→3NF with multivalued attribute; quicksort first-element pivot; Python mutable default argument; binary tree from pre+in; PCA for classification; Ridge regression ×2; MLP parameter count; minimax game-tree values; FOL validity ×2.

### Official statistics

| Metric | 2024 | 2025 | 2026 |
|---|---|---|---|
| Gen cutoff | 37.1 | 29 | **26.4** |
| Appeared | 39,210 | 57,054 | 69,242 |
| Mean marks | 23.4 | 17.7 | 15.5 |
| AIR-1 marks | 90 | 96.33 | 90 |
| Marks ≈ AIR<100 | ~70+ | ~68–70 | ~70+ |
| Marks ≈ AIR<500 | ~60 | ~60 | ~58–60 |

**Reading:** paper getting harder + candidates +77% in two years → cutoffs falling, but **top-500 bar (~58–60) is far more stable than the cutoff suggests**. AIR<500 in DA is a ~60-mark game; AIR<100 needs ~70.

### DA question-type trend
NAT share rising (heaviest in 2026); MSQs strong in 2025. Same discipline as CSE: exact answers, no guessing crutches.

## A.7 Cross-paper meta-trends (why the plan looks the way it does)

1. **Non-MCQ dominance** (35–50%) → both papers reward deep, exact understanding over elimination tricks. PYQ practice must be NAT/MSQ-heavy.
2. **Math is the common backbone**: CSE's biggest single block (EM+DM ~13) and DA's biggest two sections (P&S + LA ≈ 27–30) are siblings. Highest marks-per-hour investment in the entire prep.
3. **DBMS is rising in DA** (8→18) while stable-high in CSE — study it once, at CSE depth, add warehousing on top.
4. **PDSA eased in DA (21→14) but Programming output-tracing is a universal pattern** — C and Python tracing drills serve both.
5. **Cross-subject questions** (COA×OS virtual memory, probability×combinatorics) are increasing → study subjects in connected blocks, not silos.
6. **Calculus and AI are small/shrinking in DA** → cap your time there; **TOC-decidability and file systems rising in CSE** → don't skip them.
7. **Cutoffs**: qualifying cutoffs are ~26–30 for both papers, but that's the ~top-15% line; AIR 1–500 needs ~70 (CS) / ~60 (DA).

---

# B. Subject-wise Weightage & Priority (with marks-per-hour ROI)

ROI = expected marks ÷ study hours, combining weightage, stability, and difficulty.

## B.1 GATE CSE priority order

| Rank | Subject | Marks (avg) | Hours (theory+PYQ) | ROI | Verdict |
|---|---|---|---|---|---|
| 1 | Engg Math + Discrete Math | 12–13 | 75 | ★★★★★ | Highest single block; shared with DA |
| 2 | Programming & Data Structures | 9–10 | 50 | ★★★★★ | Guaranteed marks; shared concepts with DA Python |
| 3 | Operating Systems | 8–9 | 45 | ★★★★☆ | Consistent, finite, numerical-heavy |
| 4 | Algorithms | 7–8 | 40 | ★★★★☆ | Shared with DA |
| 5 | COA | ~9 | 45 | ★★★★☆ | Rank-decider; pipelining+cache are formulaic once mastered |
| 6 | TOC | ~8 | 35 | ★★★★☆ | Most stable subject in the paper |
| 7 | DBMS | 7–8 | 40 | ★★★★☆ | Shared with DA (DA's fastest-rising section) |
| 8 | CN | ~8 | 35 | ★★★☆☆ | Two numerical clusters carry most marks |
| 9 | Digital Logic | ~5 | 22 | ★★★★★ (per hour) | Small syllabus, very high ROI |
| 10 | Compiler Design | 5–6 | 30 | ★★★☆☆ | Parsing cluster = most of the marks |
| 11 | General Aptitude | 15 | 20 (spread) | ★★★★☆ | No "theory phase"; weekly practice from day 1 |

## B.2 GATE DA priority order

| Rank | Section | Marks (3-yr avg) | Hours | ROI | Verdict |
|---|---|---|---|---|---|
| 1 | Probability & Statistics | 16–19 | 55 | ★★★★★ | Anchor section; pure math, fully controllable |
| 2 | Linear Algebra | 8–11 | 35 | ★★★★★ | Formulaic once eigen/projection machinery is yours |
| 3 | PDSA (Python + DS + Algo) | 14–21 | 45 (incl. shared) | ★★★★☆ | Python tracing is trainable fast |
| 4 | DBMS & Warehousing | 8–18 | 45 (incl. shared) | ★★★★☆ | Rising fast; CSE-depth study covers 80% |
| 5 | Machine Learning | 11–14 | 40 | ★★★☆☆ | Concept+calc; PCA/clustering/regression every year |
| 6 | Calculus & Optimization | 5–9 | 20 | ★★★☆☆ | Shrinking; single-variable focus |
| 7 | AI | 6–11 | 22 | ★★★☆☆ | Search + logic clusters carry nearly all marks |
| 8 | General Aptitude | 15 | 20 (spread) | ★★★★☆ | Same syllabus as CSE GA — study once |

---

# C. Topic-wise Priority Table (Tiers, with PYQ reasons)

Legend: 🔴 Tier 1 Must-Master · 🟠 Tier 2 High · 🟡 Tier 3 Important · 🟢 Tier 4 Low. "Freq" = share of the relevant years in which the topic appeared.

## C.1 GATE CSE topics

### Engineering Mathematics + Discrete Math (13 marks official block)

| Topic | Tier | Freq | Pattern & reason |
|---|---|---|---|
| Probability: conditional, Bayes, RVs, expectation/variance | 🔴 | 9/10 | Numerical every year; identical to DA P&S core — study once |
| Distributions: binomial/Poisson/normal/exponential/uniform | 🔴 | 8/10 | Distribution-recognition + mean/variance questions |
| Linear algebra: rank, eigen, systems, determinants | 🔴 | 8/10 | Eigen shortcuts (triangular, rank-1, I+uuᵀ) — shared with DA |
| Combinatorics: counting, recurrences, generating functions | 🔴 | 8/10 | Counting + recurrence solving; GF coefficient extraction |
| Graph theory: connectivity, matching, colouring | 🟠 | 6/10 | Handshake/chromatic/matching numericals; shared with DA |
| Propositional + first-order logic | 🟠 | 7/10 | Validity/satisfiability; shared with DA AI logic |
| Sets, relations, functions, partial orders, lattices, groups | 🟠 | 6/10 | Lattice/hasse diagram + group-axiom questions |
| Calculus: maxima/minima, limits, integration | 🟡 | 4/10 | Small for CS (bigger for DA) |
| Statistics: mean/median/mode/std | 🟡 | 3/10 | Quick 1-mark; added emphasis post-2024 |

### Digital Logic (≈5 marks)

| Topic | Tier | Freq | Pattern & reason |
|---|---|---|---|
| Number representation & arithmetic (2's complement, IEEE-754) | 🔴 | 8/10 | Range/overflow/floating-point numericals |
| Boolean minimization (K-map, algebraic) | 🔴 | 9/10 | Direct, fast marks |
| Sequential circuits (flip-flops, counters, state machines) | 🟠 | 6/10 | State-tracing numericals |
| Combinational design (MUX/decoder/adders) | 🟠 | 5/10 | MUX-implementation of functions |
| Tabulation (Quine–McCluskey) method | 🟢 | 1/10 | Rare; know the idea only |

### COA (≈9 marks)

| Topic | Tier | Freq | Pattern & reason |
|---|---|---|---|
| Pipelining: hazards, stalls, forwarding, speedup | 🔴 | 9/10 | The signature COA numerical |
| Cache: mapping, AMAT, multi-level, write policies | 🔴 | 9/10 | Always numerical; often merged with OS |
| Virtual memory, TLB, EMAT (COA×OS) | 🔴 | 7/10 | Cross-subject staple |
| Machine instructions, addressing modes, formats | 🟠 | 6/10 | Instruction-count/encoding questions |
| I/O: interrupts, DMA | 🟠 | 4/10 | Conceptual + cycle-stealing numericals |
| ALU design (ripple/carry-lookahead adders) | 🟡 | 3/10 | Delay calculations |
| Control unit: hardwired vs microprogrammed | 🟡 | 3/10 | Conceptual 1–2 marks |
| Memory interfacing/DRAM details | 🟢 | 1/10 | Rare |

### Programming & Data Structures (≈10 marks)

| Topic | Tier | Freq | Pattern & reason |
|---|---|---|---|
| C tracing: pointers, arrays, functions, recursion, scope, malloc | 🔴 | 10/10 | 3–5 Qs every single year |
| Trees: BST, traversals, heaps | 🔴 | 9/10 | Operation-count and property questions |
| Stacks & queues (applications) | 🔴 | 7/10 | Expression evaluation, implementation mixes |
| Linked lists | 🟠 | 6/10 | Pointer-manipulation outputs |
| Multi-dim arrays (address calculation) | 🟠 | 5/10 | Quick numericals |
| Hashing (chaining, probing) | 🟠 | 5/10 | Probe/cluster counting |
| Graph representations | 🟡 | 3/10 | 1-mark adjacency facts |
| Structs/unions padding | 🟢 | 2/10 | Occasional 1-mark |

### Algorithms (≈8 marks)

| Topic | Tier | Freq | Pattern & reason |
|---|---|---|---|
| Asymptotics + recurrences (Master theorem) | 🔴 | 9/10 | Comparison/solve-the-recurrence |
| Graph algorithms: Dijkstra/MST/BFS-DFS/topological | 🔴 | 9/10 | Traces + properties; 2026 modified-Dijkstra |
| Sorting: properties, comparison/swap counts | 🔴 | 7/10 | Stability + count numericals |
| Greedy (Huffman, activity selection, correctness) | 🟠 | 6/10 | Huffman cost numericals; exchange-argument questions |
| Dynamic programming (conceptual, counting) | 🟠 | 5/10 | 2026: non-standard DP |
| Searching, hashing | 🟡 | 4/10 | Binary-search variant counts |
| Divide & conquer | 🟡 | 4/10 | Usually inside recurrences |
| NP-completeness | 🟢 | ≤2023 only | **Dropped from 2024+ syllabus — background read only** |

### TOC (≈8 marks)

| Topic | Tier | Freq | Pattern & reason |
|---|---|---|---|
| Regular languages: RE↔FA, closures, pumping | 🔴 | 9/10 | Design + property questions |
| CFL: CFG, PDA, ambiguity, closures | 🔴 | 8/10 | Grammar design + closure traps |
| Undecidability, Rice's theorem, TM | 🟠 | 6/10 | **Rising trend**; 2026 Rice's theorem |
| Grammar simplification, CNF/GNF, DPDA | 🟡 | 4/10 | Conversion mechanics |
| TM design/variants | 🟢 | 2/10 | Rare as direct design Qs |

### Compiler Design (≈5–6 marks)

| Topic | Tier | Freq | Pattern & reason |
|---|---|---|---|
| Parsing: LL(1) conditions; LR(0)/SLR/LR(1)/LALR tables & conflicts | 🔴 | 8/10 | Most of CD's marks live here |
| Syntax-directed translation (attributes, evaluation order) | 🔴 | 6/10 | SDT scheme tracing |
| Intermediate code (3-address), local optimization | 🟠 | 5/10 | Translate-snippet questions |
| Lexical analysis, regex→NFA | 🟠 | 4/10 | Overlaps TOC regular languages |
| Data-flow analysis (constant prop, liveness, CSE) | 🟡 | 2/10 | **New explicit syllabus item — expect growth** |
| Runtime environments | 🟡 | 3/10 | Activation records occasionally |
| Compiler phases | 🟢 | 2/10 | 1-mark conceptual |

### OS (≈8–9 marks)

| Topic | Tier | Freq | Pattern & reason |
|---|---|---|---|
| Synchronization: semaphores, critical sections, race analysis | 🔴 | 9/10 | 2026 race-condition analysis |
| CPU scheduling numericals | 🔴 | 8/10 | SJF/RR/priority timelines |
| Paging: replacement, TLB/EMAT, multi-level | 🔴 | 8/10 | Often merged with COA |
| Deadlock: Banker's, RAG, prevention/avoidance | 🔴 | 6/10 | Safe-sequence numericals |
| File systems (Unix, inodes, directory layout) | 🟠 | 5/10 | **Rising** |
| Processes, threads, system calls, fork | 🟠 | 5/10 | fork-output counting |
| Disk scheduling, fragmentation | 🟡 | 3/10 | Standard numericals |
| IPC details | 🟢 | 1/10 | Rare |

### DBMS (≈7–8 marks; DA's fastest-rising section — study once at full depth)

| Topic | Tier | Freq | Pattern & reason |
|---|---|---|---|
| SQL: joins, nested/correlated subqueries, aggregation | 🔴 | 9/10 | Every year, both papers |
| Normalization: FDs, closures, keys, 3NF/BCNF decomposition | 🔴 | 9/10 | Every year, both papers |
| Transactions: serializability, recoverability, 2PL | 🔴 | 8/10 | Schedule analysis every year |
| Relational algebra + tuple calculus | 🟠 | 6/10 | 2026: TRC in DA too |
| Indexing: B/B+ trees | 🟠 | 6/10 | Order/max-keys numericals (2026 DA: 2 Qs) |
| ER modeling | 🟡 | 4/10 | Diagram-to-relations |
| File organization | 🟡 | 3/10 | Occasional |

### CN (≈8 marks)

| Topic | Tier | Freq | Pattern & reason |
|---|---|---|---|
| TCP: flow control, congestion control, sliding window | 🔴 | 8/10 | Window/timeout tracing numericals |
| IPv4: CIDR/subnetting, fragmentation, NAT | 🔴 | 8/10 | Subnetting is the perennial quick-mark numerical |
| Routing: DV (count-to-infinity) vs LS | 🟠 | 6/10 | DV table updates |
| Error detection: CRC, checksum, Hamming | 🟠 | 5/10 | Division numericals |
| MAC: Ethernet/CSMA-CD backoff | 🟡 | 4/10 | Occasional numericals |
| DNS, HTTP, socket API | 🟡 | 4/10 | Conceptual 1–2 marks |
| Layering, switching basics | 🟡 | 3/10 | 1-mark conceptual |
| UDP detail, SMTP/FTP/email, ARP/DHCP/ICMP, bridging | 🟢 | — | **Removed from GATE 2027 syllabus — skip** |

### General Aptitude (15 marks)

| Topic | Tier | Freq | Pattern & reason |
|---|---|---|---|
| Quantitative (ratios, %, P&C, series, DI) | 🔴 | every yr | Bulk of GA marks |
| Analytical (deduction, analogy, relations) | 🔴 | every yr | Trainable fast |
| Verbal (grammar, vocabulary, comprehension) | 🟠 | every yr | Reading habit + rules |
| Spatial (folding, rotation, patterns) | 🟡 | every yr | Practice-based only |

## C.2 GATE DA topics

### Probability & Statistics (16–19 marks — the anchor)

| Topic | Tier | Freq (of 3 yrs) | Pattern & reason |
|---|---|---|---|
| Random variables: PMF/PDF/CDF, expectation, conditional expectation/variance (tower rule) | 🔴 | 3/3 | 2025 tower rule, 2026 CDF properties |
| Named distributions: Bernoulli/binomial/Poisson/exponential (memorylessness)/normal/standard-normal/uniform | 🔴 | 3/3 | Memorylessness 2026; Poisson limit 2026; CLT 2025 |
| Joint/marginal/conditional probability, Bayes theorem | 🔴 | 3/3 | 2025 3-boxes; 2026 disease test |
| Central limit theorem, confidence intervals | 🔴 | 2/3 | CLT 2025; CI syllabus-explicit |
| Hypothesis testing: z-test, t-test, chi-squared test | 🔴 | 2/3 | Explicit syllabus topics; expect growth |
| Correlation & covariance | 🟠 | 3/3 | 2024 correlation of coin RVs; 2026 conditional-uniform correlation |
| Estimators (unbiasedness, MLE-style) | 🟠 | 2/3 | 2025 Bernoulli p̂ question |
| Combinatorics inside probability (stars-and-bars, counting) | 🟠 | 2/3 | 2026 subset-product, stars-and-bars |
| t/χ² distribution properties | 🟡 | 1/3 | Know shapes and usage conditions |

### Linear Algebra (8–11)

| Topic | Tier | Freq | Pattern & reason |
|---|---|---|---|
| Eigenvalues/eigenvectors; special matrices (rotation, idempotent, orthogonal, projection, I+uuᵀ) | 🔴 | 3/3 | 2026 rotation M^2026, Rayleigh quotient |
| Rank/nullity, systems, Gaussian elimination | 🔴 | 3/3 | 2025 row-stochastic Bx=0 |
| Projections, least squares, Gram matrix | 🟠 | 2/3 | 2025 Gram; 2024 projection matrices |
| SVD & singular values | 🟠 | 2/3 | 2024 rank-1; 2025 projection SVs |
| Vector spaces, dependence, bases | 🟠 | 3/3 | 2024 subspaces of R³; 2025 orthonormal bases |
| Quadratic forms | 🟡 | 1/3 | 2026 Rayleigh quotient |
| LU decomposition | 🟡 | 1/3 | Shared with CSE EM |
| Partition matrices | 🟢 | 0/3 | Syllabus word; never directly asked |

### Calculus & Optimization (5–9, shrinking)

| Topic | Tier | Freq | Pattern & reason |
|---|---|---|---|
| Maxima/minima of single-variable functions | 🔴 | 3/3 | 2024 quartic; 2025 cubic; 2026 cubic |
| Limits, continuity, differentiability | 🟠 | 3/3 | 2024 ln-limit; 2025 √(t²+t)−t |
| Taylor series | 🟡 | 1/3 | 2025 sinh¹⁰ derivative |
| Convexity (global min existence) | 🟡 | 2/3 | 2025 statement question |
| Derivatives of ML-flavored functions (sigmoid, ReLU) | 🟡 | 2/3 | 2024 sigmoid at 0.4; 2025 ReLU differentiability |
| Multivariable optimization beyond basics | 🟢 | 0/3 | Syllabus is single-variable — don't over-study |

### Programming, DS & Algorithms (14–21)

| Topic | Tier | Freq | Pattern & reason |
|---|---|---|---|
| Python: recursion, mutable default args, closures, list/set/dict ops | 🔴 | 3/3 | 2026 mutable-default is a classic trap; 2–4 Qs/yr |
| Sorting & searching: properties, comparison/swap counts, binary search | 🔴 | 3/3 | 2025 insertion-sort swaps; 2026 quicksort pivot |
| Trees: traversals, construction from pre+in, BST, full-binary-tree relations | 🔴 | 3/3 | 2026 pre+in construction |
| Hash tables: open addressing, probing traces | 🔴 | 2/3 | 2024 uniform hashing; 2025 linear probing |
| Graph: traversals (DFS/BFS), shortest path basics, topological order | 🟠 | 3/3 | 2024 DAG orderings; 2026 DFS |
| Stacks/queues/linked lists/deques | 🟠 | 2/3 | 2024 deque ops; 2025 stack pseudocode |
| Complexity counting (e.g., Gaussian elimination ops) | 🟡 | 1/3 | 2025 |
| Advanced DP/greedy (CSE-depth) | 🟢 | 0/3 | DA syllabus stops at basics — cap your time |

### DBMS & Warehousing (8→18 — rising fastest)

| Topic | Tier | Freq | Pattern & reason |
|---|---|---|---|
| SQL: joins, nested queries, DDL, NULL semantics | 🔴 | 3/3 | Every year |
| Normalization: FDs, candidate keys, BCNF/3NF, decomposition | 🔴 | 3/3 | 2024 FDs/keys; 2025 dependency-preserving; 2026 ER→3NF |
| B+ trees & indexing | 🔴 | 2/3 | 2026: two B+ tree questions |
| Relational algebra + tuple calculus | 🟠 | 3/3 | 2025 division; 2026 TRC count |
| Data warehouse: OLAP, GROUP BY CUBE, cuboids from concept hierarchies, multidimensional schema | 🟠 | 2/3 | 2025 CUBE; 2026 cuboids — DA-unique, study separately |
| ER model, integrity constraints | 🟡 | 2/3 | 2026 referential integrity |
| Data transformation: min-max normalization, discretization, sampling, compression | 🟡 | 1/3 | 2024 min-max |
| Transactions/concurrency | 🟡 | 1/3 | Lighter than CSE so far — but study core anyway (shared) |

### Machine Learning (11–14)

| Topic | Tier | Freq | Pattern & reason |
|---|---|---|---|
| Regression: linear, multiple, ridge (closed forms, objectives) | 🔴 | 3/3 | 2025 least squares; 2026 Ridge ×2 |
| Classification: logistic, k-NN, naive Bayes, LDA, SVM (hard margin) | 🔴 | 3/3 | 2025 SVM margin √2; naive Bayes misclassification |
| Clustering: k-means/k-medoid, hierarchical (single/complete linkage traces) | 🔴 | 3/3 | 2024 k-means+linkage; 2025 linkage; 2026 agglomerative merge |
| PCA: covariance eigen, projections, dimensionality reduction | 🔴 | 3/3 | **Every year**; 2026 PCA-for-classification |
| Decision trees (entropy/gain splits) | 🔴 | 2/3 | Standard computation |
| Bias-variance, cross-validation (LOO, k-fold) | 🟠 | 2/3 | Conceptual 1–2 marks |
| Neural networks: perceptron updates, MLP parameter counts, ReLU nets, backprop gradients | 🟠 | 3/3 | 2024 two-ReLU nets; 2025 backprop; 2026 MLP params |
| Evaluation metrics (accuracy/precision/recall/F1/ROC) | 🟠 | 1/3 | Syllabus-implied; quick marks |
| Ensembles / deep learning beyond MLP | 🟢 | 0/3 | **Not in syllabus — skip** |

### AI (6–11)

| Topic | Tier | Freq | Pattern & reason |
|---|---|---|---|
| Search: A* (admissibility, expansion order), uninformed vs informed | 🔴 | 3/3 | 2024 heuristics; 2025 expansion sequence |
| Adversarial search: minimax, alpha-beta | 🔴 | 3/3 | 2026 game-tree values |
| Propositional + predicate logic: validity, entailment, equivalence | 🔴 | 3/3 | 2026 two FOL-validity Qs |
| Reasoning under uncertainty: Bayes nets, conditional independence, variable elimination, sampling (Gibbs/rejection) | 🟠 | 2/3 | 2024 CPT; 2025 VE-vs-sampling |
| CSP, planning, KR&R beyond logic | 🟢 | 0/3 | **Not in GATE 2027 DA syllabus — skip** |

### General Aptitude — identical to CSE. Study once (Section D).
