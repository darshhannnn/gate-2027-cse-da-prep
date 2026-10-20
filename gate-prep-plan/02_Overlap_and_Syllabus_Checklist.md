# CSE–DA Overlap Analysis + Complete Syllabus Checklist (Sections D, E)

# D. CSE–DA Overlap Analysis

The two syllabi share roughly **half their content**. Studied in the right order, the combined preparation costs ~65–70% of two separate preps.

## D.1 Study ONCE — serves both papers (~45–50 marks on each paper)

| Shared block | Where it counts | Depth to study at |
|---|---|---|
| **Probability & random variables** (Bayes, conditional, expectation, distributions) | CSE EM (~4–6 m) + DA P&S (~10 m of its 16–19) | **DA depth** (it subsumes CSE depth) |
| **Linear algebra** (rank, eigen, systems, projections) | CSE EM (~3–4 m) + DA LA (~8–11 m) | **DA depth** (+ SVD, projections) |
| **Combinatorics, graph theory, logic, sets/relations/groups** | CSE DM + DA P&S counting + DA AI logic | CSE DM depth |
| **Data structures & algorithms** (sorting, searching, trees, hashing, graphs, complexity) | CSE P&DS+Algo (~17 m) + DA PDSA (~14–21 m) | CSE depth + DA's Python tracing drills |
| **DBMS core** (SQL, normalization, transactions, indexing, ER, relational algebra) | CSE DBMS (~7–8 m) + DA DBMS (~8–18 m) | **CSE depth** (it covers DA's 2026-heavy topics), + DA's warehousing extra |
| **Calculus core** (limits, differentiability, maxima/minima) | CSE EM calc (~2–3 m) + DA Calc (~5–9 m) | DA depth (single-variable focus) |
| **General Aptitude** | 15 m on both, identical syllabus | One practice track |

## D.2 CSE-ONLY (~40–45 marks on the CS paper)

Digital Logic (~5), COA (~9), OS (~9), TOC (~8), Compiler Design (~5–6), CN (~8) — none of these appear in DA. This block is what makes the CS paper a separate discipline.

## D.3 DA-ONLY (~28–32 marks on the DA paper)

- Machine Learning full section (~11–14)
- AI section beyond shared logic (~6–11; search + Bayes-net inference are DA-unique; propositional/FOL logic itself is shared with CSE DM)
- Statistics beyond CSE level: CLT, confidence intervals, z/t/χ² tests, estimators (~4–6 m)
- Data warehousing/OLAP (~3–5 m)
- Optimization flavor: convexity, Taylor series (~1–2 m)
- Python-specific programming practice (C covers concepts; Python syntax and tracing drills are required for DA)

## D.4 Optimal study order (no double-study)

1. **Math spine** (P&S + LA + Calc + DM) — at DA depth. Covers both.
2. **Programming + DS + Algorithms** — concepts via C (CSE needs C tracing), then a 1-week Python conversion block for DA tracing drills.
3. **DBMS core** — at CSE depth, then a 1-day warehousing extension for DA.
4. **Branch out**: CSE-only six (DL, COA, OS, TOC, CD, CN) ↔ DA-only four (ML, AI, stats-tests, warehousing), interleaved (see Phase 2 schedule).
5. **GA** — one weekly practice track.

---

# E. Complete Syllabus Checklist (official GATE 2027 syllabi, tier-tagged)

Tick every box. Tier: 🔴 T1 · 🟠 T2 · 🟡 T3 · 🟢 T4. ✍️ = "do PYQs immediately after this topic."

## E.1 GATE CS

### 1. Engineering Mathematics (GA 15 + EM 13 official split)
**Discrete Mathematics**

- [ ] 🔠 🟠 Propositional logic: syntax, truth tables, validity, satisfiability, logical equivalences ✍️
- [ ] 🟠 First-order logic: predicates, quantifiers, negation rules, inference ✍️
- [ ] 🔴 Sets, relations, functions: closure, equivalence relations, partial orders, lattices (Hasse diagrams) ✍️
- [ ] 🟠 Monoids, groups: axioms, subgroups, cyclic groups ✍️
- [ ] 🔴 Graphs: connectivity, Euler/Hamiltonian, matching (bipartite, Hall's), colouring (chromatic number) ✍️
- [ ] 🔴 Combinatorics: counting arguments, permutations/combinations, pigeonhole, recurrence relations, generating functions ✍️

**Linear Algebra**

- [ ] 🔴 Matrices, determinants, rank; systems of linear equations (consistency) ✍️
- [ ] 🔴 Eigenvalues, eigenvectors, diagonalization; properties for special matrices ✍️
- [ ] 🟡 LU decomposition ✍️

**Calculus**

- [ ] 🟡 Limits, continuity, differentiability; mean value theorem
- [ ] 🟡 Maxima and minima
- [ ] 🟡 Integration (definite integrals, properties)

**Probability & Statistics**

- [ ] 🔴 Random variables; expectation, variance, conditional probability ✍️
- [ ] 🔴 Uniform, normal, exponential, Poisson, binomial distributions ✍️
- [ ] 🟡 Mean, median, mode, standard deviation
- [ ] 🔴 Bayes theorem ✍️

### 2. Digital Logic

- [ ] 🔴 Boolean algebra; minimization: algebraic, K-map, tabular method ✍️
- [ ] 🟠 Combinational circuits: adders, MUX, decoders, implementations ✍️
- [ ] 🟠 Sequential circuits: flip-flops, counters, state diagrams/machines ✍️
- [ ] 🔴 Number representation: fixed point, 2's complement; floating point (IEEE-754) ✍️
- [ ] 🟠 Computer arithmetic basics (overflow, ranges)

### 3. COA

- [ ] 🟠 Instruction sets, instruction formats, addressing modes ✍️
- [ ] 🟡 ALU design: ripple-carry, carry-lookahead adders; delay calculation
- [ ] 🟡 Control unit: hardwired; microprogrammed (microinstructions, sequencing) ✍️
- [ ] 🟠 Memory hierarchy: performance, interface; DRAM basics
- [ ] 🔴 Cache memory: mapping (direct/associative), replacement, write policies, multi-level, AMAT ✍️
- [ ] 🟠 I/O interface: interrupts, DMA ✍️
- [ ] 🔴 Instruction pipelining: stages, hazards (structural/data/control), stalls, forwarding, speedup ✍️

### 4. Programming & Data Structures

- [ ] 🔴 C programming: data types, operators, control flow, functions, parameter passing, scope, pointers, arrays, dynamic memory ✍️ (tracing drills)
- [ ] 🔴 Recursion: call trees, base cases, counting ✍️
- [ ] 🟠 Arrays (incl. multi-dimensional addressing) ✍️
- [ ] 🔴 Stacks, queues (array + linked implementations, applications) ✍️
- [ ] 🟠 Linked lists: singly/doubly, manipulations ✍️
- [ ] 🔴 Trees, binary trees, BST: traversals, properties, operations ✍️
- [ ] 🔴 Binary heaps: insert/delete/heapify ✍️
- [ ] 🟡 Graphs: representations, basic traversals

### 5. Algorithms

- [ ] 🔴 Searching (linear/binary variants), sorting (all standard sorts: properties, counts) ✍️
- [ ] 🔴 Hashing: chaining, open addressing, load factor ✍️
- [ ] 🔴 Asymptotic worst-case time/space complexity; comparison of functions ✍️
- [ ] 🔴 Recurrence relations, Master theorem ✍️
- [ ] 🟠 Greedy: framework, Huffman, activity selection, exchange arguments ✍️
- [ ] 🟠 Dynamic programming: principles, standard problems, counting subproblems ✍️
- [ ] 🟡 Divide and conquer ✍️
- [ ] 🔴 Graph traversals (BFS/DFS and applications), topological sort ✍️
- [ ] 🔴 MST: Prim, Kruskal ✍️
- [ ] 🔴 Shortest paths: Dijkstra (incl. properties/limitations), Bellman-Ford idea ✍️
- [ ] 🟢 NP-completeness — background reading only (dropped from 2024+ syllabus)

### 6. TOC

- [ ] 🔴 Regular expressions, FA (DFA/NFA/ε-NFA), conversion, minimization ✍️
- [ ] 🔴 Regular languages: closure properties, pumping lemma ✍️
- [ ] 🔴 CFGs: derivations, ambiguity, simplification, CNF ✍️
- [ ] 🔴 PDAs: design, acceptance ✍️
- [ ] 🟠 CFL closure properties, pumping lemma for CFLs ✍️
- [ ] 🟠 Turing machines: model, language recognition
- [ ] 🔴 Decidable/recognizable languages, undecidability, Rice's theorem, reductions ✍️ (rising trend)

### 7. Compiler Design

- [ ] 🟠 Lexical analysis: tokens, regex→NFA (overlap with TOC) ✍️
- [ ] 🟡 Parsing overview: top-down vs bottom-up
- [ ] 🔴 LL(1): FIRST/FOLLOW, parsing table, conditions ✍️
- [ ] 🔴 LR family: LR(0) items, SLR, CLR(1), LALR; table construction, conflicts ✍️
- [ ] 🔴 Syntax-directed translation: SDD/SDT, synthesized vs inherited attributes, evaluation ✍️
- [ ] 🟡 Runtime environments: activation records, calling conventions
- [ ] 🟠 Intermediate code generation: 3-address code, quadruples ✍️
- [ ] 🟡 Local optimization; data-flow analyses: constant propagation, liveness, CSE ✍️ (new explicit syllabus item)

### 8. OS

- [ ] 🟠 System calls, processes, threads, IPC ✍️
- [ ] 🔴 Concurrency & synchronization: critical section, semaphores, mutex, classical problems, race analysis ✍️
- [ ] 🔴 Deadlock: conditions, RAG, prevention/avoidance, Banker's algorithm ✍️
- [ ] 🔴 CPU scheduling: FCFS/SJF/SRTF/RR/priority numericals ✍️
- [ ] 🟡 I/O scheduling
- [ ] 🔴 Memory management: paging, segmentation, fragmentation ✍️
- [ ] 🔴 Virtual memory: demand paging, page replacement (FIFO/LRU/optimal), TLB, multi-level ✍️
- [ ] 🟠 File systems: allocation, Unix inodes, directories ✍️ (rising)

### 9. Databases

- [ ] 🟡 ER model: entities, relationships, constraints, mapping to tables ✍️
- [ ] 🔴 Relational algebra ✍️ · [ ] 🟠 Tuple relational calculus ✍️
- [ ] 🔴 SQL: joins, nested/correlated subqueries, aggregation, NULL semantics, DDL ✍️
- [ ] 🟡 Integrity constraints (PK/FK/check)
- [ ] 🔴 Normal forms: FDs, closure, candidate keys, 2NF/3NF/BCNF, lossless & dependency-preserving decomposition ✍️
- [ ] 🟡 File organization
- [ ] 🟠 Indexing: B trees, B+ trees (order, height, max keys) ✍️
- [ ] 🔴 Transactions: ACID, schedules, conflict/view serializability, recoverability, 2PL ✍️

### 10. Computer Networks (2027-trimmed syllabus)

- [ ] 🟡 Principles of layering, OSI vs TCP/IP concepts
- [ ] 🟡 Switching: circuit, packet, virtual circuit; performance metrics
- [ ] 🟠 Data link: error detection (CRC, checksum, Hamming), MAC sublayer, Ethernet ✍️
- [ ] 🟠 Routing: distance-vector (count-to-infinity), link-state ✍️
- [ ] 🔴 IPv4: fragmentation, CIDR/subnetting, NAT ✍️
- [ ] 🔴 TCP: flow control, congestion control (slow start/AIMD), socket API ✍️
- [ ] 🟡 DNS, HTTP
- [ ] 🟢 (Removed in 2027: UDP detail, SMTP/FTP/email, ARP/DHCP/ICMP, bridging — skip)

### General Aptitude (both papers, same syllabus)

- [ ] 🔴 Quantitative: ratios, percentages, powers/exponents/logarithms, P&C, series, mensuration, elementary statistics & probability, data interpretation (graphs, tables, maps)
- [ ] 🔴 Analytical: deduction/induction, analogy, numerical relations
- [ ] 🟠 Verbal: grammar (tenses, articles, prepositions, agreement), vocabulary/idioms, reading comprehension, narrative sequencing
- [ ] 🟡 Spatial: translation/rotation/scaling/mirroring, paper folding/cutting, 2-D/3-D patterns

## E.2 GATE DA

### 1. Probability & Statistics (85-mark technical paper's anchor)

- [ ] 🔴 Counting (P&C) in probability contexts ✍️
- [ ] 🔴 Probability axioms; sample space, events; independent & mutually exclusive events ✍️
- [ ] 🔴 Marginal, conditional, joint probability; Bayes theorem ✍️
- [ ] 🔴 Conditional expectation and variance (tower rule) ✍️
- [ ] 🔴 Mean, median, mode, standard deviation; correlation, covariance ✍️
- [ ] 🔴 Discrete RVs & PMF: uniform, Bernoulli, binomial ✍️
- [ ] 🔴 Continuous RVs & PDF/CDF: uniform, exponential, Poisson, normal, standard normal, t, χ² ✍️
- [ ] 🟠 Conditional PDF; cumulative distribution function properties ✍️
- [ ] 🔴 Central limit theorem ✍️
- [ ] 🔴 Confidence intervals ✍️
- [ ] 🔴 Hypothesis tests: z-test, t-test, chi-squared test ✍️
- [ ] 🟠 Estimator properties (unbiasedness, variance), MLE-style questions ✍️

### 2. Linear Algebra

- [ ] 🔴 Vector spaces, subspaces, linear dependence/independence ✍️
- [ ] 🔴 Matrices & properties: projection, orthogonal, idempotent, partition; quadratic forms ✍️
- [ ] 🔴 Systems of linear equations; Gaussian elimination ✍️
- [ ] 🔴 Eigenvalues/eigenvectors ✍️
- [ ] 🔴 Determinant, rank, nullity ✍️
- [ ] 🔴 Projections; projection matrix ✍️
- [ ] 🟠 LU decomposition ✍️
- [ ] 🟠 Singular value decomposition; singular values ✍️

### 3. Calculus & Optimization

- [ ] 🔴 Functions of a single variable: limit, continuity, differentiability ✍️
- [ ] 🟡 Taylor series ✍️
- [ ] 🔴 Maxima and minima; single-variable optimization ✍️
- [ ] 🟡 Convexity ideas (as they surface in ML contexts)

### 4. Programming, Data Structures & Algorithms

- [ ] 🔴 Programming in Python: recursion, functions/closures, lists/sets/dicts, slicing, mutable defaults ✍️
- [ ] 🔴 Basic DS: stacks, queues, linked lists, trees, hash tables ✍️
- [ ] 🔴 Search: linear, binary ✍️
- [ ] 🔴 Basic sorts: selection, bubble, insertion ✍️
- [ ] 🔴 Divide & conquer: mergesort, quicksort ✍️
- [ ] 🟠 Graph theory intro; traversals, shortest path (basic) ✍️
- [ ] 🟡 Complexity counting for standard algorithms ✍️

### 5. Database Management & Warehousing

- [ ] 🔴 ER model; relational model: relational algebra, tuple calculus, SQL ✍️
- [ ] 🔴 Integrity constraints; normal forms ✍️
- [ ] 🔴 File organization; indexing ✍️
- [ ] 🟡 Data types; data transformation: normalization (min-max), discretization, sampling, compression ✍️
- [ ] 🟠 Data warehouse modelling: multidimensional schemas (star/snowflake), concept hierarchies, cuboids, OLAP (ROLLUP/CUBE), measures ✍️

### 6. Machine Learning
**Supervised**

- [ ] 🔴 Regression vs classification framing; simple & multiple linear regression (closed forms, assumptions) ✍️
- [ ] 🔴 Ridge regression (effect of λ, closed form) ✍️
- [ ] 🔴 Logistic regression ✍️
- [ ] 🔴 k-NN ✍️ · [ ] 🔴 Naive Bayes ✍️
- [ ] 🟠 Linear discriminant analysis ✍️
- [ ] 🔴 Support vector machine (hard margin: support vectors, margin) ✍️
- [ ] 🔴 Decision trees (impurity, information gain) ✍️
- [ ] 🔴 Bias-variance trade-off ✍️
- [ ] 🟠 Cross-validation: LOO, k-fold ✍️
- [ ] 🟠 Multi-layer perceptron, feed-forward networks, perceptron updates, backprop gradients ✍️

**Unsupervised**

- [ ] 🔴 k-means / k-medoid ✍️
- [ ] 🔴 Hierarchical clustering: top-down/bottom-up, single/complete linkage ✍️
- [ ] 🔴 PCA: covariance eigen-decomposition, projections ✍️
- [ ] 🟠 Dimensionality reduction concepts
- [ ] 🟠 Evaluation metrics (accuracy, precision/recall/F1, confusion matrix)

### 7. AI

- [ ] 🔴 Uninformed search (BFS/DFS/UCS properties) ✍️
- [ ] 🔴 Informed search: heuristics, A*, admissibility ✍️
- [ ] 🔴 Adversarial search: minimax, alpha-beta pruning ✍️
- [ ] 🔴 Propositional logic: entailment, validity, equivalence ✍️
- [ ] 🔴 Predicate (first-order) logic ✍️
- [ ] 🟠 Reasoning under uncertainty: conditional independence, Bayes nets, variable elimination ✍️
- [ ] 🟠 Approximate inference: sampling (rejection, Gibbs) ✍️
- [ ] 🟢 CSP/planning — not in GATE 2027 DA syllabus (skip)

### Shared with CSE — already ticked above
GA (identical), DBMS core (SQL/normalization/indexing), DS & algorithms core, probability & linear algebra core, logic, combinatorics, graph theory.
