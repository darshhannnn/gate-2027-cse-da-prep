#!/usr/bin/env python3
"""Generate checklist_data.json for the GATE plan website.

Includes:
- Official GATE 2027 syllabi (CS + DA)
- Exact PYQ book chapters, section numbers, topic names, and question counts across:
  * Core CS Book (Ch 1–10: Algorithms, COA, Compiler Design, Computer Networks, Databases, Digital Logic, OS, Data Structures, Programming in C, TOC)
  * Engineering & Discrete Math + GATE General Aptitude Book (Ch 1–11)
  * Practice Aptitude Book (Ch 1 Data Interpretation, Ch 2 Logical Reasoning, Ch 5 English Language, Ch 7 Quantitative Aptitude, Ch 8 Spatial Aptitude)
- All DA syllabus topics and DA extensions (Python, AI Search, AI Uncertainty, Machine Learning, Data Warehousing, DA Linear Algebra/Calculus/Probability/Stats extensions)
- First 4 subtopics of each row preserved in order so any existing localStorage subtopic ticks remain aligned.
"""
import json

def T(tier, topic, subs, freq, patterns, tests):
    return {"tier": tier, "topic": topic,
            "subs": [{"n": n, "p": p} for n, p in subs],
            "freq": freq, "patterns": patterns, "tests": tests}

G = []

# 1 ------------------------------------------------------------------ EM+DM
G.append({"name": "1. Engineering Mathematics & Discrete Mathematics", "note": "Common to both papers (~13-mark block in CS; feeds DA maths) · Book Ch 1–7 (653 Qs)",
"rows": [
T(1, "Propositional Logic and First-Order Logic", [
    ("Truth tables, equivalences, normal forms, inference, resolution [Both] · Book Ch 3: 3.3 Propositional Logic (40), 3.2 Logical Reasoning (3)", "Both papers — Warm-up 1-mark material; 43 book PYQs"),
    ("Validity, satisfiability, counter-models [Both]", "Near-yearly: decide whether a formula set is valid/satisfiable"),
    ("FOL: quantifiers, translating sentences, unification and resolution [Both] · Book Ch 3: 3.1 First Order Logic (34)", "Alternate years; 2026 CSE and DA both had FOL validity questions; 34 book PYQs")],
    "7/10 years · 1–2 Qs · Book Ch 3 (77 Qs)",
    ["Decide validity/satisfiability of given formulas", "Translate English statements into FOL and negate them", "Count truth assignments / models"],
    ["20-min topic quiz after first pass (mix NAT+MSQ) — target 90%", "Add to Sunday mixed set until two clean passes"]),
T(1, "Sets, Relations, Functions, Partial Orders and Lattices", [
    ("Sets, relations, equivalence relations, partial orders, Hasse diagrams [CS] · Book Ch 4: 4.13 Set Theory (27), 4.12 Relations (37), 4.10 Partial Order (10), 4.2 Countable Uncountable Set (2)", "CS only — Basic 1-mark fodder inside combinatorics; 76 book PYQs"),
    ("Lattices and functions (including counting functions) [CS] · Book Ch 4: 4.3 Functions (29), 4.5 Identify Function (1), 4.9 Onto (1), 4.6 Lattice (10)", "CS only — Hasse-diagram questions alternate years; 41 book PYQs"),
    ("Monoids and groups (axioms) [CS] · Book Ch 4: 4.1 Binary Operation (8), 4.4 Group Theory (33), 4.7 Mathematical Induction (2), 4.8 Number Theory (7), 4.11 Polynomials (4)", "CS only — Group-axiom checks appear as quick 1-markers; 54 book PYQs")],
    "6/10 years · 1–2 Qs · Book Ch 4 (171 Qs)",
    ["Hasse diagram reading", "Classify relation properties", "Count functions/relations with constraints"],
    ["Include in the weekly sectional rotation"]),
T(1, "Graphs — Connectivity, Matching, Colouring", [
    ("Graph terms, degree, paths, cycles, connectivity, trees [Both] · Book Ch 2: 2.1 Counting (3), 2.2 Degree of Graph (12), 2.4 Graph Connectivity (40)", "Both papers — Degree-sum numericals are quick marks; 55 book PYQs"),
    ("Official CS graph core: connectivity, matching and colouring [CS] · Book Ch 2: 2.3 Graph Coloring (11), 2.5 Graph Isomorphism (3), 2.6 Graph Matching (1), 2.7 Graph Planarity (13)", "CS only — Chromatic number of standard graphs; 28 book PYQs")],
    "6/10 years · 1–2 Qs · Book Ch 2 (83 Qs)",
    ["Chromatic/connectivity properties", "Matching in bipartite graphs", "Counting labelled structures"],
    ["Weekly sectional inclusion"]),
T(1, "Combinatorics — Counting, Recurrence Relations, Generating Functions", [
    ("Counting, permutations and combinations [Both] · Book Ch 1: 1.1 Balls In Bins (4), 1.2 Combinatory (22), 1.3 Counting (4), 1.5 Modular Arithmetic (2), 1.6 Pigeonhole Principle (2), 1.8 Summation (3)", "Both papers — Every year somewhere (CSE math or DA P&S); 37 book PYQs"),
    ("Recurrence relations and generating functions [CS] · Book Ch 1: 1.4 Generating Functions (6), 1.7 Recurrence Relation (7)", "CS only — Solve-the-recurrence appears most years; generating functions alternate years; 13 book PYQs")],
    "8/10 years · 1–2 Qs · Book Ch 1 (50 Qs)",
    ["Count with constraints", "Solve recurrences", "Extract coefficients from generating functions"],
    ["Timed 10-question counting drill weekly in Phase 1"]),
T(1, "Linear Algebra — Matrices, Determinants, Systems of Linear Equations", [
    ("Matrix properties and determinants [Both] · Book Ch 6: 6.1 Cartesian Coordinates (1), 6.2 Determinant (11), 6.6 Matrix (22)", "Both papers — Trick determinants (DA 2024: det(M²+12M)); 34 book PYQs"),
    ("Gaussian elimination, solutions of linear systems [Both] · Book Ch 6: 6.4 Gaussian Elimination (1), 6.11 System of Equations (17)", "Both papers — Consistency/parametric solutions recur; 18 book PYQs")],
    "8/10 years · 2 Qs · Book Ch 6 Part 1 (52 Qs)",
    ["Solve/characterise systems", "Determinant shortcuts", "Rank arguments without full computation"],
    ["20-min quiz after first pass; re-solve misses at day 7"]),
T(1, "Linear Algebra — Eigenvalues and Eigenvectors", [
    ("Vector spaces, subspaces, linear independence, basis and dimension [Both] · Book Ch 6: 6.10 Subspace (1), 6.12 Vector Space (6)", "Both papers — DA 2024 and 2026 both asked subspace identification; 7 book PYQs"),
    ("Eigenvalues and eigenvectors [Both] · Book Ch 6: 6.3 Eigen Value (33)", "Both papers — Direct computation almost every year across both papers; 33 book PYQs"),
    ("Projections, Orthonormality & Quadratic forms [DA + Both] · Book Ch 6: 6.7 Orthonormality (2)", "DA extension — Ties into regression & PCA (DA ML) questions; 2 book PYQs")],
    "8/10 years · 1–2 Qs · Book Ch 6 Part 2 (42 Qs)",
    ["Compute eigen-pairs fast", "Aⁿ without multiplying", "Eigen-based arguments about rank/invertibility"],
    ["Include in Saturday mixed set"]),
T(1, "Linear Algebra — LU Decomposition, Rank, Nullity", [
    ("LU decomposition, rank and nullity [Both] · Book Ch 6: 6.5 Lu Decomposition (1), 6.8 Rank of Matrix (6)", "Both papers — Mechanical; know the count of operations & rank-nullity theorem; 7 book PYQs"),
    ("Projection matrix, orthogonal matrix, idempotent matrix and partition matrices [DA] · Book Ch 6: 6.6 Matrix (22), 6.7 Orthonormality (2)", "DA extension — DA 2025: rank of I+xxᵀ; official DA wording includes each matrix type"),
    ("Singular value decomposition [DA] · Book Ch 6: 6.9 Singular Value Decomposition (1)", "DA extension — DA 2024: rank-1 uuᵀ; DA 2025: singular values of a projection; 1 book PYQ")],
    "3/3 DA years · 1–2 Qs · Book Ch 6 Part 3 (8 Qs)",
    ["Special matrix shortcuts", "Compute singular values of small matrices"],
    ["Fold into the Linear Algebra topic quiz"]),
T(1, "Probability — Conditional Probability and Bayes Theorem", [
    ("Probability axioms, sample spaces and events; counting, conditional probability, independence, mutually exclusive events and Bayes' theorem [Both] · Book Ch 7: 7.1 Bayes Theorem (1), 7.5 Conditional Probability (14), 7.9 Independent Events (6), 7.12 Probability (28)", "Both papers — Foundation for nearly every probability question; 49 book PYQs"),
    ("Joint, marginal and conditional probability & Bayesian Networks [DA] · Book Ch 7: 7.2 Bayesian Network (2)", "DA extension — DA asks marginal/conditional & Bayes nets nearly every year; 2 book PYQs")],
    "9/10 years · 2–3 Qs · Book Ch 7 Part 1 (51 Qs)",
    ["Bayes with base rates", "Independence factorisation checks (DA 2024)", "Total-probability partitions"],
    ["This is the highest-ROI quiz in the plan — 20-min drill weekly"]),
T(1, "Probability Distributions — Uniform, Normal, Exponential, Poisson, Binomial", [
    ("Probability mass function, probability density function, cumulative distribution function [Both] · Book Ch 7: 7.13 Probability Density Function (1), 7.14 Probability Distribution (1), 7.15 Random Variable (8)", "Both papers — Quick 1-markers; 10 book PYQs"),
    ("Uniform, Bernoulli, binomial and Poisson distributions [Both] · Book Ch 7: 7.3 Bernoulli (1), 7.4 Binomial (6), 7.11 Poisson (4), 7.18 Uniform Distribution (10)", "Both papers — Estimator-style questions (DA 2025 unbiased p̂); 21 book PYQs"),
    ("Exponential, normal and standard normal distributions [Both] · Book Ch 7: 7.6 Continuous Distribution (1), 7.8 Exponential (5), 7.10 Normal Distribution (2)", "Both papers — Standardisation numericals; ties into CLT; 8 book PYQs")],
    "9/10 years · 2–3 Qs · Book Ch 7 Part 2 (39 Qs)",
    ["Recognise the distribution, then compute", "Memorylessness and merging properties", "Standardisation"],
    ["Distribution-recognition drill: 15 mixed questions weekly"]),
T(1, "Mean, Median, Mode, Standard Deviation, Variance", [
    ("Expectation, variance, mean, median, mode, standard deviation [Both] · Book Ch 7: 7.7 Expectation (13), 7.16 Square Invariant (1), 7.17 Statistics (2), 7.19 Variance (1)", "Both papers — DA 2026 used the pairwise-sum identity; 17 book PYQs"),
    ("Conditional expectation and conditional variance [DA]", "DA only — DA 2025 direct question on tower rule")],
    "6/10 years · 1 Q · Book Ch 7 Part 3 (17 Qs)",
    ["Compute/compare moments", "Variance identity shortcuts"],
    ["Fold into probability drill"]),
T(2, "Calculus — Limits, Continuity, Differentiability, Maxima and Minima", [
    ("Functions of a single variable, limits, continuity and differentiability [Both] · Book Ch 5: 5.1 Continuity (9), 5.3 Differentiation (10), 5.5 Limits (15), 5.7 Polynomials (2)", "Both papers — DA 2025: lim(√(t²+t)−t); 36 book PYQs"),
    ("Maxima and minima, single-variable optimization [Both] · Book Ch 5: 5.6 Maxima Minima (13)", "Both papers — DA all three years (quartic/cubic/cubic); 13 book PYQs")],
    "5/10 years (CS) · heavier in DA · Book Ch 5 Part 1 (49 Qs)",
    ["Critical points and classification", "Differentiability checks at joints"],
    ["Fold into Calculus & Optimisation quiz (DA group 12)"]),
T(3, "Calculus — Mean Value Theorem, Integration", [
    ("Mean value theorems [CS] · Book Ch 5: 5.3 Differentiation (10)", "CS only — Statement-level questions only"),
    ("Definite and indefinite integration [CS] · Book Ch 5: 5.2 Definite Integral (3), 5.4 Integration (11)", "CS only — Occasional 1-mark; supports probability densities; 14 book PYQs"),
    ("Taylor and Maclaurin series [DA]", "DA extension — DA 2025: 10th derivative of sinh")],
    "3/10 years · ≤1 Q · Book Ch 5 Part 2 (14 Qs) + DA Taylor",
    ["Integral properties", "Density-based areas", "Know 6 Taylor expansions cold"],
    ["Low priority: solve PYQs once + flashcard Taylor expansions"]),
]})

# 2 ------------------------------------------------------------------ PDSA
G.append({"name": "2. Programming, Data Structures and Algorithms", "note": "Common core — highest return for both papers (~16–18 marks in CS) · Core CS Book Ch 1 (334), Ch 8 (236), Ch 9 (127)",
"rows": [
T(1, "Programming in C (and Python for the DA paper) — Recursion", [
    ("C: pointers, arrays, parameter passing, scope [CS] · Core CS Ch 9: 9.1 Aliasing (1), 9.2 Array (10), 9.7 Output (10), 9.8 Parameter Passing (12), 9.9 Pointers (14), 9.14 Strings (1), 9.19 Variable Binding (1)", "C output-tracing is asked every single year (3–5 Qs); 49 book PYQs"),
    ("C: constructs, structs, unions, type checking [CS] · Core CS Ch 9: 9.4 Goto (2), 9.6 Loop Invariants (8), 9.10 Programming Constructs (1), 9.11 Programming In C (31), 9.12 Paradigms (2), 9.15 Structure (5), 9.16 Switch Case (2), 9.17 Type Checking (1), 9.18 Union (1)", "sizeof array-vs-pointer and struct/union patterns recur; 53 book PYQs"),
    ("Recursion: call trees, counting calls [Both] · Core CS Ch 9: 9.3 Functions (1), 9.5 Identify Function (6), 9.13 Recursion (18) & Ch 1: 1.28 Recursion (4)", "Call-count and return-value tracing every year; 29 book PYQs"),
    ("Python (DA Extension): closures, mutable default arguments, functions & scope [DA]", "DA 2026: mutable default — the classic trap"),
    ("Python (DA Extension): list/set/dict/tuple behaviour, slicing & code tracing [DA]", "2–4 Python output questions per DA paper")],
    "10/10 years · 3–5 Qs · Core CS Ch 9 (127 Qs)",
    ["Trace the exact output", "Count recursive calls", "Spot aliasing/mutation effects"],
    ["Daily 30-min tracing drill through Phase 1–2 (this tab's single best habit)"]),
T(1, "Arrays, Stacks, Queues, Linked Lists", [
    ("Multi-dimensional array addressing [Both] · Core CS Ch 8: 8.2 Array (13), 8.6 Data Structures (5), 8.10 Number of Swap (1), 8.14 Time Complexity (1)", "Row/column-major address numericals, alternate years; 20 book PYQs"),
    ("Stack applications: expression evaluation [Both] · Core CS Ch 8: 8.8 Infix Prefix (5), 8.13 Stack (18)", "Postfix/infix evaluation and stack traces; 23 book PYQs"),
    ("Circular queues and deques [Both] · Core CS Ch 8: 8.12 Queue (14)", "DA 2024 asked deque operation sequences; 14 book PYQs"),
    ("Linked-list pointer manipulation [Both] · Core CS Ch 8: 8.9 Linked List (23)", "Pointer-swap/output questions alternate years; 23 book PYQs")],
    "8/10 years · 1–2 Qs · Core CS Ch 8 Part 1 (80 Qs)",
    ["Trace data-structure operation sequences", "Address calculation", "Spot pointer bugs"],
    ["Include in the weekly programming drill"]),
T(1, "Trees — Binary Trees, Binary Search Trees", [
    ("Traversals (pre/in/post/level) & tree properties [Both] · Core CS Ch 8: 8.5 Binary Tree (53), 8.15 Tree (14)", "Every year in some form across both papers; 67 book PYQs"),
    ("BST insert/delete/search [Both] · Core CS Ch 8: 8.4 Binary Search Tree (36)", "Comparison counts and resulting shapes; 36 book PYQs"),
    ("AVL tree rotations & height balance [Both] · Core CS Ch 8: 8.1 AVL Tree (6)", "LL/RR/LR/RL rotation traces; 6 book PYQs"),
    ("Construction from pre+in / post+in [Both]", "DA 2026 asked reconstruction"),
    ("Full/complete binary tree relations [Both]", "DA 2024: height vs internal vs leaf counts")],
    "9/10 years · 1–2 Qs · Core CS Ch 8 Part 2 (109 Qs)",
    ["Reconstruct trees from orders", "Count comparisons/nodes", "Identify valid BST sequences"],
    ["Topic quiz after first pass; add to Sunday mixed set"]),
T(1, "Heaps and Priority Queues", [
    ("Heapify, insert, delete-min [CS] · Core CS Ch 8: 8.3 Binary Heap (29)", "Element-comparison counting recurs; 29 book PYQs"),
    ("Priority queue operations [CS] · Core CS Ch 8: 8.11 Priority Queue (2)", "O(n) build-heap vs O(n log n) distinction — classic MCQ; 2 book PYQs"),
    ("Heapsort and k-largest elements [CS]", "Conceptual frequency"),
    ("d-heaps / k-way merge (light) [CS]", "Rare; know the idea")],
    "6/10 years · 1 Q · Core CS Ch 8 Part 3 (31 Qs)",
    ["Trace heap operations", "Count comparisons", "Complexity distinctions"],
    ["Include in DS sectional"]),
T(1, "Graphs — Representation, Traversals (BFS, DFS)", [
    ("Adjacency matrix vs list trade-offs [Both] · Core CS Ch 1: 1.10 Directed Graph (1), 1.13 Graph Algorithms (11)", "1-mark property questions; 12 book PYQs"),
    ("BFS/DFS mechanics and complexity [Both] · Core CS Ch 1: 1.8 Depth First Search (1), 1.14 Graph Search (22)", "DA 2024 DFS properties; DA 2026 DFS question; 23 book PYQs"),
    ("Connected components, SCCs, cycles, bipartiteness [Both] · Core CS Ch 1: 1.33 Strongly Connected Components (3)", "Applications appear as twist questions; 3 book PYQs"),
    ("Topological sort of DAGs [Both] · Core CS Ch 1: 1.35 Topological Sort (4)", "DA 2024: count valid orderings; 4 book PYQs")],
    "8/10 years · 1–2 Qs · Core CS Ch 1 Graph Part 1 (42 Qs)",
    ["Trace traversal orders", "Count orderings/components", "Complexity under both representations"],
    ["Graph drill fortnightly"]),
T(1, "Hashing", [
    ("Chaining and load factor [Both] · Core CS Ch 8: 8.7 Hashing (16) & Ch 1: 1.16 Hashing (7)", "Expected search cost numericals; 23 book PYQs"),
    ("Open addressing: linear/double/uniform probing [Both] · Core CS Ch 1: 1.11 Double Hashing (1), 1.20 Linear Probing (1)", "DA 2024 uniform hashing; DA 2025 linear-probing trace; 2 book PYQs"),
    ("Hash function properties [Both]", "Simple 1-markers")],
    "6/10 years · 1 Q · Core CS Ch 8 & Ch 1 (25 Qs)",
    ["Count probes exactly", "Load-factor formulas"],
    ["Trace 20 probe-sequence problems across prep"]),
T(1, "Searching and Sorting Algorithms", [
    ("Binary search variants and comparison counts [Both] · Core CS Ch 1: 1.6 Binary Search (3), 1.7 Bitonic Array (1), 1.29 Searching (7)", "DA 2025: array vs linked-list binary search; 11 book PYQs"),
    ("Insertion/selection/bubble counts [Both] · Core CS Ch 1: 1.19 Insertion Sort (3), 1.31 Sorting (28)", "DA 2025: insertion-sort swap count; DA 2026 bubble vs insertion; 31 book PYQs"),
    ("Merge sort and quicksort behaviour [Both] · Core CS Ch 1: 1.22 Merge Sort (3), 1.23 Merging (2), 1.26 Quick Sort (14)", "DA 2026: first-element-pivot quicksort; 2024 in-place quicksort; 19 book PYQs"),
    ("Stability and in-place properties [Both]", "DA 2024 sort-stability question; recurring MCQ")],
    "9/10 years · 1–2 Qs · Core CS Ch 1 Search/Sort (61 Qs)",
    ["Count comparisons/swaps exactly", "Match algorithm to property", "Trace one partition pass"],
    ["Sorting-property flashcards + fortnightly drill"]),
T(1, "Asymptotic Worst-Case Time and Space Complexity", [
    ("O/Ω/Θ comparisons of functions [Both] · Core CS Ch 1: 1.3 Asymptotic Notation (7), 1.4 Asymptotic Notations (14)", "Near-every-year ranking question; 21 book PYQs"),
    ("Running time of code snippets [Both] · Core CS Ch 1: 1.18 Identify Function (38), 1.32 Space Complexity (1), 1.34 Time Complexity (29)", "Loop-analysis 1–2 markers; 68 book PYQs"),
    ("Best vs worst vs average case [Both] · Core CS Ch 1: 1.1 Algorithm Design (8), 1.2 Algorithm Design Technique (9)", "Sorting/algorithm-specific cases; 17 book PYQs")],
    "9/10 years · 1–2 Qs · Core CS Ch 1 Complexity (106 Qs)",
    ["Rank functions by growth", "Analyse nested loops", "Identify amortised twists"],
    ["Flashcards + include in every sectional"]),
T(1, "Algorithm Design — Divide and Conquer", [
    ("Recurrence relations & Master theorem [CS] · Core CS Ch 1: 1.27 Recurrence Relation (35)", "Recurrence questions most years; 35 book PYQs"),
    ("Merge sort & Quick sort recurrences [Both] · Core CS Ch 1: 1.22 Merge Sort (3), 1.23 Merging (2), 1.26 Quick Sort (14)", "Standard D&C applications"),
    ("Recursion-tree/substitution methods & counting inversions [CS]", "When Master theorem doesn't apply — CSE 2026 favourite")],
    "6/10 years · 1 Q · Core CS Ch 1 Recurrences (35 Qs)",
    ["Solve recurrences", "Recognise non-standard forms"],
    ["Fold into complexity drill"]),
T(1, "Algorithm Design — Greedy Algorithms", [
    ("Huffman coding cost [CS] · Core CS Ch 1: 1.17 Huffman Code (6)", "Huffman tree construction numericals recur; 6 book PYQs"),
    ("Activity selection, fractional knapsack & greedy paradigms [CS] · Core CS Ch 1: 1.15 Greedy Algorithms (5)", "Conceptual exchange-argument questions; 5 book PYQs"),
    ("Greedy correctness intuition [CS]", "2026 CSE-style: when greedy fails"),
    ("Greedy basis of MST [CS] · Core CS Ch 1: 1.24 Minimum Spanning Tree (34), 1.25 Prims Algorithm (2)", "Bridge to graph algorithms; 36 book PYQs")],
    "6/10 years · 1 Q · Core CS Ch 1 Greedy (11 Qs)",
    ["Build Huffman trees", "Spot greedy counter-examples"],
    ["Include in algorithms sectional"]),
T(1, "Algorithm Design — Dynamic Programming", [
    ("Standard DP problems (LCS, 0/1 knapsack, subset sum) [CS] · Core CS Ch 1: 1.12 Dynamic Programming (9)", "Conceptual state-design questions; 9 book PYQs"),
    ("Matrix Chain Multiplication [CS] · Core CS Ch 1: 1.21 Matrix Chain Ordering (3)", "Optimal parenthesization & scalar multiplication count; 3 book PYQs"),
    ("DP vs greedy vs divide-conquer [CS]", "2026 CSE asked a non-standard DP — the separator"),
    ("Memoisation mechanics [CS]", "Subdependency tracing")],
    "5/10 years · 1–2 Qs · Core CS Ch 1 DP (12 Qs)",
    ["Define states correctly", "Count solutions", "Prove optimal substructure informally"],
    ["Solve 30 classic DP PYQs topic-wise; no cramming"]),
T(1, "Graph Algorithms — Minimum Spanning Tree, Shortest Paths", [
    ("Prim and Kruskal traces [CS] · Core CS Ch 1: 1.24 Minimum Spanning Tree (34), 1.25 Prims Algorithm (2)", "MST edge-selection and uniqueness questions; 36 book PYQs"),
    ("Dijkstra [Both] · Core CS Ch 1: 1.9 Dijkstras Algorithm (6), 1.30 Shortest Path (9)", "2026 CSE: modified Dijkstra — hardest question of the paper; 15 book PYQs"),
    ("Dijkstra with negative edges [Both]", "Why-it-fails conceptual staple"),
    ("Bellman-Ford and Floyd-Warshall shortest paths [CS] · Core CS Ch 1: 1.5 Bellman Ford (2)", "Property comparisons recur; 2 book PYQs"),
    ("DA AI Extension: BFS/DFS/Dijkstra -> Uninformed (UCS/IDS), Informed (Greedy, A*) & Adversarial (Minimax, Alpha-Beta) Search [DA]", "Direct extension of Graph Search & Shortest Paths for DA AI")],
    "9/10 years · 1–2 Qs · Core CS Ch 1 MST/SP (53 Qs)",
    ["Trace algorithms step-by-step", "Prove/disprove properties", "Modified-algorithm analysis"],
    ["The single most important algorithms quiz — fortnightly full drill"]),
]})

# 3 ------------------------------------------------------------------ COA
G.append({"name": "3. Computer Organization and Architecture", "note": "Mainly Computer Science paper (~9 marks; the rank-decider) · Core CS Book Ch 2 (238 Qs)",
"rows": [
T(1, "Machine Instructions and Addressing Modes", [
    ("Instruction set, addressing modes, instruction format [CS] · Core CS Ch 2: 2.1 Addressing Modes (18), 2.3 CISC RISC Architecture (2), 2.11 Instruction Format (9), 2.12 Instruction Set Architecture (1), 2.14 Machine Instruction (21), 2.18 Runtime Environment (2)", "Instruction-size/field numericals; Identify mode / compute EA — recurring; 53 book PYQs")],
    "6/10 years · 1 Q · Core CS Ch 2 ISA (53 Qs)",
    ["Compute effective addresses", "CPI from instruction mix"],
    ["Topic quiz after first pass"]),
T(1, "Arithmetic Logic Unit, Datapath and Control Unit", [
    ("Arithmetic logic unit, clock cycles, datapath & instruction execution [CS] · Core CS Ch 2: 2.5 Clock Cycles (1), 2.8 Data Path (7), 2.10 Instruction Execution (6)", "ALU operations and flags; 14 book PYQs"),
    ("Control unit design: hardwired and microprogrammed [CS] · Core CS Ch 2: 2.16 Microprogramming (13)", "Horizontal vs vertical microinstruction sequencing appears alternate years; 13 book PYQs")],
    "4/10 years · 1 Q · Core CS Ch 2 Datapath/CU (27 Qs)",
    ["Adder delay arithmetic", "Micro-program sequencing"],
    ["Light drill; fold into COA sectional"]),
T(1, "Instruction Pipelining and Pipeline Hazards", [
    ("Pipelining, data dependency, hazards, forwarding & speedup [CS] · Core CS Ch 2: 2.7 Data Dependency (2), 2.17 Pipelining (43), 2.19 Speedup (4)", "The signature COA question — ~9/10 years; Exact-cycle tracing in 2026-style questions; 49 book PYQs")],
    "9/10 years · 2 Qs · Core CS Ch 2 Pipelining (49 Qs)",
    ["Count exact cycles with/without forwarding", "Compute throughput/speedup", "Reorder code to avoid stalls"],
    ["COA's must-drill: 25 numericals topic-wise, re-solve misses weekly"]),
T(1, "Memory Hierarchy — Cache Memory", [
    ("Cache mapping (direct, associative, set-associative), write policies and average memory access time [CS] · Core CS Ch 2: 2.2 Average Memory Access Time (2), 2.4 Cache Memory (73)", "Tag/index/offset split — near-every-year; 2026 CSE: multi-level cache numerical; 75 book PYQs")],
    "9/10 years · 2 Qs · Core CS Ch 2 Cache (75 Qs)",
    ["Compute AMAT exactly", "Split address fields", "Count misses for access patterns"],
    ["Second must-drill: 25 numericals + formula card"]),
T(2, "Main Memory and Secondary Storage", [
    ("Memory interfacing, chip expansion, virtual memory and secondary storage [CS] · Core CS Ch 2: 2.15 Memory Interfacing (6), 2.20 Virtual Memory (3) & Ch 7: 7.3 Disk (31)", "Chip-interfacing and disk transfer-time numericals; 9 COA book PYQs")],
    "4/10 years · 1 Q · Core CS Ch 2 Memory Interfacing (9 Qs)",
    ["Compute chip counts & decoder lines", "Disk seek + rotational + transfer time"],
    ["Fold into COA sectional"]),
T(2, "I/O Interface — Interrupt and DMA", [
    ("I/O interface, interrupts and direct memory access [CS] · Core CS Ch 2: 2.6 DMA (9), 2.9 IO Handling (7), 2.13 Interrupts (9)", "Cycle-count numericals alternate years; Transfer-time numericals; 25 book PYQs")],
    "4/10 years · 1 Q · Core CS Ch 2 I/O & DMA (25 Qs)",
    ["Count I/O cycles", "Compare polling/interrupt/DMA overhead"],
    ["Fold into COA sectional"]),
]})

# 4 ------------------------------------------------------------------ OS
G.append({"name": "4. Operating Systems", "note": "Mainly Computer Science paper (~8–9 marks, consistently high) · Core CS Book Ch 7 (335 Qs)",
"rows": [
T(1, "Processes, Threads and Inter-Process Communication", [
    ("System calls, fork(), process states, PCB, context switching, protection [CS] · Core CS Ch 7: 7.1 Context Switch (4), 7.6 Fork System Call (7), 7.14 OS Protection (3), 7.18 Process (5), 7.25 System Calls (1)", "fork() process counting & state-diagram questions; 20 book PYQs"),
    ("Threads (user and kernel) [CS] · Core CS Ch 7: 7.26 Threads (10)", "Conceptual 1–2 marks; 10 book PYQs"),
    ("Central processing unit scheduling: FCFS, SJF, SRTF, Round Robin, Priority [CS] · Core CS Ch 7: 7.19 Process Scheduling (48), 7.24 Srtf (1)", "Gantt-chart numericals nearly every year; 49 book PYQs")],
    "5/10 years · 1 Q · Core CS Ch 7 Processes/Sched (79 Qs)",
    ["Count fork-created processes", "Identify shared vs private memory"],
    ["Fold into OS sectional"]),
T(1, "CPU Scheduling Algorithms", [
    ("Waiting/turnaround/response time [CS] · Core CS Ch 7: 7.19 Process Scheduling (48), 7.24 Srtf (1)", "Always part of the above"),
    ("Preemption effects and convoy avoidance [CS]", "Comparison questions"),
    ("Context switches and quantum choice [CS] · Core CS Ch 7: 7.1 Context Switch (4)", "Counting context switches — trap-rich")],
    "8/10 years · 1–2 Qs",
    ["Build exact Gantt charts", "Compute all three time metrics", "RR quantum effects"],
    ["Scheduling drill: 20 numericals topic-wise"]),
T(1, "Concurrency, Synchronisation and Deadlock", [
    ("Critical section problem, Peterson's solution, mutex, semaphores, classical problems, IPC [CS] · Core CS Ch 7: 7.9 Inter Process Communication (1), 7.17 Precedence Graph (3), 7.20 Process Synchronization (52), 7.23 Semaphore (10)", "Property-checking & semaphore trace questions; 66 book PYQs"),
    ("Deadlocks: conditions, resource allocation graphs, prevention, Banker's algorithm, detection, recovery [CS] · Core CS Ch 7: 7.2 Deadlock Prevention Avoidance Detection (4), 7.21 Resource Allocation (27), 7.22 Resource Allocation Graph (1)", "RAG cycle questions alternate years; 'safe ≠ all orders' trap; 32 book PYQs")],
    "9/10 years · 2 Qs · Core CS Ch 7 Sync/Deadlock (98 Qs)",
    ["Trace semaphore-guided executions", "Detect race conditions", "Banker's safe-sequence check"],
    ["Sync drill: 20 problems + trap list review"]),
T(1, "Memory Management and Virtual Memory", [
    ("Paging, multi-level page tables, TLB, segmentation [CS] · Core CS Ch 7: 7.12 Memory Management (10), 7.13 Multilevel Paging (1), 7.27 Virtual Memory (43)", "Page-number/offset split & EMAT numericals; 54 book PYQs"),
    ("Demand paging, page replacement (FIFO, Optimal, LRU), thrashing [CS] · Core CS Ch 7: 7.15 Optimal Page Replacement (1), 7.16 Page Replacement (33)", "Reference-string traces nearly every year; 34 book PYQs")],
    "8/10 years · 2 Qs · Core CS Ch 7 Memory/VM (88 Qs)",
    ["EMAT with TLB hit ratios (don't double-count!)", "Replacement traces", "Multi-level translation"],
    ["Paired with COA cache drill — same formula family"]),
T(2, "File Systems", [
    ("File systems, file allocation methods, free-space management [CS] · Core CS Ch 7: 7.5 File System (9), 7.11 Linked Allocation (1)", "Max-file-size indexed inode numericals; 10 book PYQs"),
    ("Disk & I/O scheduling: FCFS, SSTF, SCAN, C-SCAN, LOOK & interrupts [CS] · Core CS Ch 7: 7.3 Disk (31), 7.4 Disk Scheduling (14), 7.7 IO Handling (7), 7.8 Input Output (1), 7.10 Interrupts (6)", "Disk seek/rotational numericals alternate years; 59 book PYQs")],
    "5/10 years · 1 Q · Core CS Ch 7 Disk/File/IO (69 Qs)",
    ["Compute max file sizes", "Count disk accesses for a path lookup"],
    ["Rising topic: solve all decade PYQs here"]),
]})

# 5 ------------------------------------------------------------------ CN
G.append({"name": "5. Computer Networks", "note": "Mainly Computer Science paper (~8 marks); 2027 syllabus trimmed · Core CS Book Ch 4 (215 Qs)",
"rows": [
T(1, "Layering and Protocol Principles", [
    ("Principles of layering; circuit, packet and virtual-circuit switching; performance metrics [CS] · Core CS Ch 4: 4.7 Channel Utilization (1), 4.8 Communication (4), 4.18 Network Flow (4), 4.19 Network Layering (6), 4.21 Network Switching (4), 4.22 Osi Model (1), 4.23 Probability (1)", "1-mark conceptual; Delay-comparison numericals alternate years; 21 book PYQs")],
    "4/10 years · 1 Q · Core CS Ch 4 Layering (21 Qs)",
    ["Map functions to layers", "Switching delay comparisons"],
    ["Fold into CN sectional"]),
T(1, "IP Addressing, CIDR and NAT", [
    ("IPv4 fragmentation, CIDR subnetting/supernetting, NAT, ARP/ICMP/DHCP [CS] · Core CS Ch 4: 4.2 Arp (1), 4.13 Fragmentation (2), 4.14 IP Addressing (11), 4.15 IP Packet (11), 4.20 Network Protocols (10), 4.29 Subnetting (21)", "The perennial quick-mark numerical; Prefix-merging & Fragment-offset numericals; 56 book PYQs")],
    "8/10 years · 1–2 Qs · Core CS Ch 4 IP/Subnetting (56 Qs)",
    ["Subnet math without a calculator", "Aggregate prefixes", "Fragment reassembly sizing"],
    ["30-problem subnetting drill until 100% automatic"]),
T(1, "Routing — Distance Vector and Link State", [
    ("Distance vector and link state routing [CS] · Core CS Ch 4: 4.10 Distance Vector Routing (8), 4.24 Routing (13), 4.25 Routing Protocols (1)", "Distance-vector iteration questions; Link-state + Dijkstra overlaps algorithms; 22 book PYQs")],
    "6/10 years · 1 Q · Core CS Ch 4 Routing (22 Qs)",
    ["One DV exchange trace", "LS vs DV property comparison"],
    ["Fold into CN sectional"]),
T(1, "TCP and UDP — Flow Control and Congestion Control", [
    ("TCP flow control (sliding window) and congestion control; UDP; sockets [CS] · Core CS Ch 4: 4.9 Congestion Control (6), 4.26 Sliding Window (15), 4.27 Sockets (4), 4.28 Stop and Wait (6), 4.30 TCP (22), 4.31 Token Bucket (2), 4.32 UDP (4)", "Window-size/throughput numericals; 2026 CSE: congestion-window tracing; 59 book PYQs")],
    "8/10 years · 1–2 Qs · Core CS Ch 4 Transport/Window (59 Qs)",
    ["Trace cwnd evolution", "Window/throughput math", "Seq/ack number accounting"],
    ["TCP drill: 20 numericals; pair with subnetting drill"]),
T(2, "Data Link Layer — Framing, Error Detection, MAC", [
    ("Error detection, medium access control, Ethernet [CS] · Core CS Ch 4: 4.3 Bit Stuffing (2), 4.4 Bridges (3), 4.5 CRC Polynomial (4), 4.6 CSMA CD (6), 4.11 Error Detection (10), 4.12 Ethernet (7), 4.16 LAN Technologies (7), 4.17 MAC Protocol (5)", "CRC-polynomial division numericals; CSMA/CD backoff & min frame size; 44 book PYQs")],
    "5/10 years · 1 Q · Core CS Ch 4 DLL/MAC (44 Qs)",
    ["CRC division without errors", "Hamming-distance arguments"],
    ["Fold into CN sectional"]),
T(3, "Application Layer — DNS, HTTP, SMTP, FTP", [
    ("Domain Name System, HTTP, SMTP, FTP & POP3 [CS] · Core CS Ch 4: 4.1 Application Layer Protocols (12)", "1-mark conceptual; Object-fetch time numericals occasionally; 12 book PYQs")],
    "4/10 years · ≤1 Q · Core CS Ch 4 App Layer (12 Qs)",
    ["Resolution order", "HTTP timing basics"],
    ["PYQs once; no drilling"]),
]})

# 6 ------------------------------------------------------------------ DBMS
G.append({"name": "6. Database Management Systems", "note": "Common — extra warehousing for the DA paper; DA's fastest-rising section (8→18 marks) · Core CS Book Ch 5 (284 Qs)",
"rows": [
T(1, "Entity Relationship Model", [
    ("Entity-relationship model, relational model, keys, integrity constraints [Both] · Core CS Ch 5: 5.2 Candidate Key (5), 5.4 Database Design (1), 5.7 ER Diagram (12), 5.14 Referential Integrity (5), 5.17 Relational Model (2)", "Foundational for mapping questions; DA 2026: referential-integrity question; 25 book PYQs"),
    ("ER-to-relational mapping [Both]", "DA 2026: ER→3NF with multivalued attribute"),
    ("Weak entities and ISA hierarchies [Both]", "Occasional conceptual")],
    "5/10 years · 1 Q · Core CS Ch 5 ER/Keys (25 Qs)",
    ["Convert ER → tables correctly", "Handle multivalued/weak constructs"],
    ["Fold into DBMS sectional"]),
T(1, "Relational Model — Relational Algebra, Tuple Calculus, SQL", [
    ("Relational algebra and tuple relational calculus [Both] · Core CS Ch 5: 5.10 Joins (7), 5.12 Natural Join (3), 5.15 Relational Algebra (31), 5.16 Relational Calculus (15), 5.20 Tuple Relational Calculus (1)", "Both papers nearly every year; DA 2025 division; DA 2026 TRC count question; 57 book PYQs"),
    ("Structured Query Language: joins, grouping, aggregation, nested and correlated subqueries, views [Both] · Core CS Ch 5: 5.13 Query (1), 5.18 SQL (58)", "Every year; DA 2026 correlated COUNT; 59 book PYQs")],
    "9/10 years · 2 Qs · Core CS Ch 5 RA/TRC/SQL (116 Qs)",
    ["Translate SQL ↔ algebra", "Evaluate correlated subqueries row-by-row", "NULL three-valued logic"],
    ["SQL drill weekly — write every query by hand"]),
T(1, "Integrity Constraints and Normal Forms", [
    ("Functional dependencies, attribute closure, minimal cover [Both] · Core CS Ch 5: 5.2 Candidate Key (5), 5.8 Functional Dependency (2)", "Closure arithmetic — where silly marks die"),
    ("Normal forms through BCNF, lossless join, dependency preservation [Both] · Core CS Ch 5: 5.5 Database Normalization (56), 5.6 Decomposition (1), 5.11 Multivalued Dependency 4nf (1)", "Key-finding under partial FDs — every year; DA 2025 JOIN decomposition; 58 book PYQs")],
    "9/10 years · 2 Qs · Core CS Ch 5 Normalization (60 Qs)",
    ["Compute closures fast and clean", "Find all candidate keys", "Judge decompositions"],
    ["Normalization drill: 25 problems; show every closure step"]),
T(1, "Indexing — B Trees and B+ Trees", [
    ("File organization, indexing, B-trees and B+ trees [Both] · Core CS Ch 5: 5.1 B Tree (31), 5.9 Indexing (13)", "DA 2026 asked two B+ tree questions; Structure-tracing questions; 44 book PYQs")],
    "6/10 years · 1–2 Qs · Core CS Ch 5 B-Tree/Indexing (44 Qs)",
    ["Order/height arithmetic", "Trace insertions with splits"],
    ["Include in DBMS sectional"]),
T(1, "Transactions and Concurrency Control", [
    ("Transactions, ACID, conflict/view serializability, recoverability [CS] · Core CS Ch 5: 5.3 Conflict Serializable (9), 5.19 Transaction and Concurrency (30)", "Schedule analysis nearly every year; 39 book PYQs"),
    ("Concurrency control: two-phase locking, timestamp ordering, deadlock and recovery [CS]", "2PL-strictness comparisons")],
    "8/10 years · 1–2 Qs · Core CS Ch 5 Transactions (39 Qs)",
    ["Build precedence graphs", "Classify schedules", "Spot blind writes"],
    ["Serializability drill: 20 schedules"]),
T(2, "File Organisation", [
    ("File organization: ordered/unordered/hashed files, primary/secondary/clustering indexes [Both] · Core CS Ch 5: 5.9 Indexing (13)", "Block-factor and access-cost numericals; 13 book PYQs"),
    ("DA Data Preparation Extension: data types (nominal, ordinal, interval, ratio); transformation including normalization (min-max, z-score, decimal scaling), discretization, sampling and compression [DA]", "DA extension — Data preparation & preprocessing")],
    "2/3 DA years · 1 Q",
    ["Block-access arithmetic", "Normalization & discretization arithmetic"],
    ["PYQs once"]),
T(2, "Data Warehousing — Multidimensional Models (DA paper)", [
    ("Multidimensional models, star, snowflake and fact constellation schemas, concept hierarchies, OLAP operations (roll-up, drill-down, slice, dice, pivot), distributive/algebraic/holistic measures [DA]", "DA 2026: number of data cuboids; DA 2025: GROUP BY CUBE tuple count")],
    "2/3 DA years · 2–4 Qs and rising",
    ["Count cuboids from hierarchies", "Predict CUBE output sizes"],
    ["DA-specific: make a 1-page cuboid-formula card"]),
]})

# 7 ------------------------------------------------------------------ TOC
G.append({"name": "7. Theory of Computation", "note": "Mainly Computer Science paper (~8 marks; most stable subject) · Core CS Book Ch 10 (286 Qs)",
"rows": [
T(1, "Regular Expressions and Finite Automata", [
    ("Regular expressions, DFA/NFA/epsilon-NFA, minimization, Arden's theorem [CS] · Core CS Ch 10: 10.7 Finite Automata (42), 10.8 Finite State Machines (1), 10.10 Minimal State Automata (25), 10.11 Non Determinism (6), 10.12 Number of States (1), 10.17 Regular Expression (29), 10.18 Regular Grammar (3)", "Design questions nearly every year; 107 book PYQs"),
    ("Regular language closure properties [CS] · Core CS Ch 10: 10.1 Closure Property (9), 10.19 Regular Language (36)", "Closure-trap MCQs (complement/intersection); 45 book PYQs")],
    "9/10 years · 2 Qs · Core CS Ch 10 Regular/FA (152 Qs)",
    ["Convert and minimise quickly", "Apply closure rules correctly"],
    ["TOC drill: 30 design problems topic-wise"]),
T(1, "Context-Free Grammars and Push-Down Automata", [
    ("Context-free grammars, ambiguity, Chomsky normal form [CS] · Core CS Ch 10: 10.2 Context Free Grammar (2), 10.3 Context Free Language (33)", "Ambiguity demonstration recurs; Conversion numericals; 35 book PYQs"),
    ("Pushdown automata (DPDA vs NPDA) and CFL closure properties [CS] · Core CS Ch 10: 10.6 Dpda (1), 10.14 Pushdown Automata (15)", "Design + language matching; The complement/intersection trap — recurring; 16 book PYQs")],
    "8/10 years · 2 Qs · Core CS Ch 10 CFG/PDA (51 Qs)",
    ["Design grammars for languages", "Check ambiguity", "Apply CFL closures correctly"],
    ["Pair with regular-language drill"]),
T(2, "Pumping Lemma", [
    ("Pumping lemma for Regular and Context-Free Languages & non-regular/non-CFL tests [CS] · Core CS Ch 10: 10.13 Pumping Lemma (2), 10.9 Identify Class Language (31)", "Language-class separation & pumping lemma applications; 33 book PYQs")],
    "5/10 years · 1 Q · Core CS Ch 10 Pumping/Class (33 Qs)",
    ["Test non-regularity & non-context-freeness", "Distinguish DCFL vs NCFL"],
    ["Include in TOC sectional"]),
T(2, "Turing Machines and Undecidability", [
    ("Turing machines, recursive and recursively enumerable languages [CS] · Core CS Ch 10: 10.4 Countable Uncountable Set (3), 10.15 Recursive and Recursively Enumerable Languages (16)", "Language-class membership MCQs; 19 book PYQs"),
    ("Undecidability, halting problem, Rice's theorem & reductions [CS] · Core CS Ch 10: 10.5 Decidability (29), 10.16 Reduction (2)", "Rising trend in the last 5 years; 31 book PYQs")],
    "6/10 years · 1 Q and rising · Core CS Ch 10 TM/Decidability (50 Qs)",
    ["Classify languages", "Build simple reductions", "Apply Rice's theorem correctly"],
    ["Don't skip this — it's the modern differentiator"]),
]})

# 8 ------------------------------------------------------------------ CD
G.append({"name": "8. Compiler Design", "note": "Mainly Computer Science paper (~5–6 marks; parsing carries most of it) · Core CS Book Ch 3 (234 Qs)",
"rows": [
T(3, "Lexical Analysis", [
    ("Lexical analysis: tokens, lexemes, scanner, compilation phases & supporting systems [CS] · Core CS Ch 3: 3.1 Assembler (9), 3.5 Compilation Phases (12), 3.11 Lexical Analysis (6), 3.12 Linker (3), 3.14 Macros (4), 3.21 Symbol Table (1)", "1-mark conceptual; 35 book PYQs")],
    "4/10 years · ≤1 Q · Core CS Ch 3 Lexical/Phases (35 Qs)",
    ["Tokenise a snippet", "Recognise lexical vs syntax errors"],
    ["PYQs once"]),
T(2, "Parsing — Top-Down and Bottom-Up", [
    ("Parsing: FIRST and FOLLOW sets, LL(1), LR(0), SLR(1), CLR(1), LALR(1) & operator precedence [CS] · Core CS Ch 3: 3.7 First and Follow (6), 3.8 Grammar (51), 3.10 LR Parser (20), 3.15 Operator Precedence (3), 3.17 Parsing (27)", "Feeds every parsing question — arithmetic must be clean; 2026 CSE: LL(1) & LALR conflict questions; 107 book PYQs")],
    "8/10 years · 1–2 Qs · Core CS Ch 3 Parsing (107 Qs)",
    ["Build tables without arithmetic slips", "Count and classify conflicts"],
    ["Parsing drill: 20 table problems — CD's marks live here"]),
T(3, "Intermediate Code Generation", [
    ("Syntax-directed translation: S-attributed and L-attributed definitions [CS] · Core CS Ch 3: 3.6 Expression Evaluation (2), 3.22 Syntax Directed Translation (17)", "Translate-snippet questions alternate years; 19 book PYQs"),
    ("Intermediate code: three-address code, quadruples, triples & backpatching [CS] · Core CS Ch 3: 3.2 Backpatching (1), 3.9 Intermediate Code (11)", "Standard TAC forms; 12 book PYQs")],
    "5/10 years · 1 Q · Core CS Ch 3 SDT/ICG (31 Qs)",
    ["Emit 3-address code by hand", "Evaluate SDT attributes on parse trees"],
    ["PYQs once + one practice set"]),
T(3, "Runtime Environments", [
    ("Runtime environments, parameter passing, scope and activation records [CS] · Core CS Ch 3: 3.16 Parameter Passing (14), 3.19 Runtime Environment (22), 3.23 Variable Scope (2)", "Activation-tree & parameter-passing questions; 38 book PYQs")],
    "5/10 years · 1 Q · Core CS Ch 3 Runtime (38 Qs)",
    ["Track activation records across calls", "Static vs dynamic scoping traces"],
    ["PYQs once + one practice set"]),
T(3, "Data Flow Analysis — Liveness, Constant Propagation", [
    ("Basic blocks, control flow graphs, SSA form, local optimization [CS] · Core CS Ch 3: 3.3 Basic Blocks (1), 3.4 Code Optimization (10), 3.20 Static Single Assignment (3)", "New explicit syllabus item — expect growth; 14 book PYQs"),
    ("Constant propagation, liveness analysis, register allocation, common subexpression elimination [CS] · Core CS Ch 3: 3.13 Live Variable Analysis (3), 3.18 Register Allocation (6)", "All named compiler requirements are explicitly present; 9 book PYQs")],
    "2/10 years · new in syllabus · Core CS Ch 3 Optimization (23 Qs)",
    ["Compute IN/OUT sets on small CFGs"],
    ["Learn the framework once; do whatever PYQs exist"]),
]})

# 9 ------------------------------------------------------------------ DL
G.append({"name": "9. Digital Logic", "note": "Mainly Computer Science paper (~5 marks; highest marks-per-hour in the paper) · Core CS Book Ch 6 (303 Qs)",
"rows": [
T(3, "Boolean Algebra and Minimisation", [
    ("Boolean algebra, logic gates, canonical normal forms & functional completeness [CS] · Core CS Ch 6: 6.3 Boolean Algebra (34), 6.5 Canonical Normal Form (9), 6.16 Functional Completeness (7), 6.20 Min No Gates (4)", "Warm-up for K-map questions; 54 book PYQs"),
    ("Karnaugh maps, prime implicants, SOP/POS minimization, Quine-McCluskey & hazards [CS] · Core CS Ch 6: 6.18 K Map (20), 6.21 Min Products of Sum Form (2), 6.22 Min Sum of Products Form (15), 6.25 Prime Implicants (2), 6.30 Static Hazard (1)", "Nearly every year — fast marks; 40 book PYQs")],
    "7/10 years · 1 Q · Core CS Ch 6 Boolean/K-Map (94 Qs)",
    ["Minimise 3–4 variable functions", "Handle don't-cares correctly"],
    ["Speed drill: 15 K-maps"]),
T(3, "Combinational and Sequential Circuits", [
    ("Combinational circuits: multiplexers, decoders, adders, multipliers, ROM [CS] · Core CS Ch 6: 6.1 Adder (9), 6.2 Array Multiplier (2), 6.6 Carry Generator (2), 6.7 Circuit Output (40), 6.8 Combinational Circuit (2), 6.9 Decoder (3), 6.10 Digital Circuits (6), 6.19 Memory Interfacing (5), 6.23 Multiplexer (14), 6.26 ROM (4)", "MUX-implementation & circuit output questions; 87 book PYQs"),
    ("Sequential circuits: latches, flip-flops, counters, shift registers, FSMs [CS] · Core CS Ch 6: 6.11 Digital Counter (17), 6.12 Finite State Machines (4), 6.14 Flip Flop (6), 6.27 Ripple Counter Operation (1), 6.28 Sequential Circuit (1), 6.29 Shift Registers (2), 6.31 Synchronous Asynchronous Circuits (4)", "Counter-state tracing alternate years; 35 book PYQs")],
    "6/10 years · 1 Q · Core CS Ch 6 Circuits (122 Qs)",
    ["Trace flip-flop outputs cycle-by-cycle", "Implement functions with MUXes"],
    ["Include in DL sectional"]),
T(3, "Number Representations and Computer Arithmetic", [
    ("Number representation and arithmetic: two's complement, Booth's algorithm, fixed-point, floating-point (IEEE 754) [CS] · Core CS Ch 6: 6.4 Booths Algorithm (7), 6.13 Fixed Point Representation (2), 6.15 Floating Point Representation (12), 6.17 IEEE Representation (8), 6.24 Number Representation (58)", "Range/overflow & IEEE-754 numericals nearly every year; 87 book PYQs")],
    "6/10 years · 1 Q · Core CS Ch 6 Number/Arithmetic (87 Qs)",
    ["Convert/represent exactly", "IEEE-754 encode-decode both ways"],
    ["Make the IEEE-754 formula card — it always pays"]),
]})

# 10 ----------------------------------------------------------------- P&S
G.append({"name": "10. Probability and Statistics", "note": "Extra depth for the DA paper (~16–19 marks — its anchor section); also helps CS · Engg Math Book Ch 7 (107 Qs)",
"rows": [
T(1, "Random Variables — Discrete and Continuous", [
    ("Discrete random variables and PMFs; uniform, Bernoulli, binomial [Both] · Book Ch 7: 7.3 Bernoulli (1), 7.4 Binomial (6), 7.15 Random Variable (8), 7.18 Uniform Distribution (10)", "DA 2026: CDF property statements; Estimator-style questions (DA 2025 unbiased p̂); 25 book PYQs"),
    ("Continuous PDFs; uniform, exponential, Poisson, normal and standard normal [Both] · Book Ch 7: 7.6 Continuous Distribution (1), 7.8 Exponential (5), 7.10 Normal (2), 7.11 Poisson (4), 7.13 PDF (1), 7.14 Probability Distribution (1)", "DA 2024 identity; DA 2026 Poisson-limit sum; DA 2026: P(X>10|X>5); 14 book PYQs"),
    ("CDF and conditional PDF [DA]", "DA 2024: E[Y|X] from joint pdf")],
    "3/3 DA years · 3–4 Qs · Book Ch 7",
    ["Switch between PMF/PDF/CDF fluidly", "Compute moments of transformed RVs"],
    ["The DA anchor drill: 20 problems weekly until Phase 3"]),
T(1, "Joint, Marginal and Conditional Distributions", [
    ("Joint, marginal and conditional distributions, including conditional probability density functions for DA [DA] · Book Ch 7: 7.5 Conditional Probability (14), 7.12 Probability (28)", "Normalisation numericals; DA asks marginal/conditional nearly every year"),
    ("Independence verification [Both] · Book Ch 7: 7.9 Independent Events (6)", "Factorisation checks (DA 2024)")],
    "3/3 DA years · 2–3 Qs",
    ["Marginalise correctly", "Condition and renormalise"],
    ["Include in the DA anchor drill"]),
T(1, "Correlation, Covariance, Conditional Expectation", [
    ("Covariance and correlation [DA] · Book Ch 7: 7.7 Expectation (13), 7.19 Variance (1)", "DA 2024 coin-RV correlation; DA 2026 conditional-uniform correlation"),
    ("Conditional expectation and conditional variance [DA]", "DA 2025 direct question on tower rule; Pairs with tower rule")],
    "3/3 DA years · 2 Qs",
    ["Apply tower rule cleanly", "Expand variances via identities"],
    ["Add to anchor drill"]),
T(2, "Central Limit Theorem", [
    ("Central limit theorem, sample mean distribution [DA] · Book Ch 7: 7.10 Normal Distribution (2), 7.17 Statistics (2)", "DA 2025: CLT for a Bernoulli(0.25) sum; DA 2026: distribution of the sample mean")],
    "2/3 DA years · 1 Q",
    ["Standardise sums/means", "Judge when CLT applies"],
    ["Include in anchor drill"]),
T(2, "Confidence Intervals and Hypothesis Testing", [
    ("Confidence intervals [DA]", "Syllabus-explicit; expect growth"),
    ("Null and alternate hypotheses, z-test, t-test and chi-squared test [DA] · Book Ch 7: 7.17 Statistics (2)", "Direction traps; z vs t vs χ² decision rule")],
    "2/3 DA years · 1–2 Qs",
    ["Pick test and df correctly", "Read p-value direction"],
    ["Make a test-selection decision card"]),
T(2, "t-distribution and Chi-squared Distribution", [
    ("Student's t and chi-squared distributions [DA] · Book Ch 7: 7.16 Square Invariant (1), 7.17 Statistics (2)", "Small-sample tests; df rules are the trap")],
    "1/3 DA years · ≤1 Q",
    ["df arithmetic", "Match distribution to scenario"],
    ["Fold into hypothesis-testing drill"]),
]})

# 11 ----------------------------------------------------------------- LA
G.append({"name": "11. Linear Algebra", "note": "Extra depth for the DA paper (~8–11 marks); shared with CS maths · Engg Math Book Ch 6 (102 Qs)",
"rows": [
T(1, "Vector Spaces, Subspaces, Linear Dependence and Independence", [
    ("Vector spaces/subspaces, linear dependence/independence [Both] · Book Ch 6: 6.10 Subspace (1), 6.12 Vector Space (6)", "DA 2024 and 2026 both asked subspace identification; 7 book PYQs"),
    ("Spanning sets and orthonormal bases [Both] · Book Ch 6: 6.7 Orthonormality (2)", "DA 2025: orthonormal bases; 2 book PYQs"),
    ("Rank–nullity, systems of equations and dimension counting [Both] · Book Ch 6: 6.4 Gaussian Elimination (1), 6.5 Lu Decomposition (1), 6.8 Rank of Matrix (6), 6.11 System of Equations (17)", "Direct numericals; 25 book PYQs")],
    "3/3 DA years · 2 Qs · Book Ch 6",
    ["Test subspace axioms fast", "Count dimensions"],
    ["20-problem drill after first pass"]),
T(1, "Eigenvalues, Eigenvectors, Determinant", [
    ("Eigenvalues, determinants, matrix properties [Both] · Book Ch 6: 6.2 Determinant (11), 6.3 Eigen Value (33), 6.6 Matrix (22)", "DA eigen questions every year; DA 2026: rotation matrix M^2026; DA 2024: det(M²+12M); 66 book PYQs"),
    ("Quadratic forms, idempotent, orthogonal & partition matrices [DA]", "DA 2025/2026; Rayleigh quotient 2026")],
    "3/3 DA years · 2–3 Qs · Book Ch 6",
    ["Shortcut eigen-arguments", "Avoid full computation where possible"],
    ["Make the special-matrices card (rotation/idempotent/orthogonal/projection)"]),
T(2, "Singular Value Decomposition and Projections", [
    ("Projections & Cartesian geometry [DA] · Book Ch 6: 6.1 Cartesian Coordinates (1), 6.7 Orthonormality (2)", "DA 2025: singular values of a projection; Bridge into regression"),
    ("Singular value decomposition [DA] · Book Ch 6: 6.9 Singular Value Decomposition (1)", "DA 2024: rank-1 uuᵀ; DA 2025: norm-preserving ⟹ orthogonal; 1 book PYQ")],
    "2/3 DA years · 1–2 Qs",
    ["Compute singular values of small matrices", "Project vectors correctly"],
    ["Include in LA drill"]),
]})

# 12 ----------------------------------------------------------------- Calc
G.append({"name": "12. Calculus and Optimisation", "note": "Data Science paper (~5–9 marks) · Engg Math Book Ch 5 (63 Qs)",
"rows": [
T(2, "Functions of a Single Variable — Limits, Continuity, Differentiability", [
    ("Algebraic limits and expansions [Both] · Book Ch 5: 5.5 Limits (15), 5.7 Polynomials (2)", "DA 2025: lim(√(t²+t)−t); 17 book PYQs"),
    ("Piecewise continuity [Both] · Book Ch 5: 5.1 Continuity (9)", "DA 2024 continuity question; 9 book PYQs"),
    ("Differentiability of products/compositions [Both] · Book Ch 5: 5.3 Differentiation (10)", "DA 2025 statement question; 10 book PYQs"),
    ("Lipschitz-style statements [DA]", "DA 2025: |f(x)−f(y)|≤(x−y)²")],
    "3/3 DA years · 1–2 Qs · Book Ch 5",
    ["Expand near the point", "Check joints piecewise"],
    ["Fold into the optimisation quiz"]),
T(2, "Taylor Series", [
    ("Standard expansions (eˣ, sin, cos, sinh, ln) [DA]", "DA 2025: 10th derivative of sinh"),
    ("nth-derivative-at-a-point tricks [DA]", "Read coefficients off the series"),
    ("Derivatives of ML functions [DA]", "DA 2024: sigmoid derivative at a point")],
    "1–2/3 DA years · 1 Q",
    ["Know 6 expansions cold", "Match coefficient ↔ derivative"],
    ["Flashcard the expansions"]),
T(2, "Maxima, Minima and Optimisation of Single-Variable Functions", [
    ("Critical points and second-derivative test [Both] · Book Ch 5: 5.6 Maxima Minima (13)", "DA all three years (quartic/cubic/cubic); 13 book PYQs"),
    ("Convexity and global minima [DA]", "DA 2025: at-most-one-global-min statement"),
    ("ReLU/non-smooth differentiability [DA]", "DA 2025: ReLU differentiability question")],
    "3/3 DA years · 1–2 Qs",
    ["Classify stationary points", "Argue convexity when asked"],
    ["Topic quiz after PYQ pass"]),
]})

# 13 ----------------------------------------------------------------- ML
G.append({"name": "13. Machine Learning", "note": "Data Science paper (~11–14 marks, steady top-3 section) · DA Core Syllabus",
"rows": [
T(1, "Simple and Multiple Linear Regression, Ridge Regression", [
    ("Simple and multiple linear regression, ridge regression [DA] (Applies Engg Math Ch 6 Projections & Matrix 6.6/6.11)", "DA 2025: y=wx fitting; DA 2026 asked Ridge twice (incl. MAE objective)")],
    "3/3 DA years · 2 Qs",
    ["Derive/apply closed forms", "Reason about λ and shrinkage"],
    ["Regression drill: 15 numericals"]),
T(1, "Logistic Regression", [
    ("Logistic regression, sigmoid & cross-entropy [DA] (Applies Engg Math Ch 5 Calculus 5.3/5.6)", "Threshold/boundary questions; Decision boundary geometry")],
    "2/3 DA years · 1 Q",
    ["Compute probabilities at thresholds"],
    ["Fold into classification drill"]),
T(1, "k-Nearest Neighbours, Naive Bayes, Linear Discriminant Analysis", [
    ("k-nearest neighbour [DA]", "DA 2024 kNN question"),
    ("Naive Bayes classifier, linear discriminant analysis [DA] (Applies Engg Math Ch 7 Bayes 7.1 & Normal 7.10)", "DA 2024: parameter count for K binary attributes; DA 2025: which-class prediction; DA 2025: linearity of nearest-mean classifier")],
    "3/3 DA years · 1–2 Qs",
    ["Count NB parameters", "Apply kNN by hand"],
    ["Include in ML sectional"]),
T(1, "Support Vector Machine", [
    ("Support vector machine: hard/soft margin, dual & kernels [DA]", "DA 2025: margin √2, identify SVs; The core formula: Margin = 2/‖w‖")],
    "1–2/3 DA years · 1 Q",
    ["Find SVs and compute margins"],
    ["Make the SVM formula card"]),
T(1, "Decision Trees", [
    ("Decision trees: Entropy, Information Gain, Gini Impurity, splitting & pruning [DA]", "Split-selection numericals; Depth and overfitting conceptual")],
    "2/3 DA years · 1 Q",
    ["Compute gain for one split by hand"],
    ["Include in ML sectional"]),
T(1, "Bias-Variance Trade-off and Cross-Validation", [
    ("Bias–variance trade-off; leave-one-out and k-fold cross-validation [DA]", "Syllabus-explicit; estimate-computation questions; Regularisation link to Ridge")],
    "2/3 DA years · 1 Q",
    ["Estimate LOO/k-fold errors", "Classify high-bias vs high-variance"],
    ["Conceptual flashcards"]),
T(2, "Multi-Layer Perceptron and Feed-Forward Neural Networks", [
    ("Multi-layer perceptron, feed-forward neural network, activations & backpropagation [DA]", "DA 2025: update-direction question; DA 2025: ∂y/∂a backprop; ReLU differentiability; DA 2026: parameter-count question; DA 2024 two-network comparison")],
    "3/3 DA years · 1–2 Qs",
    ["Count parameters exactly", "One backprop step by hand"],
    ["NN drill: 15 problems"]),
T(2, "Clustering — k-Means, k-Medoids, Hierarchical", [
    ("Clustering algorithms: k-means/k-medoids; hierarchical top-down/bottom-up, single-/multiple-linkage [DA]", "DA 2024: k=3 same-cluster question; DA 2024/2025 linkage traces; DA 2026 agglomerative with Manhattan; k-means trap question")],
    "3/3 DA years · 1–2 Qs",
    ["Trace one k-means iteration", "Merge clusters by linkage rule"],
    ["Clustering drill: 12 traces"]),
T(2, "Principal Component Analysis", [
    ("Dimensionality reduction and PCA [DA] (Applies Engg Math Ch 6 Eigen Value 6.3 & SVD 6.9)", "DA 2025: eigenvalues λᵢ=100^(2−i); DA 2026: PCA-for-classification question; DA 2024: between/within-class scatter; Recurring conceptual trap")],
    "3/3 DA years · 1–2 Qs — ask every year",
    ["Eigenvectors of 2×2 covariance by hand", "Explain what PCA maximises"],
    ["PCA drill — never skip, it appears every year"]),
]})

# 14 ----------------------------------------------------------------- AI
G.append({"name": "14. Artificial Intelligence", "note": "Data Science paper (~6–11 marks, smallest section — efficient study wins here) · DA Core Syllabus",
"rows": [
T(3, "Uninformed Search (BFS, DFS)", [
    ("Uninformed search: BFS, DFS, UCS, IDS [DA] (Extends Core CS Ch 1: 1.8 DFS, 1.9 Dijkstra, 1.14 Graph Search)", "Completeness/optimality MCQs; DA 2024: successor counting; DA 2025: discovery-count question")],
    "3/3 DA years · 1 Q",
    ["Count nodes expanded", "Compare time/space/optimality of BFS, DFS, UCS, IDS"],
    ["Fold into graph search drill"]),
T(3, "Informed Search — A* and Heuristics", [
    ("A-star & Greedy Best-First; admissible and consistent heuristics [DA]", "DA 2024: admissibility of h1+h2, max, min; DA 2025: expansion-sequence question")],
    "3/3 DA years · 1 Q",
    ["Check admissibility & consistency against h*", "Trace expansions with f=g+h"],
    ["A* drill: 10 traces — always asked"]),
T(3, "Adversarial Search — Minimax", [
    ("Adversarial search: Minimax & Alpha-Beta pruning [DA]", "DA 2026: game-tree value question; DA 2024/2025: pruning ranges")],
    "3/3 DA years · 1 Q",
    ["Evaluate game trees", "Mark alpha-beta pruned branches correctly"],
    ["Minimax/Alpha-Beta drill: 8 game-tree traces"]),
T(3, "Propositional Logic and Predicate Logic (AI section)", [
    ("Propositional and predicate logic [Both] · Book Ch 3: 3.1 First Order Logic (34), 3.2 Logical Reasoning (3), 3.3 Propositional Logic (40)", "DA 2026: two FOL validity questions; DA 2025: equivalence question; DA 2024: game/shape predicates; Shared with CSE discrete maths (77 book PYQs)")],
    "3/3 DA years · 1–2 Qs · Book Ch 3 (77 Qs)",
    ["Same skill as CS logic topic"],
    ["Shared with group 1 drill — no separate study"]),
T(3, "Reasoning under Uncertainty — Conditional Independence, Variable Elimination, Sampling", [
    ("Conditional-independence representation; Bayesian Networks; exact inference through variable elimination; approximate inference through sampling [DA] · Book Ch 7: 7.1 Bayes Theorem (1), 7.2 Bayesian Network (2), 7.5 Conditional Probability (14)", "DA 2024: P(U,V,W,X,Y) factorisation; DA 2024: CPT inference question; DA 2025: exact-inference question; DA 2025: approximate-inference comparison")],
    "2/3 DA years · 1 Q · Book Ch 7 (7.1, 7.2, 7.5)",
    ["Read factorisations off the graph", "One VE elimination by hand"],
    ["Make a Bayes-net worked-example card"]),
]})

# 15 ----------------------------------------------------------------- GA
G.append({"name": "15. General Aptitude", "note": "Common to both papers — fixed 15 marks · GATE GA Book Ch 8–11 (1058 Qs) + Practice Aptitude Book Ch 1–8 (5264 Qs)",
"rows": [
T(1, "Verbal Ability — Grammar, Vocabulary, Reading Comprehension", [
    ("Grammar: tenses, articles, prepositions, agreement [Both] · GATE GA Ch 11: 11.1 Articles (2), 11.2 Comparative Forms (7), 11.3 English Grammar (12), 11.4 Grammatical Error (9), 11.5 Incorrect Sentence Part (5), 11.8 Noun Verb Adjective (3), 11.13 Prepositions (8), 11.14 Pronouns (4), 11.19 Tenses (25) | Practice Book Ch 5: 5.3 Error Spotting (16), 5.6 Imperative Sentences (1), 5.7 Indirect Speech (2), 5.17 Passive Voice (2), 5.19 Sentence Correction (6)", "Error-spotting & grammar questions; 102 book Qs"),
    ("Vocabulary, synonyms, opposites, word pairs and idioms in context [Both] · GATE GA Ch 11: 11.6 Most Appropriate Word (113), 11.9 Opposite (5), 11.11 Phrasal Verb (2), 11.12 Phrase Meaning (8), 11.18 Synonyms (19), 11.21 Word Meaning (17), 11.22 Word Pairs (30) | Practice Book Ch 5: 5.1 Appropriate Word (89), 5.4 Fill The Blank (42), 5.5 Idioms (2), 5.8 Jumbled Word (1), 5.14 Opposite Word (6), 5.23 Two Blank Word (3), 5.24 Word Meaning (4), 5.25 Word Pairs (46)", "Word-meaning & cloze questions; 387 book Qs"),
    ("Reading comprehension, narrative sequencing & verbal reasoning [Both] · GATE GA Ch 11: 11.7 Narrative Sequencing (1), 11.10 Passage Reading (57), 11.15 Sentence Ordering (5), 11.16 Statement Sufficiency (2), 11.17 Statements Follow (2), 11.20 Verbal Reasoning (40) | Practice Book Ch 5: 5.2 English Language (321), 5.9 Most Appropriate Alternative (32), 5.10 Most Appropriate Option (21), 5.11 Most Appropriate Replacement (6), 5.12 Most Appropriate Sentence (5), 5.13 Most Appropriate Words (2), 5.15 Paragraph Construction (28), 5.16 Passage Reading (641), 5.18 Sentence Completion (10), 5.20 Sentence Formation (37), 5.21 Sentence Rearrangement (117), 5.22 Statements Conclusions (8)", "Short-passage & ordering questions every year")],
    "Every year · 4–6 marks · GATE GA Ch 11 (376 Qs) + Practice Ch 5 (1560 Qs)",
    ["Error spotting", "Cloze/vocab in context", "Passage inference"],
    ["30-min GA block alternate days — no separate theory phase"]),
T(1, "Numerical Ability — Quantitative Aptitude and Data Interpretation", [
    ("Ratios, percentages, averages, mixtures, profit/loss, interest, speed/time/work, clocks/calendars [Both] · GATE GA Ch 9: 9.4 Alligation Mixture (3), 9.7 Average (3), 9.9 Calendar (2), 9.12 Clock Time (10), 9.14 Compound Interest (5), 9.18 Cost Market Price (6), 9.21 Currency Notes (1), 9.43 Percentage (21), 9.51 Profit Loss (6), 9.54 Ratio Proportion (26), 9.59 Speed Time Distance (19), 9.70 Work Time (17) | Practice Book Ch 7: 7.3 Ages (13), 7.5 Alligation Mixture (25), 7.10 Average (27), 7.13 Boat Stream (7), 7.15 Calendar (2), 7.19 Clock Time (1), 7.20 Clocks (8), 7.23 Compound Interest (4), 7.24 Cost Price Selling Price (6), 7.31 Discount (4), 7.36 Fare Journey (1), 7.46 Income Expenditure (1), 7.49 Interests Payments (1), 7.53 Market Price (1), 7.55 Mean (2), 7.56 Median (1), 7.58 Milk Water (1), 7.59 Mixtures (4), 7.64 Percentage (60), 7.68 Pipes Cistern (13), 7.71 Profit Loss (48), 7.75 Ratio Proportion (61), 7.81 Safe (1), 7.85 Simple Compound Interest (11), 7.86 Simple Interest (6), 7.88 Speed Distance Time (82), 7.97 Time And Distance (24), 7.98 Train (6), 7.103 Work Cost (9), 7.104 Work Time (49)", "Bulk of quant marks"),
    ("Number systems, algebra, functions, logarithms, progressions, permutations/combinations, probability & stats [Both] · GATE GA Ch 9: 9.1 Absolute Value (7), 9.2 Activation Functions (1), 9.3 Algebra (6), 9.6 Arithmetic Series (9), 9.13 Combinatory (12), 9.15 Conditional Probability (6), 9.19 Counting (6), 9.25 Factors (4), 9.26 Fractions (4), 9.27 Functions (18), 9.29 Graph Coloring (3), 9.30 Inequality (4), 9.31 LCM HCF (1), 9.34 Logarithms (14), 9.36 Maxima Minima (4), 9.38 Modular Arithmetic (2), 9.39 Number Series (10), 9.40 Number System (7), 9.41 Number Theory (6), 9.42 Numerical Computation (14), 9.44 Permutation and Combination (4), 9.46 Polynomials (4), 9.47 Powers (1), 9.48 Prime Numbers (1), 9.49 Probability (29), 9.50 PDF (1), 9.52 Quadratic Equations (11), 9.56 Seating Arrangement (2), 9.57 Sequence Series (10), 9.58 Set Theory (1), 9.61 Statistics (9), 9.62 System of Equations (1), 9.67 Unit Digit (2), 9.68 Venn Diagram (16) | Practice Book Ch 7: 7.1 3d (1), 7.2 Absolute Value (14), 7.4 Algebra (73), 7.7 AGP (1), 7.8 AM (4), 7.9 AP (15), 7.12 Binomial Theorem (1), 7.14 Bodmas (1), 7.22 Combinatory (5), 7.26 Cubic Equations (3), 7.29 Dice (2), 7.30 Digits (2), 7.32 Divisibility (7), 7.33 Equations (11), 7.34 Factorials (5), 7.35 Factors (6), 7.37 Fractions (8), 7.38 Functions (48), 7.39 Fundamental Operations (3), 7.40 GM (2), 7.41 GP (3), 7.45 Inclusion Exclusion (2), 7.47 Inequalities (18), 7.48 Infinite GP (4), 7.50 Lcm Hcf (13), 7.52 Logarithms (34), 7.54 Maxima Minima (5), 7.60 Number Of Zeroes (1), 7.61 Number System (4), 7.62 Number Systems (131), 7.63 Numbers (89), 7.65 Permutation And Combination (18), 7.66 Permutations And Combinations (38), 7.69 Polynomials (6), 7.70 Probability (10), 7.72 Progression (1), 7.73 Quadratic Equations (34), 7.74 Quantitative Aptitude (50), 7.76 Rational Numbers (1), 7.78 Recurrence Relation (1), 7.79 Remainder (2), 7.80 Remainder Theorem (5), 7.82 Sequences & Series (89), 7.83 Sets (7), 7.89 Square Root (5), 7.90 Statistics (1), 7.92 Summation (1), 7.93 System Of Equations (9), 7.94 System Of Linear Equations (1), 7.96 Roots (1), 7.101 Unit Digit (7), 7.102 Venn Diagrams (9)", "Feeds from maths prep"),
    ("Data interpretation: bar graphs, line graphs, pie charts, radar, scatter, contour & tables [Both] · GATE GA Ch 9: 9.8 Bar Graph (18), 9.17 Contour Plots (4), 9.23 Data Interpretation (5), 9.32 Line Graph (12), 9.35 Maps (1), 9.45 Pie Chart (16), 9.53 Radar Chart (1), 9.55 Scatter Plot (1), 9.63 Tables (1), 9.64 Tabular Data (10) | Practice Book Ch 1 (323 Qs): 1.1 Bar Graph (79), 1.2 Data Interpretation (17), 1.3 Graphical Data (4), 1.4 Line Graph (36), 1.5 Pie Chart (12), 1.6 Radar Web Graph (7), 1.7 Tabular Data (168) & Ch 7 (7.11 Bar Graph (6), 7.28 Data Interpretation (2), 7.43 Graph (2), 7.51 Line Graph (1), 7.67 Pie Chart (7), 7.95 Tabular Data (2))", "Every year 2–3 questions"),
    ("Mensuration, geometry, coordinates & trigonometry [Both] · GATE GA Ch 9: 9.5 Area (2), 9.10 Cartesian Coordinates (10), 9.11 Circle (7), 9.16 Cones (1), 9.20 Cube (2), 9.22 Curves (2), 9.28 Geometry (29), 9.33 Lines (1), 9.37 Mensuration (1), 9.60 Squares (4), 9.65 Triangles (11), 9.66 Trigonometry (1), 9.69 Volume (2) | Practice Book Ch 7: 7.6 Area (4), 7.16 Cartesian Coordinates (10), 7.17 Circle (1), 7.18 Circles (3), 7.21 Collinear (1), 7.25 Cubes (2), 7.27 Curves (2), 7.42 Geometry (174), 7.44 Height Distance (8), 7.57 Mensuration (23), 7.77 Rectangle (1), 7.84 Shadow (1), 7.87 Solids (1), 7.91 Straight Lines (3), 7.99 Triangle (9), 7.100 Trigonometry (7)", "Occasional 1–2 marks")],
    "Every year · 5–7 marks · GATE GA Ch 9 (494 Qs) + Practice Ch 1 (323 Qs) & Ch 7 (1760 Qs)",
    ["Speed arithmetic", "DI extraction accuracy", "Geometry & coordinate shortcuts"],
    ["Daily 15-question GA set"]),
T(1, "Logical Reasoning and Analytical Ability", [
    ("Deduction/induction, syllogisms, statements & conclusions, seating/round-table arrangements [Both] · GATE GA Ch 8: 8.8 Logical Inference (1), 8.9 Logical Reasoning (39), 8.12 Passage Reading (6), 8.13 Round Table Arrangement (6), 8.14 Seating Arrangement (4), 8.16 Statements Follow (33) | Practice Book Ch 2 (1101 Qs): 2.10 Data Sufficiency (10), 2.11 Decision Making (10), 2.13 Fact Judgement Inference (10), 2.18 Logic Puzzles (508), 2.19 Logical Reasoning (149), 2.26 Order And Sequence (2), 2.27 Passage Reading (33), 2.28 Preference List (1), 2.29 Puzzle (1), 2.31 Round Table Arrangement (7), 2.32 Seating Arrangement (16), 2.36 Some All None (13), 2.37 Statement Follows (12), 2.38 Statement Sufficiency (23), 2.39 Statements Conclusions (16), 2.40 Syllogism (13)", "Constraint-satisfaction style puzzles"),
    ("Blood/family relations, direction sense, coding-decoding, series & odd-one-out [Both] · GATE GA Ch 8: 8.1 Age Relation (2), 8.2 Code Words (5), 8.3 Coding Decoding (1), 8.5 Direction Sense (12), 8.6 Family Relationship (7), 8.7 Inequality (1), 8.10 Number Relations (3), 8.11 Odd One (6), 8.15 Sequence Series (12) | Practice Book Ch 2: 2.1 Age Relation (1), 2.2 Alphanumeric Series (11), 2.3 Arithmetic Series (1), 2.4 Blood Relation (13), 2.5 Calendar (5), 2.6 Clocks (1), 2.7 Code Language (15), 2.8 Codes (5), 2.12 Direction Sense (3), 2.14 Family Relationships (1), 2.15 Finding The Missing Figure (1), 2.16 Follow Instruction (1), 2.17 Forming Word (1), 2.20 Match The Following (3), 2.21 Mathematical Operations (2), 2.22 Mirror Image (3), 2.23 Number Series (18), 2.24 Odd Man Out (1), 2.25 Odd One Out (21), 2.30 Relationship (1), 2.33 Sequence And Series (2), 2.34 Sequence Of Words (7), 2.35 Sequences & Series (45), 2.41 Verification Of Truth (1), 2.42 Word Formation (1)", "Quick marks"),
    ("Spatial aptitude & Practice Book Bonus Sections [Both] · GATE GA Ch 10 (49 Qs): 10.1 Assembling Pieces (4), 10.2 Counting Figure (1), 10.3 Grouping (1), 10.4 Image Rotation (7), 10.5 Mirror Image (7), 10.6 Paper Folding (12), 10.7 Patterns In 3D (8), 10.8 Patterns In 2D (9) + Ch 8: 8.4 Counting Figure (1) + Ch 9: 9.24 Digital Image Processing (1) | Practice Book Ch 8 (8 Qs): 8.1 Direction Sense (3), 8.2 Figure Folding (1), 8.3 Sequences & Series (1), 8.4 Spatial Aptitude (3) & Ch 2: 2.9 Counting Figure (3) | Practice Book Bonus Ch 3 Attitude & Leadership (3.1 Assertive (1), 3.2 Assertion (1), 3.3 Judgement (2), 3.4 Leadership (1)), Ch 4 Computer Knowledge (4.1–4.21, 300 Qs), Ch 6 General Awareness (6.1–6.23, 207 Qs)", "Spatial & paper-folding questions + bonus speed drills")],
    "Every year · 4–5 marks · GATE GA Ch 8 (139 Qs) & Ch 10 (49 Qs) + Practice Ch 2 (1101 Qs), Ch 8 (8 Qs) & Bonus Ch 3/4/6",
    ["Constraint grids", "Visual rotation", "Syllogism Venn diagrams"],
    ["Alternate-day GA block"]),
]})

data = {"groups": G,
        "meta": {"disclaimer": "Includes exact PYQ book chapters, section numbers & question counts across Core CS, Engineering/Discrete Math, and General Aptitude + all DA syllabus topics.",
                 "solveCSE": "CSE: Core CS Book Ch 1–10 (2,592 Qs) + Math/GA Book Ch 1–11 (1,711 Qs)",
                 "solveDA": "DA: Shared Math/Programming/DS/Algo/DBMS book chapters + DA 2024–2026 papers & ML/AI/Warehousing extensions"}}

out = __import__("pathlib").Path(__file__).resolve().parent / "checklist_data.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
print("wrote", out.name + ":", sum(len(g["rows"]) for g in G), "topics,",
      sum(len(r["subs"]) for g in G for r in g["rows"]), "subtopics")
