# -*- coding: utf-8 -*-
"""Master script to update the GATE 2027 CSE+DA plan and tracker with all exact PYQ book topics and question counts.

Enforces all user rules:
1. Keep the plan up to 23rd October (`2026-10-06` through `2026-10-23`) completely untouched.
2. Do NOT clear or break any completed progress/checkbox keys (`localStorage` keys for days, topics, checklist, pyq, etc.).
3. Update all daily study sessions from `2026-10-24` onward with the exact PYQ book topics (section numbers, names, and question counts)
   from the Core CS book (Ch 1–10), Engineering/Discrete Math & GATE GA book (Ch 1–11), and Practice Aptitude book (Ch 1, 2, 5, 7, 8).
4. Include all DA syllabus topics and DA extensions alongside CS topics, tagged properly so each item displays `CS`, `DA`, or `Both`.
5. Rebuild `daily_resequenced.json`, `workbook_plan.json`, `checklist_data.json`, and `site/index.html` cleanly without needing external markdown packages.
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(r"e:\Unreg\GATE")
PREP = ROOT / "gate-prep-plan"
SITE = PREP / "site"

# Import our rich definitions
# -*- coding: utf-8 -*-
"""Update the GATE 2027 CSE+DA plan and tracker with all exact PYQ book topics and question counts.

Requirements fulfilled:
1. Keep all days up to and including 2026-10-23 (till 23rd October) completely untouched.
2. Keep all completed progress/checkbox keys untouched so no existing progress is cleared.
3. Update all daily study sessions from 2026-10-24 onward with the exact PYQ book topics (section numbers, names, and question counts)
   from the Core CS book, Engineering/Discrete Mathematics & GATE General Aptitude book, and Comprehensive Aptitude book.
4. Include all DA syllabus topics and DA extensions alongside CS topics, tagged properly so each item displays CS, DA, or Both.
5. Update Master Checklist (checklist_data.json) and rebuild index.html with the unified daily card UI.
"""
import json
import re
from pathlib import Path

ROOT = Path(r"e:\Unreg\GATE")
PREP = ROOT / "gate-prep-plan"
SITE = PREP / "site"

# ---------------------------------------------------------------------------
# 1. General Aptitude + Math Recall Schedule for Daily Blocks (from 2026-10-24 onward)
#    Every topic from the Engineering Math & GATE GA book (Ch 1-11) + Aptitude book
#    is scheduled systematically across the daily GA and Math Recall blocks.
# ---------------------------------------------------------------------------

GA_ROTATION = [
    "GA Verbal (Ch 11): 11.1 Articles (2), 11.3 English Grammar (12), 11.4 Grammatical Error (9), 11.5 Incorrect Sentence Part (5) | Practice Book Ch 5: 5.3 Error Spotting (16), 5.6 Imperative Sentences (1), 5.7 Indirect Speech (2), 5.17 Passive Voice (2), 5.19 Sentence Correction (6)",
    "GA Verbal (Ch 11): 11.13 Prepositions (8), 11.14 Pronouns (4), 11.19 Tenses (25), 11.8 Noun Verb Adjective (3), 11.2 Comparative Forms (7)",
    "GA Verbal (Ch 11): 11.6 Most Appropriate Word (113), 11.11 Phrasal Verb (2), 11.12 Phrase Meaning (8) | Practice Book Ch 5: 5.1 Appropriate Word (89), 5.4 Fill The Blank (42), 5.5 Idioms (2), 5.8 Jumbled Word (1)",
    "GA Verbal (Ch 11): 11.18 Synonyms (19), 11.9 Opposite (5), 11.21 Word Meaning (17), 11.22 Word Pairs (30) | Practice Book Ch 5: 5.14 Opposite Word (6), 5.23 Two Blank Word (3), 5.24 Word Meaning (4), 5.25 Word Pairs (46)",
    "GA Verbal (Ch 11): 11.7 Narrative Sequencing (1), 11.15 Sentence Ordering (5), 11.20 Verbal Reasoning (40) | Practice Book Ch 5: 5.15 Paragraph Construction (28), 5.18 Sentence Completion (10), 5.20 Sentence Formation (37), 5.21 Sentence Rearrangement (117), 5.22 Statements Conclusions (8)",
    "GA Verbal (Ch 11): 11.10 Passage Reading (57), 11.16 Statement Sufficiency (2), 11.17 Statements Follow (2) | Practice Book Ch 5: 5.2 English Language (321), 5.9 Most Appropriate Alternative (32), 5.10 Most Appropriate Option (21), 5.11 Most Appropriate Replacement (6), 5.12 Most Appropriate Sentence (5), 5.13 Most Appropriate Words (2), 5.16 Passage Reading (641)",
    "GA Analytical (Ch 8): 8.1 Age Relation (2), 8.5 Direction Sense (12), 8.6 Family Relationship (7), 8.7 Inequality (1) | Practice Book Ch 2: 2.1 Age Relation (1), 2.4 Blood Relation (13), 2.5 Calendar (5), 2.6 Clocks (1), 2.12 Direction Sense (3), 2.14 Family Relationships (1), 2.15 Finding The Missing Figure (1), 2.16 Follow Instruction (1), 2.17 Forming Word (1), 2.30 Relationship (1)",
    "GA Analytical (Ch 8): 8.2 Code Words (5), 8.3 Coding Decoding (1), 8.10 Number Relations (3), 8.11 Odd One (6), 8.15 Sequence Series (12) | Practice Book Ch 2: 2.2 Alphanumeric Series (11), 2.3 Arithmetic Series (1), 2.7 Code Language (15), 2.8 Codes (5), 2.20 Match The Following (3), 2.21 Mathematical Operations (2), 2.22 Mirror Image (3), 2.23 Number Series (18), 2.24 Odd Man Out (1), 2.25 Odd One Out (21), 2.33 Sequence And Series (2), 2.34 Sequence Of Words (7), 2.35 Sequences & Series (45), 2.41 Verification Of Truth (1), 2.42 Word Formation (1)",
    "GA Analytical (Ch 8): 8.13 Round Table Arrangement (6), 8.14 Seating Arrangement (4), 9.29 Graph Coloring (3), 9.56 Seating Arrangement (2) | Practice Book Ch 2: 2.18 Logic Puzzles (508), 2.26 Order And Sequence (2), 2.27 Passage Reading (33), 2.28 Preference List (1), 2.29 Puzzle (1), 2.31 Round Table Arrangement (7), 2.32 Seating Arrangement (16)",
    "GA Analytical (Ch 8): 8.8 Logical Inference (1), 8.9 Logical Reasoning (39), 8.12 Passage Reading (6), 8.16 Statements Follow (33) | Practice Book Ch 2: 2.10 Data Sufficiency (10), 2.11 Decision Making (10), 2.13 Fact Judgement Inference (10), 2.19 Logical Reasoning (149), 2.36 Some All None (13), 2.37 Statement Follows (12), 2.38 Statement Sufficiency (23), 2.39 Statements Conclusions (16), 2.40 Syllogism (13)",
    "GA Quantitative (Ch 9): 9.25 Factors (4), 9.26 Fractions (4), 9.31 LCM HCF (1), 9.38 Modular Arithmetic (2), 9.40 Number System (7), 9.41 Number Theory (6), 9.48 Prime Numbers (1), 9.67 Unit Digit (2) | Practice Book Ch 7: 7.14 Bodmas (1), 7.30 Digits (2), 7.32 Divisibility (7), 7.34 Factorials (5), 7.35 Factors (6), 7.37 Fractions (8), 7.39 Fundamental Operations (3), 7.50 Lcm Hcf (13), 7.60 Number Of Zeroes (1), 7.61 Number System (4), 7.62 Number Systems (131), 7.63 Numbers (89), 7.74 Quantitative Aptitude (50), 7.76 Rational Numbers (1), 7.79 Remainder (2), 7.80 Remainder Theorem (5), 7.89 Square Root (5), 7.101 Unit Digit (7)",
    "GA Quantitative (Ch 9): 9.4 Alligation Mixture (3), 9.7 Average (3), 9.43 Percentage (21), 9.54 Ratio Proportion (26) | Practice Book Ch 7: 7.3 Ages (13), 7.5 Alligation Mixture (25), 7.10 Average (27), 7.55 Mean (2), 7.56 Median (1), 7.58 Milk Water (1), 7.59 Mixtures (4), 7.64 Percentage (60), 7.75 Ratio Proportion (61), 7.81 Safe (1)",
    "GA Quantitative (Ch 9): 9.14 Compound Interest (5), 9.18 Cost Market Price (6), 9.21 Currency Notes (1), 9.51 Profit Loss (6) | Practice Book Ch 7: 7.23 Compound Interest (4), 7.24 Cost Price Selling Price (6), 7.31 Discount (4), 7.46 Income Expenditure (1), 7.49 Interests Payments (1), 7.53 Market Price (1), 7.71 Profit Loss (48), 7.85 Simple Compound Interest (11), 7.86 Simple Interest (6)",
    "GA Quantitative (Ch 9): 9.9 Calendar (2), 9.12 Clock Time (10), 9.59 Speed Time Distance (19), 9.70 Work Time (17) | Practice Book Ch 7: 7.13 Boat Stream (7), 7.15 Calendar (2), 7.19 Clock Time (1), 7.20 Clocks (8), 7.36 Fare Journey (1), 7.68 Pipes Cistern (13), 7.88 Speed Distance Time (82), 7.97 Time And Distance (24), 7.98 Train (6), 7.103 Work Cost (9), 7.104 Work Time (49)",
    "GA Quantitative (Ch 9): 9.1 Absolute Value (7), 9.2 Activation Functions (1), 9.3 Algebra (6), 9.27 Functions (18), 9.30 Inequality (4), 9.34 Logarithms (14), 9.46 Polynomials (4), 9.47 Powers (1), 9.52 Quadratic Equations (11), 9.62 System of Equations (1) | Practice Book Ch 7: 7.1 3d (1), 7.2 Absolute Value (14), 7.4 Algebra (73), 7.26 Cubic Equations (3), 7.33 Equations (11), 7.38 Functions (48), 7.47 Inequalities (18), 7.52 Logarithms (34), 7.69 Polynomials (6), 7.73 Quadratic Equations (34), 7.93 System Of Equations (9), 7.94 System Of Linear Equations (1), 7.96 Roots (1)",
    "GA Quantitative (Ch 9): 9.6 Arithmetic Series (9), 9.36 Maxima Minima (4), 9.39 Number Series (10), 9.42 Numerical Computation (14), 9.57 Sequence Series (10) | Practice Book Ch 7: 7.7 AGP (1), 7.8 AM (4), 7.9 AP (15), 7.12 Binomial Theorem (1), 7.40 GM (2), 7.41 GP (3), 7.48 Infinite GP (4), 7.54 Maxima Minima (5), 7.72 Progression (1), 7.78 Recurrence Relation (1), 7.82 Sequences & Series (89), 7.92 Summation (1)",
    "GA Quantitative (Ch 9): 9.13 Combinatory (12), 9.15 Conditional Probability (6), 9.19 Counting (6), 9.44 Permutation and Combination (4), 9.49 Probability (29), 9.50 PDF (1), 9.58 Set Theory (1), 9.61 Statistics (9), 9.68 Venn Diagram (16) | Practice Book Ch 7: 7.22 Combinatory (5), 7.29 Dice (2), 7.45 Inclusion Exclusion (2), 7.65 Permutation And Combination (18), 7.66 Permutations And Combinations (38), 7.70 Probability (10), 7.83 Sets (7), 7.90 Statistics (1), 7.102 Venn Diagrams (9)",
    "GA Quantitative (Ch 9): 9.5 Area (2), 9.10 Cartesian Coordinates (10), 9.11 Circle (7), 9.16 Cones (1), 9.20 Cube (2), 9.22 Curves (2), 9.28 Geometry (29), 9.33 Lines (1), 9.37 Mensuration (1), 9.60 Squares (4), 9.65 Triangles (11), 9.66 Trigonometry (1), 9.69 Volume (2) | Practice Book Ch 7: 7.6 Area (4), 7.16 Cartesian Coordinates (10), 7.17 Circle (1), 7.18 Circles (3), 7.21 Collinear (1), 7.25 Cubes (2), 7.27 Curves (2), 7.42 Geometry (174), 7.44 Height Distance (8), 7.57 Mensuration (23), 7.77 Rectangle (1), 7.84 Shadow (1), 7.87 Solids (1), 7.91 Straight Lines (3), 7.99 Triangle (9), 7.100 Trigonometry (7)",
    "GA Data Interpretation (Ch 9 & Practice Book Ch 1 & Ch 7): 9.8 Bar Graph (18), 9.17 Contour Plots (4), 9.23 Data Interpretation (5), 9.32 Line Graph (12), 9.35 Maps (1), 9.45 Pie Chart (16), 9.53 Radar Chart (1), 9.55 Scatter Plot (1), 9.63 Tables (1), 9.64 Tabular Data (10) | Practice Book Ch 1 (323 Qs): 1.1 Bar Graph (79), 1.2 Data Interpretation (17), 1.3 Graphical Data (4), 1.4 Line Graph (36), 1.5 Pie Chart (12), 1.6 Radar Web Graph (7), 1.7 Tabular Data (168) & Ch 7 DI: 7.11 Bar Graph (6), 7.28 Data Interpretation (2), 7.43 Graph (2), 7.51 Line Graph (1), 7.67 Pie Chart (7), 7.95 Tabular Data (2)",
    "GA Spatial Aptitude (Ch 10 & Practice Book Ch 8) + Practice Book Bonus (Ch 3, 4, 6): 10.1 Assembling Pieces (4), 10.2 Counting Figure (1), 10.3 Grouping (1), 10.4 Image Rotation (7), 10.5 Mirror Image (7), 10.6 Paper Folding (12), 10.7 Patterns In 3D (8), 10.8 Patterns In 2D (9), 8.4 Counting Figure (1), 9.24 Digital Image Processing (1) | Practice Book Ch 8 (8 Qs): 8.1 Direction Sense (3), 8.2 Figure Folding (1), 8.3 Sequences & Series (1), 8.4 Spatial Aptitude (3) & Ch 2: 2.9 Counting Figure (3) | Practice Book Bonus Ch 3 Attitude & Leadership (5 Qs: 3.1 Assertive (1), 3.2 Assertion (1), 3.3 Judgement (2), 3.4 Leadership (1)), Ch 4 Computer Knowledge (300 Qs: 4.1 Algos (12), 4.2 CO (29), 4.3 CN (32), 4.4 DS (28), 4.5 DBMS (24), 4.6 Digital (30), 4.7 Hacking (1), 4.8 Info Sys (4), 4.9 Hardware (4), 4.10 Internet (15), 4.11 Memory (10), 4.12 MS Office (24), 4.13 Number Sys (12), 4.14 OS (34), 4.15 Prog (25), 4.16 SW Eng (6), 4.17 SW Testing (1), 4.18 Sys SW (3), 4.19 Security (2), 4.20 UNIX (3), 4.21 Web (1)), Ch 6 General Awareness (207 Qs: 6.1 Abbreviations (2), 6.2 Agriculture (2), 6.3 Art & Literature (3), 6.4 Awards (7), 6.5 Banking (3), 6.6 Books & Authors (10), 6.7 Committees (1), 6.8 Constitution (7), 6.9 Culture (1), 6.10 Days & Years (4), 6.11 Economy (14), 6.12 Finance (1), 6.13 Current Affairs (11), 6.14 Geography (17), 6.15 History (14), 6.16 Governance (6), 6.17 Int Org (11), 6.18Polity (8), 6.19 Personalities (6), 6.20 Politics (2), 6.21 Science (67), 6.22 Social Issues (2), 6.23 Sports (8))",
]

MATH_RECALL_ROTATION = [
    "Math Recall — Discrete Math Ch 3 Mathematical Logic (77 Qs): 3.1 First Order Logic (34), 3.2 Logical Reasoning (3), 3.3 Propositional Logic (40) [Both CS & DA]",
    "Math Recall — Discrete Math Ch 4 Set Theory & Algebra (171 Qs): 4.2 Countable Uncountable Set (2), 4.3 Functions (29), 4.5 Identify Function (1), 4.9 Onto (1), 4.12 Relations (37), 4.13 Set Theory (27) [CS Only]",
    "Math Recall — Discrete Math Ch 4 Algebra & Posets (171 Qs): 4.1 Binary Operation (8), 4.4 Group Theory (33), 4.6 Lattice (10), 4.7 Mathematical Induction (2), 4.8 Number Theory (7), 4.10 Partial Order (10), 4.11 Polynomials (4) [CS Only]",
    "Math Recall — Discrete Math Ch 1 Combinatory (50 Qs): 1.1 Balls In Bins (4), 1.2 Combinatory (22), 1.3 Counting (4), 1.4 Generating Functions (6), 1.5 Modular Arithmetic (2), 1.6 Pigeonhole Principle (2), 1.7 Recurrence Relation (7), 1.8 Summation (3) [1.1-1.3, 1.6 Both; 1.4, 1.7 CS Only]",
    "Math Recall — Discrete Math Ch 2 Graph Theory (83 Qs): 2.1 Counting (3), 2.2 Degree of Graph (12), 2.3 Graph Coloring (11), 2.4 Graph Connectivity (40), 2.5 Graph Isomorphism (3), 2.6 Graph Matching (1), 2.7 Graph Planarity (13) [2.2, 2.4 Both; 2.3, 2.5-2.7 CS Only]",
    "Math Recall — Engg Math Ch 6 Linear Algebra Part 1 (102 Qs): 6.1 Cartesian Coordinates (1), 6.2 Determinant (11), 6.4 Gaussian Elimination (1), 6.5 LU Decomposition (1), 6.6 Matrix (22), 6.8 Rank of Matrix (6), 6.11 System of Equations (17) [Both CS & DA + DA Extra: Idempotent & Partition Matrices]",
    "Math Recall — Engg Math Ch 6 Linear Algebra Part 2 (102 Qs): 6.3 Eigen Value (33), 6.7 Orthonormality (2), 6.9 Singular Value Decomposition (1), 6.10 Subspace (1), 6.12 Vector Space (6) [Both CS & DA + DA Extra: Projections, Quadratic Forms & SVD]",
    "Math Recall — Engg Math Ch 5 Calculus (63 Qs): 5.1 Continuity (9), 5.2 Definite Integral (3), 5.3 Differentiation (10), 5.4 Integration (11), 5.5 Limits (15), 5.6 Maxima Minima (13), 5.7 Polynomials (2) [5.1, 5.3, 5.5, 5.6 Both; 5.2, 5.4 CS Only; DA Extra: Taylor Series & Single-Variable Optimization]",
    "Math Recall — Engg Math Ch 7 Probability Part 1 (107 Qs): 7.1 Bayes Theorem (1), 7.2 Bayesian Network (2), 7.5 Conditional Probability (14), 7.7 Expectation (13), 7.9 Independent Events (6), 7.12 Probability (28), 7.15 Random Variable (8), 7.19 Variance (1) [Both CS & DA + DA Extra: Conditional Expectation & Variance, Covariance & Correlation]",
    "Math Recall — Engg Math Ch 7 Probability & Stats Part 2 (107 Qs): 7.3 Bernoulli (1), 7.4 Binomial (6), 7.6 Continuous Dist (1), 7.8 Exponential (5), 7.10 Normal (2), 7.11 Poisson (4), 7.13 PDF (1), 7.14 Prob Dist (1), 7.16 Square Invariant (1), 7.17 Statistics (2), 7.18 Uniform Dist (10) [Both + DA Extra: Joint/Marginal/Conditional PDF, CLT, t-dist, Chi-square, Confidence Intervals, z/t/chi-square Hypothesis Tests]",
]

# ---------------------------------------------------------------------------
# 2. Daily Unit Topic Definitions (from 2026-10-24 onward)
#    Format of each entry in `cs_items` and `da_items`:
#    - Items present in BOTH `cs_items` and `da_items` (exact string match) get pill `Both`
#    - Items only in `cs_items` get pill `CS`
#    - Items only in `da_items` get pill `DA`
# ---------------------------------------------------------------------------

UNIT_UPDATES = {
    ("2026-10-24", "Unit 28"): {
        "cs": [
            "Ch 9 Programming in C: 9.3 Functions (1), 9.5 Identify Function (6), 9.13 Recursion (18) — revision & tracing from Session A",
            "Session focus: Part B (24 Oct): Python fundamentals & DA-style PYQs, plus C recursion/function tracing revision from Session A (Ch 9: 9.3, 9.5, 9.13).",
        ],
        "da": [
            "DA Python Programming: Python syntax, data types (int, float, bool, str), type conversion",
            "DA Python Programming: Control structures (if/elif/else, for/while loops, comprehensions)",
            "DA Python Programming: Functions, default/keyword arguments, closures, recursion tracing",
            "Session focus: Part B (24 Oct): Python fundamentals & DA-style PYQs, plus C recursion/function tracing revision from Session A (Ch 9: 9.3, 9.5, 9.13).",
        ],
    },
    ("2026-10-25", "Sunday review 1"): {
        "cs": [
            "Engg Math Ch 6 Linear Algebra (102 Qs): 6.1 Cartesian Coordinates (1), 6.2 Determinant (11), 6.3 Eigen Value (33), 6.4 Gaussian Elimination (1), 6.5 LU Decomposition (1), 6.6 Matrix (22), 6.7 Orthonormality (2), 6.8 Rank of Matrix (6), 6.9 SVD (1), 6.10 Subspace (1), 6.11 System of Equations (17), 6.12 Vector Space (6)",
            "Discrete Math Ch 3 Mathematical Logic (77 Qs): 3.1 First Order Logic (34), 3.2 Logical Reasoning (3), 3.3 Propositional Logic (40)",
            "Discrete Math Ch 2 Graph Theory (83 Qs): 2.1 Counting (3), 2.2 Degree of Graph (12), 2.3 Graph Coloring (11), 2.4 Graph Connectivity (40), 2.5 Graph Isomorphism (3), 2.6 Graph Matching (1), 2.7 Graph Planarity (13)",
            "Discrete Math Ch 1 Combinatory (50 Qs): 1.1 Balls In Bins (4), 1.2 Combinatory (22), 1.3 Counting (4), 1.4 Generating Functions (6), 1.5 Modular Arithmetic (2), 1.6 Pigeonhole Principle (2), 1.7 Recurrence Relation (7), 1.8 Summation (3)",
            "Discrete Math Ch 4 Set Theory & Algebra (171 Qs): 4.1 Binary Operation (8), 4.2 Countable Uncountable Set (2), 4.3 Functions (29), 4.4 Group Theory (33), 4.5 Identify Function (1), 4.6 Lattice (10), 4.7 Mathematical Induction (2), 4.8 Number Theory (7), 4.9 Onto (1), 4.10 Partial Order (10), 4.11 Polynomials (4), 4.12 Relations (37), 4.13 Set Theory (27)",
            "Session focus: Timed diagnostic set (~25 PYQs, 90 min) from Linear Algebra & Discrete Mathematics book chapters above. Any topic below 70% goes onto the January second-pass list.",
        ],
        "da": [
            "Engg Math Ch 6 Linear Algebra (102 Qs): 6.1 Cartesian Coordinates (1), 6.2 Determinant (11), 6.3 Eigen Value (33), 6.4 Gaussian Elimination (1), 6.5 LU Decomposition (1), 6.6 Matrix (22), 6.7 Orthonormality (2), 6.8 Rank of Matrix (6), 6.9 SVD (1), 6.10 Subspace (1), 6.11 System of Equations (17), 6.12 Vector Space (6)",
            "DA Linear Algebra Extensions: Projection, Orthogonal, Idempotent & Partition Matrices, Quadratic Forms, SVD applications",
            "Discrete Math Ch 3 Mathematical Logic (77 Qs): 3.1 First Order Logic (34), 3.2 Logical Reasoning (3), 3.3 Propositional Logic (40)",
            "Session focus: Timed diagnostic set (~25 PYQs, 90 min) from Linear Algebra & Discrete Mathematics book chapters above. Any topic below 70% goes onto the January second-pass list.",
        ],
    },
    ("2026-10-26", "Unit 29"): {
        "cs": [
            "Ch 9 Programming in C (127 Qs): 9.1 Aliasing (1), 9.2 Array (10), 9.4 Goto (2), 9.6 Loop Invariants (8)",
            "Ch 9 Programming in C: 9.7 Output (10), 9.8 Parameter Passing (12), 9.9 Pointers (14)",
            "Ch 9 Programming in C: 9.10 Programming Constructs (1), 9.11 Programming In C (31), 9.12 Programming Paradigms (2)",
            "Ch 9 Programming in C: 9.14 Strings (1), 9.15 Structure (5), 9.16 Switch Case (2), 9.17 Type Checking (1), 9.18 Union (1), 9.19 Variable Binding (1)",
            "Session focus: Complete all 127 C PYQs in Ch 9 (9.1–9.19) + Python lists/dicts/slicing output tracing for DA.",
        ],
        "da": [
            "DA Python Programming Extension: Lists, tuples, dictionaries, sets & mutability/aliasing traps",
            "DA Python Programming Extension: List/string slicing, shallow vs deep copy, mutable default arguments, output tracing",
            "Session focus: Complete all 127 C PYQs in Ch 9 (9.1–9.19) + Python lists/dicts/slicing output tracing for DA.",
        ],
    },
    ("2026-10-27", "Unit 30"): {
        "cs": [
            "Ch 8 Data Structures: 8.2 Array (13) — 1D & 2D row/column-major address calculation, sparse matrices",
            "Ch 8 Data Structures: 8.6 Data Structures (5), 8.8 Infix Prefix (5), 8.10 Number of Swap (1), 8.14 Time Complexity (1)",
            "Ch 8 Data Structures: 8.12 Queue (14) — linear queue, circular queue, deque operations",
            "Ch 8 Data Structures: 8.13 Stack (18) — expression evaluation, parenthesis matching, recursion stack",
            "Session focus: Practice Ch 8 sections 8.2, 8.6, 8.8, 8.10, 8.12, 8.13, 8.14 (57 Qs) + DA Python stack/queue/list implementations.",
        ],
        "da": [
            "Ch 8 Data Structures: 8.2 Array (13) — 1D & 2D row/column-major address calculation, sparse matrices",
            "Ch 8 Data Structures: 8.6 Data Structures (5), 8.8 Infix Prefix (5), 8.10 Number of Swap (1), 8.14 Time Complexity (1)",
            "Ch 8 Data Structures: 8.12 Queue (14) — linear queue, circular queue, deque operations",
            "Ch 8 Data Structures: 8.13 Stack (18) — expression evaluation, parenthesis matching, recursion stack",
            "DA Extension: Python list/collections.deque implementations of stacks and queues",
            "Session focus: Practice Ch 8 sections 8.2, 8.6, 8.8, 8.10, 8.12, 8.13, 8.14 (57 Qs) + DA Python stack/queue/list implementations.",
        ],
    },
    ("2026-10-28", "Unit 31"): {
        "cs": [
            "Ch 8 Data Structures: 8.9 Linked List (23) — singly, doubly, and circular linked lists",
            "Linked List Operations: insertion, deletion, reversal, cycle detection, pointer manipulation & time complexity",
            "Session focus: Solve all 23 PYQs in Ch 8 section 8.9 Linked List + trace pointer/reference manipulation in C and Python.",
        ],
        "da": [
            "Ch 8 Data Structures: 8.9 Linked List (23) — singly, doubly, and circular linked lists",
            "Linked List Operations: insertion, deletion, reversal, cycle detection, pointer manipulation & time complexity",
            "DA Extension: Linked list node & reference tracing in Python",
            "Session focus: Solve all 23 PYQs in Ch 8 section 8.9 Linked List + trace pointer/reference manipulation in C and Python.",
        ],
    },
    ("2026-10-29", "Unit 32"): {
        "cs": [
            "Ch 8 Data Structures: 8.5 Binary Tree (53), 8.15 Tree (14) — traversals (pre/in/post/level), height/leaf properties",
            "Ch 8 Data Structures: 8.4 Binary Search Tree (36) — search, insertion, deletion, traversal reconstruction",
            "Ch 8 Data Structures: 8.1 AVL Tree (6) — height balance, LL/RR/LR/RL rotations",
            "Ch 8 Data Structures: 8.3 Binary Heap (29), 8.11 Priority Queue (2) — min/max heap, O(n) build-heap, heapify, extract-min/max",
            "Session focus: Practice Ch 8 sections 8.1, 8.3, 8.4, 8.5, 8.11, 8.15 (140 Qs total across Trees, BST, AVL & Heaps).",
        ],
        "da": [
            "Ch 8 Data Structures: 8.5 Binary Tree (53), 8.15 Tree (14) — traversals (pre/in/post/level), height/leaf properties",
            "Ch 8 Data Structures: 8.4 Binary Search Tree (36) — search, insertion, deletion, traversal reconstruction",
            "Ch 8 Data Structures: 8.1 AVL Tree (6) — height balance, LL/RR/LR/RL rotations",
            "DA Extension: Tree & BST construction and traversal tracing in Python",
            "Session focus: Practice Ch 8 sections 8.1, 8.3, 8.4, 8.5, 8.11, 8.15 (140 Qs total across Trees, BST, AVL & Heaps).",
        ],
    },
    ("2026-10-30", "Unit 33"): {
        "cs": [
            "Ch 8 Data Structures: 8.7 Hashing (16) — hash functions, collision resolution, load factor",
            "Ch 1 Algorithms: 1.11 Double Hashing (1), 1.16 Hashing (7), 1.20 Linear Probing (1) — chaining & open addressing (linear, quadratic, double hashing)",
            "Session focus: Solve all 25 Hashing PYQs across Ch 8 (8.7) and Ch 1 (1.11, 1.16, 1.20) + probe sequence counting for CS & DA.",
        ],
        "da": [
            "Ch 8 Data Structures: 8.7 Hashing (16) — hash functions, collision resolution, load factor",
            "Ch 1 Algorithms: 1.11 Double Hashing (1), 1.16 Hashing (7), 1.20 Linear Probing (1) — chaining & open addressing (linear, quadratic, double hashing)",
            "DA Extension: Uniform hashing expected probes & Python dict/set hash table mechanics",
            "Session focus: Solve all 25 Hashing PYQs across Ch 8 (8.7) and Ch 1 (1.11, 1.16, 1.20) + probe sequence counting for CS & DA.",
        ],
    },
    ("2026-10-31", "Unit 34"): {
        "cs": [
            "Ch 1 Algorithms: 1.1 Algorithm Design (8), 1.2 Algorithm Design Technique (9)",
            "Ch 1 Algorithms: 1.3 Asymptotic Notation (7), 1.4 Asymptotic Notations (14) — Big-O, Omega, Theta, o, omega",
            "Ch 1 Algorithms: 1.18 Identify Function (38), 1.28 Recursion (4), 1.32 Space Complexity (1), 1.34 Time Complexity (29)",
            "Ch 1 Algorithms: 1.27 Recurrence Relation (35) — Master Theorem, recursion tree, substitution method",
            "Session focus: Practice Ch 1 sections 1.1–1.4, 1.18, 1.27, 1.28, 1.32, 1.34 (145 Qs across complexity, function ranking & recurrences).",
        ],
        "da": [
            "Ch 1 Algorithms: 1.1 Algorithm Design (8), 1.2 Algorithm Design Technique (9)",
            "Ch 1 Algorithms: 1.3 Asymptotic Notation (7), 1.4 Asymptotic Notations (14) — Big-O, Omega, Theta, o, omega",
            "Ch 1 Algorithms: 1.18 Identify Function (38), 1.28 Recursion (4), 1.32 Space Complexity (1), 1.34 Time Complexity (29)",
            "Session focus: Practice Ch 1 sections 1.1–1.4, 1.18, 1.27, 1.28, 1.32, 1.34 (145 Qs across complexity, function ranking & recurrences).",
        ],
    },
    ("2026-11-01", "Sunday review 2"): {
        "cs": [
            "Engg Math Ch 5 Calculus (63 Qs): 5.1 Continuity (9), 5.2 Definite Integral (3), 5.3 Differentiation (10), 5.4 Integration (11), 5.5 Limits (15), 5.6 Maxima Minima (13), 5.7 Polynomials (2)",
            "Engg Math Ch 7 Probability (107 Qs): 7.1 Bayes Theorem (1), 7.2 Bayesian Network (2), 7.3 Bernoulli Distribution (1), 7.4 Binomial Distribution (6), 7.5 Conditional Probability (14), 7.6 Continuous Distribution (1), 7.7 Expectation (13), 7.8 Exponential Distribution (5), 7.9 Independent Events (6), 7.10 Normal Distribution (2), 7.11 Poisson Distribution (4), 7.12 Probability (28), 7.13 PDF (1), 7.14 Probability Distribution (1), 7.15 Random Variable (8), 7.16 Square Invariant (1), 7.17 Statistics (2), 7.18 Uniform Distribution (10), 7.19 Variance (1)",
            "Session focus: Timed diagnostic set (~25 PYQs, 90 min) from Engg Math Ch 5 (Calculus) & Ch 7 (Probability & Statistics). Any topic below 70% goes onto the January second-pass list.",
        ],
        "da": [
            "Engg Math Ch 5 Calculus (63 Qs): 5.1 Continuity (9), 5.2 Definite Integral (3), 5.3 Differentiation (10), 5.4 Integration (11), 5.5 Limits (15), 5.6 Maxima Minima (13), 5.7 Polynomials (2)",
            "DA Calculus Extensions: Taylor & Maclaurin series, single-variable optimization & convexity",
            "Engg Math Ch 7 Probability (107 Qs): 7.1 Bayes Theorem (1), 7.2 Bayesian Network (2), 7.3 Bernoulli Distribution (1), 7.4 Binomial Distribution (6), 7.5 Conditional Probability (14), 7.6 Continuous Distribution (1), 7.7 Expectation (13), 7.8 Exponential Distribution (5), 7.9 Independent Events (6), 7.10 Normal Distribution (2), 7.11 Poisson Distribution (4), 7.12 Probability (28), 7.13 PDF (1), 7.14 Probability Distribution (1), 7.15 Random Variable (8), 7.16 Square Invariant (1), 7.17 Statistics (2), 7.18 Uniform Distribution (10), 7.19 Variance (1)",
            "DA Probability & Statistics Extensions: Joint/marginal/conditional distributions, covariance & correlation, conditional expectation/variance, CLT, Student's t, Chi-square, confidence intervals, z-test, t-test, chi-squared test",
            "Session focus: Timed diagnostic set (~25 PYQs, 90 min) from Engg Math Ch 5 (Calculus) & Ch 7 (Probability & Statistics). Any topic below 70% goes onto the January second-pass list.",
        ],
    },
    ("2026-11-02", "Unit 35"): {
        "cs": [
            "Ch 1 Algorithms: 1.6 Binary Search (3), 1.7 Bitonic Array (1), 1.29 Searching (7) — linear & binary search variants",
            "Ch 1 Algorithms: 1.19 Insertion Sort (3), 1.31 Sorting (28) — selection sort, bubble sort, insertion sort, stability & in-place analysis",
            "Session focus: Solve all 42 Searching & Sorting PYQs in Ch 1 (1.6, 1.7, 1.19, 1.29, 1.31) + DA swap/comparison counting variants.",
        ],
        "da": [
            "Ch 1 Algorithms: 1.6 Binary Search (3), 1.7 Bitonic Array (1), 1.29 Searching (7) — linear & binary search variants",
            "Ch 1 Algorithms: 1.19 Insertion Sort (3), 1.31 Sorting (28) — selection sort, bubble sort, insertion sort, stability & in-place analysis",
            "DA Extension: Exact swap & comparison counts in Insertion/Bubble/Selection sort and Binary Search on arrays vs linked lists",
            "Session focus: Solve all 42 Searching & Sorting PYQs in Ch 1 (1.6, 1.7, 1.19, 1.29, 1.31) + DA swap/comparison counting variants.",
        ],
    },
    ("2026-11-03", "Unit 36"): {
        "cs": [
            "Ch 1 Algorithms: 1.22 Merge Sort (3), 1.23 Merging (2) — 2-way/k-way merge, counting inversions",
            "Ch 1 Algorithms: 1.26 Quick Sort (14) — partition trace, pivot selection, best/worst/average case & in-place analysis",
            "Divide & Conquer Core: Min-max finding, recurrence-based D&C design (Ch 1: 1.1, 1.2, 1.27)",
            "Session focus: Solve all 19 Merge/Quick Sort PYQs in Ch 1 (1.22, 1.23, 1.26) + D&C recurrence & inversion counting problems.",
        ],
        "da": [
            "Ch 1 Algorithms: 1.22 Merge Sort (3), 1.23 Merging (2) — 2-way/k-way merge, counting inversions",
            "Ch 1 Algorithms: 1.26 Quick Sort (14) — partition trace, pivot selection, best/worst/average case & in-place analysis",
            "Session focus: Solve all 19 Merge/Quick Sort PYQs in Ch 1 (1.22, 1.23, 1.26) + D&C recurrence & inversion counting problems.",
        ],
    },
    ("2026-11-04", "Unit 37"): {
        "cs": [
            "Ch 1 Algorithms: 1.8 Depth First Search (1), 1.10 Directed Graph (1), 1.13 Graph Algorithms (11), 1.14 Graph Search (22) — BFS & DFS traversals, tree/back/forward/cross edges, cycle detection",
            "Ch 1 Algorithms: 1.33 Strongly Connected Components (3), 1.35 Topological Sort (4) — DAG ordering & SCCs",
            "Session focus: Part A: Solve Ch 1 sections 1.8, 1.10, 1.13, 1.14, 1.33, 1.35 (42 Qs on graph representations, BFS/DFS, topological sort & SCCs) + note direct link to DA AI Uninformed Search.",
        ],
        "da": [
            "Ch 1 Algorithms: 1.8 Depth First Search (1), 1.10 Directed Graph (1), 1.13 Graph Algorithms (11), 1.14 Graph Search (22) — BFS & DFS traversals, tree/back/forward/cross edges, cycle detection",
            "Ch 1 Algorithms: 1.33 Strongly Connected Components (3), 1.35 Topological Sort (4) — DAG ordering & SCCs",
            "DA AI Extension Preview: State-space graph representation for BFS/DFS search",
            "Session focus: Part A: Solve Ch 1 sections 1.8, 1.10, 1.13, 1.14, 1.33, 1.35 (42 Qs on graph representations, BFS/DFS, topological sort & SCCs) + note direct link to DA AI Uninformed Search.",
        ],
    },
    ("2026-11-05", "Unit 37"): {
        "cs": [
            "Ch 1 Algorithms: 1.9 Dijkstras Algorithm (6), 1.30 Shortest Path (9) — single-source shortest paths, relaxation, negative-weight traps",
            "Ch 1 Algorithms: 1.5 Bellman Ford (2) & Floyd-Warshall all-pairs shortest paths",
            "Session focus: Part B: Solve Ch 1 sections 1.5, 1.9, 1.30 (17 Qs on shortest paths) + DAG shortest paths & DA Uniform Cost Search connection.",
        ],
        "da": [
            "Ch 1 Algorithms: 1.9 Dijkstras Algorithm (6), 1.30 Shortest Path (9) — single-source shortest paths, relaxation, negative-weight traps",
            "DA AI Extension Preview: Dijkstra's algorithm on state-space graphs -> Uniform Cost Search (UCS)",
            "Session focus: Part B: Solve Ch 1 sections 1.5, 1.9, 1.30 (17 Qs on shortest paths) + DAG shortest paths & DA Uniform Cost Search connection.",
        ],
    },
    ("2026-11-06", "Unit 38"): {
        "cs": [
            "Ch 1 Algorithms: 1.15 Greedy Algorithms (5), 1.17 Huffman Code (6) — fractional knapsack, activity selection, prefix codes & tree cost",
            "Ch 1 Algorithms: 1.24 Minimum Spanning Tree (34), 1.25 Prims Algorithm (2) — Kruskal's & Prim's MST algorithms, cut/cycle properties, disjoint sets",
            "Session focus: Solve all 47 Greedy & MST PYQs in Ch 1 (1.15, 1.17, 1.24, 1.25).",
        ],
        "da": [],
    },
    ("2026-11-07", "Unit 39"): {
        "cs": [
            "Ch 1 Algorithms: 1.12 Dynamic Programming (9), 1.21 Matrix Chain Ordering (3) — optimal substructure, overlapping subproblems, memoization vs tabulation",
            "Dynamic Programming Core: Recurrence formulation for LCS, Matrix Chain Multiplication, 0/1 Knapsack, subset sum",
            "Session focus: Part A: Formulate DP recurrences and solve Ch 1 sections 1.12 & 1.21 (12 Qs) + related DP design questions in 1.1/1.2.",
        ],
        "da": [],
    },
    ("2026-11-09", "Unit 39"): {
        "cs": [
            "Ch 1 Algorithms: 1.12 Dynamic Programming (9), 1.21 Matrix Chain Ordering (3) — table tracing & time/space complexity analysis",
            "Mixed Algorithms Synthesis: Compare Greedy vs DP vs Divide & Conquer across Ch 1 (334 Qs complete check)",
            "Session focus: Part B: Complete remaining DP PYQs & mixed Ch 1 Algorithms synthesis.",
        ],
        "da": [],
    },
    ("2026-11-10", "Unit 40"): {
        "cs": [],
        "da": [
            "DA AI Search (Extends Ch 1: 1.8 DFS, 1.9 Dijkstra, 1.14 Graph Search): State-space graphs, tree search vs graph search (visited/closed list)",
            "DA AI Uninformed Search: Breadth-First Search (BFS), Depth-First Search (DFS), Depth-Limited Search, Iterative Deepening Search (IDS), Uniform Cost Search (UCS) — completeness, time/space complexity & optimality",
            "Session focus: Master DA Uninformed Search (direct extension of CS Graph Search Ch 1: 1.8, 1.9, 1.14) + solve DA 2024–2026 search PYQs.",
        ],
    },
    ("2026-11-11", "Unit 41"): {
        "cs": [],
        "da": [
            "DA AI Informed Search (Extends Ch 1: 1.9, 1.30 Shortest Path): Greedy Best-First Search & A* Search (f(n) = g(n) + h(n))",
            "DA AI Heuristics: Admissibility (h(n) <= h*(n)) vs Consistency/Monotonicity (h(n) <= c(n,a,n') + h(n')), dominance (max/min/sum of heuristics), tree vs graph search optimality",
            "Session focus: Master A* node expansion traces & admissibility/consistency proofs + solve DA 2024–2026 heuristic search PYQs.",
        ],
    },
    ("2026-11-12", "Unit 42"): {
        "cs": [],
        "da": [
            "DA AI Adversarial Search: Game playing trees (MAX and MIN nodes), terminal utilities & evaluation functions",
            "DA AI Adversarial Search: Minimax algorithm & Alpha-Beta pruning (alpha/beta cutoffs, move ordering impact, pruned branch conditions)",
            "Session focus: Trace Minimax & Alpha-Beta pruning on game trees + solve DA 2024–2026 adversarial search PYQs.",
        ],
    },
    ("2026-11-13", "Unit 43"): {
        "cs": [
            "Ch 5 Databases: 5.4 Database Design (1), 5.7 ER Diagram (12) — entities, attributes, relationships, cardinality, weak entities, ER-to-Relational mapping",
            "Ch 5 Databases: 5.2 Candidate Key (5), 5.14 Referential Integrity (5), 5.17 Relational Model (2) — superkey/candidate/primary/foreign keys & ON DELETE/UPDATE CASCADE/SET NULL",
            "Session focus: Solve all 25 PYQs in Ch 5 sections 5.2, 5.4, 5.7, 5.14, 5.17 for both CS and DA.",
        ],
        "da": [
            "Ch 5 Databases: 5.4 Database Design (1), 5.7 ER Diagram (12) — entities, attributes, relationships, cardinality, weak entities, ER-to-Relational mapping",
            "Ch 5 Databases: 5.2 Candidate Key (5), 5.14 Referential Integrity (5), 5.17 Relational Model (2) — superkey/candidate/primary/foreign keys & ON DELETE/UPDATE CASCADE/SET NULL",
            "Session focus: Solve all 25 PYQs in Ch 5 sections 5.2, 5.4, 5.7, 5.14, 5.17 for both CS and DA.",
        ],
    },
    ("2026-11-14", "Unit 44"): {
        "cs": [
            "Ch 5 Databases: 5.10 Joins (7), 5.12 Natural Join (3), 5.15 Relational Algebra (31) — selection, projection, rename, union, set difference, Cartesian product, natural/outer joins, division operator",
            "Ch 5 Databases: 5.16 Relational Calculus (15), 5.20 Tuple Relational Calculus (1) — TRC quantifiers, safe queries & equivalence with Relational Algebra",
            "Session focus: Solve all 57 PYQs in Ch 5 sections 5.10, 5.12, 5.15, 5.16, 5.20 for both CS and DA.",
        ],
        "da": [
            "Ch 5 Databases: 5.10 Joins (7), 5.12 Natural Join (3), 5.15 Relational Algebra (31) — selection, projection, rename, union, set difference, Cartesian product, natural/outer joins, division operator",
            "Ch 5 Databases: 5.16 Relational Calculus (15), 5.20 Tuple Relational Calculus (1) — TRC quantifiers, safe queries & equivalence with Relational Algebra",
            "Session focus: Solve all 57 PYQs in Ch 5 sections 5.10, 5.12, 5.15, 5.16, 5.20 for both CS and DA.",
        ],
    },
    ("2026-11-16", "Unit 45"): {
        "cs": [
            "Ch 5 Databases: 5.13 Query (1), 5.18 SQL (58) — Part A: SELECT, WHERE, INNER/LEFT/RIGHT/FULL Joins, GROUP BY, HAVING, aggregate functions (COUNT, SUM, AVG, MIN, MAX), NULL three-valued logic",
            "Session focus: Part A: Solve first 30 SQL PYQs in Ch 5 (5.13, 5.18) covering joins, grouping, aggregation & NULL traps.",
        ],
        "da": [
            "Ch 5 Databases: 5.13 Query (1), 5.18 SQL (58) — Part A: SELECT, WHERE, INNER/LEFT/RIGHT/FULL Joins, GROUP BY, HAVING, aggregate functions (COUNT, SUM, AVG, MIN, MAX), NULL three-valued logic",
            "Session focus: Part A: Solve first 30 SQL PYQs in Ch 5 (5.13, 5.18) covering joins, grouping, aggregation & NULL traps.",
        ],
    },
    ("2026-11-17", "Unit 45"): {
        "cs": [
            "Ch 5 Databases: 5.18 SQL (58) — Part B: Nested subqueries (IN, NOT IN, ANY, ALL), correlated subqueries (EXISTS, NOT EXISTS), views, set operations (UNION/INTERSECT/EXCEPT)",
            "Session focus: Part B: Finish remaining 29 SQL PYQs in Ch 5 (5.18) + DA correlated query & view questions.",
        ],
        "da": [
            "Ch 5 Databases: 5.18 SQL (58) — Part B: Nested subqueries (IN, NOT IN, ANY, ALL), correlated subqueries (EXISTS, NOT EXISTS), views, set operations (UNION/INTERSECT/EXCEPT)",
            "Session focus: Part B: Finish remaining 29 SQL PYQs in Ch 5 (5.18) + DA correlated query & view questions.",
        ],
    },
    ("2026-11-18", "Unit 46"): {
        "cs": [
            "Ch 5 Databases: 5.8 Functional Dependency (2), 5.2 Candidate Key (5), 5.5 Database Normalization (56) — Part A: Armstrong's axioms, attribute closure, finding all candidate keys, canonical/minimal cover",
            "Session focus: Part A: Solve first 30 Normalization & FD PYQs in Ch 5 (5.5, 5.8) on closures, keys & minimal cover.",
        ],
        "da": [
            "Ch 5 Databases: 5.8 Functional Dependency (2), 5.2 Candidate Key (5), 5.5 Database Normalization (56) — Part A: Armstrong's axioms, attribute closure, finding all candidate keys, canonical/minimal cover",
            "Session focus: Part A: Solve first 30 Normalization & FD PYQs in Ch 5 (5.5, 5.8) on closures, keys & minimal cover.",
        ],
    },
    ("2026-11-19", "Unit 46"): {
        "cs": [
            "Ch 5 Databases: 5.5 Database Normalization (56), 5.6 Decomposition (1) — Part B: Normal forms (1NF, 2NF, 3NF, BCNF), lossless-join decomposition, dependency preservation",
            "Ch 5 Databases: 5.11 Multivalued Dependency 4nf (1) — MVD & 4NF awareness",
            "Session focus: Part B: Finish remaining 29 Normalization & Decomposition PYQs in Ch 5 (5.5, 5.6, 5.11).",
        ],
        "da": [
            "Ch 5 Databases: 5.5 Database Normalization (56), 5.6 Decomposition (1) — Part B: Normal forms (1NF, 2NF, 3NF, BCNF), lossless-join decomposition, dependency preservation",
            "Session focus: Part B: Finish remaining 29 Normalization & Decomposition PYQs in Ch 5 (5.5, 5.6, 5.11).",
        ],
    },
    ("2026-11-20", "Unit 47"): {
        "cs": [
            "Ch 5 Databases: 5.9 Indexing (13) — ordered/unordered files, blocking factor, dense vs sparse, primary, clustering & secondary (multilevel) indexes",
            "Ch 5 Databases: 5.1 B Tree (31) — B-tree and B+ tree order (p), node capacity, height bounds, insertion/deletion splits",
            "Session focus: Solve all 44 Indexing & B/B+ Tree PYQs in Ch 5 (5.1, 5.9) for CS and DA.",
        ],
        "da": [
            "Ch 5 Databases: 5.9 Indexing (13) — ordered/unordered files, blocking factor, dense vs sparse, primary, clustering & secondary (multilevel) indexes",
            "Ch 5 Databases: 5.1 B Tree (31) — B-tree and B+ tree order (p), node capacity, height bounds, insertion/deletion splits",
            "Session focus: Solve all 44 Indexing & B/B+ Tree PYQs in Ch 5 (5.1, 5.9) for CS and DA.",
        ],
    },
    ("2026-11-21", "Unit 48"): {
        "cs": [
            "Ch 5 Databases: 5.3 Conflict Serializable (9), 5.19 Transaction and Concurrency (30) — ACID properties, schedules, conflict & view serializability, precedence graph",
            "Transaction Recovery & Concurrency: Recoverable, cascadeless & strict schedules, 2PL (basic/strict/rigorous), timestamp ordering, Thomas write rule, deadlock handling & log-based recovery",
            "Session focus: Solve all 39 Transaction & Concurrency PYQs in Ch 5 (5.3, 5.19) — completes all 284 Databases PYQs!",
        ],
        "da": [],
    },
    ("2026-11-23", "Unit 49"): {
        "cs": [],
        "da": [
            "DA Databases Extension — Data Warehousing 1 (Data Preparation & Preprocessing): Attribute types (nominal, ordinal, interval, ratio)",
            "DA Data Transformation: Normalization (min-max, z-score, decimal scaling), discretization & binning, sampling (simple random, stratified, cluster), data compression & cleaning",
            "Session focus: Master DA Data Preparation & Transformation formulas + solve DA 2024–2026 data preprocessing PYQs.",
        ],
    },
    ("2026-11-24", "Unit 50"): {
        "cs": [],
        "da": [
            "DA Databases Extension — Data Warehousing 2 (Schemas & OLAP): Multidimensional data models, data cubes & cuboid lattice (2^n and hierarchy cuboid counts)",
            "DA Warehouse Schemas & Measures: Star schema, Snowflake schema, Fact Constellation (Galaxy) schema, concept hierarchies",
            "DA OLAP Operations & Measures: Roll-up (drill-up), drill-down, slice, dice, pivot; Distributive (SUM, COUNT, MIN, MAX), Algebraic (AVG) & Holistic (MEDIAN, MODE, RANK) measures",
            "Session focus: Master Data Warehousing schemas, cuboid counting & OLAP operations + solve DA 2024–2026 warehousing PYQs.",
        ],
    },
    ("2026-11-25", "Unit 51"): {
        "cs": [
            "Ch 10 Theory of Computation: 10.7 Finite Automata (42), 10.8 Finite State Machines (1), 10.10 Minimal State Automata (25), 10.11 Non Determinism (6), 10.12 Number of States (1) — DFA, NFA, epsilon-NFA, subset construction & DFA minimization",
            "Ch 10 Theory of Computation: 10.17 Regular Expression (29), 10.18 Regular Grammar (3) — RE identities, Arden's theorem, right/left-linear grammars, Moore & Mealy machines",
            "Session focus: Solve all 107 PYQs in Ch 10 sections 10.7, 10.8, 10.10, 10.11, 10.12, 10.17, 10.18.",
        ],
        "da": [],
    },
    ("2026-11-26", "Unit 52"): {
        "cs": [
            "Ch 10 Theory of Computation: 10.1 Closure Property (9), 10.13 Pumping Lemma (2), 10.19 Regular Language (36) — closure under operations & proving non-regularity",
            "Ch 3 Compiler Design: 3.5 Compilation Phases (12), 3.11 Lexical Analysis (6), 3.21 Symbol Table (1) — tokens, lexemes, longest-match DFA scanner",
            "Ch 3 Compiler Design (Supporting Systems): 3.1 Assembler (9), 3.12 Linker (3), 3.14 Macros (4)",
            "Session focus: Solve 47 Regular Language PYQs in Ch 10 (10.1, 10.13, 10.19) + 35 Lexical/Phases/Assembler/Linker/Macro PYQs in Ch 3 (3.1, 3.5, 3.11, 3.12, 3.14, 3.21).",
        ],
        "da": [],
    },
    ("2026-11-27", "Unit 53"): {
        "cs": [
            "Ch 10 Theory of Computation: 10.2 Context Free Grammar (2), 10.3 Context Free Language (33) — CFG derivations, ambiguity, Chomsky Normal Form (CNF), closure properties & CFL pumping lemma",
            "Ch 10 Theory of Computation: 10.6 Dpda (1), 10.14 Pushdown Automata (15) — DPDA vs NPDA, acceptance by final state vs empty stack, DCFL vs CFL",
            "Session focus: Solve all 51 CFG, CFL & PDA PYQs in Ch 10 (10.2, 10.3, 10.6, 10.14).",
        ],
        "da": [],
    },
    ("2026-11-28", "Unit 54"): {
        "cs": [
            "Ch 10 Theory of Computation: 10.4 Countable Uncountable Set (3), 10.9 Identify Class Language (31) — Chomsky hierarchy classification (Regular vs DCFL vs CFL vs CSL vs Recursive vs RE)",
            "Ch 10 Theory of Computation: 10.5 Decidability (29), 10.15 Recursive and Recursively Enumerable Languages (16), 10.16 Reduction (2) — Turing machines, Halting problem, Rice's theorem & decidability table",
            "Session focus: Solve all 81 PYQs in Ch 10 (10.4, 10.5, 10.9, 10.15, 10.16) — completes all 286 Theory of Computation PYQs!",
        ],
        "da": [],
    },
    ("2026-11-30", "Unit 55"): {
        "cs": [
            "Ch 3 Compiler Design: 3.7 First and Follow (6), 3.8 Grammar (51) — left recursion elimination, left factoring, ambiguity, FIRST & FOLLOW sets",
            "Ch 3 Compiler Design: 3.17 Parsing (27) — Part A: Recursive descent & LL(1) parsing table construction and conflicts",
            "Session focus: Part A: Solve Ch 3 sections 3.7, 3.8 & top-down parsing in 3.17 (~65 Qs).",
        ],
        "da": [],
    },
    ("2026-12-01", "Unit 55"): {
        "cs": [
            "Ch 3 Compiler Design: 3.10 LR Parser (20), 3.15 Operator Precedence (3), 3.17 Parsing (27) — Part B: Shift-reduce parsing, handle pruning, LR(0), SLR(1), CLR(1), LALR(1) item sets, state counts & SR/RR conflicts",
            "Session focus: Part B: Solve all bottom-up & LR Parser PYQs in Ch 3 (3.10, 3.15, 3.17).",
        ],
        "da": [],
    },
    ("2026-12-02", "Unit 56"): {
        "cs": [
            "Ch 3 Compiler Design: 3.6 Expression Evaluation (2), 3.22 Syntax Directed Translation (17) — S-attributed vs L-attributed SDDs, annotated parse tree evaluation",
            "Ch 3 Compiler Design: 3.2 Backpatching (1), 3.9 Intermediate Code (11) — Three-Address Code (TAC), quadruples, triples, control-flow backpatching",
            "Ch 3 Compiler Design: 3.16 Parameter Passing (14), 3.19 Runtime Environment (22), 3.23 Variable Scope (2) — activation records, call stack, static/dynamic scope, call-by-value/reference/name",
            "Session focus: Solve all 69 PYQs in Ch 3 sections 3.2, 3.6, 3.9, 3.16, 3.19, 3.22, 3.23.",
        ],
        "da": [],
    },
    ("2026-12-03", "Unit 57"): {
        "cs": [
            "Ch 3 Compiler Design: 3.3 Basic Blocks (1), 3.4 Code Optimization (10), 3.20 Static Single Assignment (3) — leader rules, control flow graphs (CFG), SSA form, constant folding/propagation, strength reduction, common subexpression elimination, dead code elimination, loop optimization",
            "Ch 3 Compiler Design: 3.13 Live Variable Analysis (3), 3.18 Register Allocation (6) — data-flow IN/OUT equations, liveness analysis & register interference graph coloring",
            "Session focus: Solve all 23 PYQs in Ch 3 sections 3.3, 3.4, 3.13, 3.18, 3.20 — completes all 234 Compiler Design PYQs!",
        ],
        "da": [],
    },
    ("2026-12-04", "Unit 58"): {
        "cs": [
            "Ch 6 Digital Logic: 6.3 Boolean Algebra (34), 6.5 Canonical Normal Form (9), 6.16 Functional Completeness (7), 6.20 Min No Gates (4) — logic gates, NAND/NOR universality, SOP/POS minterms & maxterms",
            "Ch 6 Digital Logic: 6.18 K Map (20), 6.21 Min Products of Sum Form (2), 6.22 Min Sum of Products Form (15), 6.25 Prime Implicants (2), 6.30 Static Hazard (1) — K-map minimization, essential prime implicants, Quine-McCluskey tabular method & hazard cover",
            "Session focus: Solve all 94 Boolean & Minimization PYQs in Ch 6 (6.3, 6.5, 6.16, 6.18, 6.20, 6.21, 6.22, 6.25, 6.30).",
        ],
        "da": [],
    },
    ("2026-12-05", "Unit 59"): {
        "cs": [
            "Ch 6 Digital Logic (Combinational): 6.1 Adder (9), 6.2 Array Multiplier (2), 6.6 Carry Generator (2), 6.7 Circuit Output (40), 6.8 Combinational Circuit (2), 6.9 Decoder (3), 6.10 Digital Circuits (6), 6.19 Memory Interfacing (5), 6.23 Multiplexer (14), 6.26 ROM (4)",
            "Ch 6 Digital Logic (Sequential): 6.11 Digital Counter (17), 6.12 Finite State Machines (4), 6.14 Flip Flop (6), 6.27 Ripple Counter Operation (1), 6.28 Sequential Circuit (1), 6.29 Shift Registers (2), 6.31 Synchronous Asynchronous Circuits (4)",
            "Ch 6 Digital Logic (Number & Arithmetic): 6.4 Booths Algorithm (7), 6.13 Fixed Point Representation (2), 6.15 Floating Point Representation (12), 6.17 IEEE Representation (8), 6.24 Number Representation (58)",
            "Session focus: Solve Ch 6 Combinational (87 Qs), Sequential (35 Qs) & Number/Arithmetic (87 Qs) — completes all 303 Digital Logic PYQs!",
        ],
        "da": [],
    },
    ("2026-12-07", "Unit 60"): {
        "cs": [
            "Ch 2 CO & Architecture: 2.1 Addressing Modes (18), 2.3 CISC RISC Architecture (2), 2.11 Instruction Format (9), 2.12 Instruction Set Architecture (1), 2.14 Machine Instruction (21), 2.18 Runtime Environment (2)",
            "Ch 2 CO & Architecture: 2.5 Clock Cycles (1), 2.8 Data Path (7), 2.10 Instruction Execution (6), 2.16 Microprogramming (13) — ALU, single/multi-cycle datapath, hardwired vs horizontal/vertical microprogrammed control unit",
            "Session focus: Solve all 80 ISA, Datapath & Control Unit PYQs in Ch 2 (2.1, 2.3, 2.5, 2.8, 2.10, 2.11, 2.12, 2.14, 2.16, 2.18).",
        ],
        "da": [],
    },
    ("2026-12-08", "Unit 61"): {
        "cs": [
            "Ch 2 CO & Architecture: 2.7 Data Dependency (2), 2.17 Pipelining (43), 2.19 Speedup (4) — 5-stage pipeline, speedup, throughput, CPI with stalls, structural, data (RAW/WAR/WAW) & branch hazards, operand forwarding",
            "Session focus: Solve all 49 Pipelining, Dependency & Speedup PYQs in Ch 2 (2.7, 2.17, 2.19).",
        ],
        "da": [],
    },
    ("2026-12-09", "Unit 62"): {
        "cs": [
            "Ch 2 CO & Architecture: 2.2 Average Memory Access Time (2), 2.4 Cache Memory (73) — Part A: Direct mapped, fully associative & k-way set-associative mapping, tag/index/offset bits, tag directory size, AMAT (hierarchical & simultaneous)",
            "Session focus: Part A: Solve first 45 Cache & AMAT PYQs in Ch 2 (2.2, 2.4).",
        ],
        "da": [],
    },
    ("2026-12-10", "Unit 62"): {
        "cs": [
            "Ch 2 CO & Architecture: 2.4 Cache Memory (73) — Part B: Replacement policies (LRU/FIFO), write-through vs write-back, dirty bit, write allocate",
            "Ch 2 CO & Architecture: 2.6 DMA (9), 2.9 IO Handling (7), 2.13 Interrupts (9), 2.15 Memory Interfacing (6), 2.20 Virtual Memory (3) — chip select decoding, cycle stealing vs burst DMA, vectored vs polled interrupts",
            "Session focus: Part B: Finish remaining 30 Cache PYQs + all 34 Memory Interfacing, I/O, Interrupts & DMA PYQs in Ch 2 (2.6, 2.9, 2.13, 2.15, 2.20) — completes all 238 COA PYQs!",
        ],
        "da": [],
    },
    ("2026-12-11", "Unit 63"): {
        "cs": [
            "Ch 7 Operating System: 7.1 Context Switch (4), 7.6 Fork System Call (7), 7.14 OS Protection (3), 7.18 Process (5), 7.25 System Calls (1), 7.26 Threads (10) — PCB, process states, fork() process tree counting, user vs kernel threads, mode switch",
            "Ch 7 Operating System: 7.19 Process Scheduling (48), 7.24 Srtf (1) — FCFS, SJF, SRTF, Round Robin, Priority, multilevel feedback queue, turnaround/waiting/response time Gantt charts",
            "Session focus: Solve all 79 Process, Threads & CPU Scheduling PYQs in Ch 7 (7.1, 7.6, 7.14, 7.18, 7.19, 7.24, 7.25, 7.26).",
        ],
        "da": [],
    },
    ("2026-12-12", "Unit 64"): {
        "cs": [
            "Ch 7 Operating System: 7.17 Precedence Graph (3), 7.20 Process Synchronization (52) — Part A: Race conditions, critical section requirements (mutual exclusion, progress, bounded waiting), Peterson's solution, Test-and-Set / Compare-and-Swap hardware locks",
            "Session focus: Part A: SolveCh 7 section 7.17 (3 Qs) & first 27 Synchronization PYQs in 7.20.",
        ],
        "da": [],
    },
    ("2026-12-14", "Unit 64"): {
        "cs": [
            "Ch 7 Operating System: 7.9 Inter Process Communication (1), 7.20 Process Synchronization (52), 7.23 Semaphore (10) — Part B: Counting & binary semaphores, Producer-Consumer, Readers-Writers, Dining Philosophers, IPC (shared memory & message passing)",
            "Session focus: Part B: Finish remaining 25 Synchronization PYQs in 7.20 + all 11 Semaphore & IPC PYQs in Ch 7 (7.9, 7.23).",
        ],
        "da": [],
    },
    ("2026-12-15", "Unit 65"): {
        "cs": [
            "Ch 7 Operating System: 7.2 Deadlock Prevention Avoidance Detection (4), 7.21 Resource Allocation (27), 7.22 Resource Allocation Graph (1) — Coffman conditions, RAG single/multi-instance cycle analysis, Banker's safety & request algorithm, max-resource deadlock-free formula",
            "Session focus: Solve all 32 Deadlock & Resource Allocation PYQs in Ch 7 (7.2, 7.21, 7.22).",
        ],
        "da": [],
    },
    ("2026-12-16", "Unit 66"): {
        "cs": [
            "Ch 7 Operating System: 7.12 Memory Management (10), 7.13 Multilevel Paging (1), 7.27 Virtual Memory (43) — Part A: First/best/worst fit, internal/external fragmentation, paging address translation, hierarchical page tables, inverted page table, TLB effective memory access time (EMAT) & segmentation",
            "Session focus: Part A: Solve Ch 7 sections 7.12, 7.13 (11 Qs) & first 20 Virtual Memory/Paging PYQs in 7.27.",
        ],
        "da": [],
    },
    ("2026-12-17", "Unit 66"): {
        "cs": [
            "Ch 7 Operating System: 7.15 Optimal Page Replacement (1), 7.16 Page Replacement (33), 7.27 Virtual Memory (43) — Part B: Demand paging, page fault service time, FIFO (Belady's anomaly), Optimal, LRU, Second-Chance/Clock replacement, working set & thrashing",
            "Session focus: Part B: Solve all 34 Page Replacement PYQs (7.15, 7.16) & remaining 23 Virtual Memory PYQs in Ch 7 (7.27).",
        ],
        "da": [],
    },
    ("2026-12-18", "Unit 67"): {
        "cs": [
            "Ch 7 Operating System: 7.5 File System (9), 7.11 Linked Allocation (1) — contiguous, linked, FAT & indexed (UNIX direct/indirect inode max file size) allocation, bit vector & free space management",
            "Ch 7 Operating System: 7.3 Disk (31), 7.4 Disk Scheduling (14), 7.7 IO Handling (7), 7.8 Input Output (1), 7.10 Interrupts (6) — disk seek/rotational/transfer time, FCFS, SSTF, SCAN, C-SCAN, LOOK, C-LOOK",
            "Session focus: Solve all 69 File System, Disk & I/O PYQs in Ch 7 (7.3, 7.4, 7.5, 7.7, 7.8, 7.10, 7.11) — completes all 335 Operating System PYQs!",
        ],
        "da": [],
    },
    ("2026-12-19", "Unit 68"): {
        "cs": [
            "Ch 4 Computer Networks: 4.7 Channel Utilization (1), 4.8 Communication (4), 4.18 Network Flow (4), 4.19 Network Layering (6), 4.21 Network Switching (4), 4.22 Osi Model (1), 4.23 Probability (1) — layering principles, circuit/packet/virtual-circuit switching, delay/throughput/BDP",
            "Ch 4 Computer Networks: 4.3 Bit Stuffing (2), 4.4 Bridges (3), 4.5 CRC Polynomial (4), 4.6 CSMA CD (6), 4.11 Error Detection (10), 4.12 Ethernet (7), 4.16 LAN Technologies (7), 4.17 MAC Protocol (5) — CRC & Hamming distance, ALOHA, CSMA/CD exponential backoff, Ethernet frame & minimum frame size (L >= 2*Tp*B)",
            "Ch 4 Computer Networks: 4.26 Sliding Window (15), 4.28 Stop and Wait (6) — link/end-to-end Stop-and-Wait, Go-Back-N & Selective Repeat utilization and sequence number bits",
            "Session focus: Solve all 82 Layering, Error Detection, MAC, Ethernet & Sliding Window PYQs in Ch 4.",
        ],
        "da": [],
    },
    ("2026-12-21", "Unit 69"): {
        "cs": [
            "Ch 4 Computer Networks (IP & Addressing): 4.2 Arp (1), 4.13 Fragmentation (2), 4.14 IP Addressing (11), 4.15 IP Packet (11), 4.20 Network Protocols (10), 4.29 Subnetting (21) — IPv4 header, fragmentation & offsets, CIDR subnetting/supernetting, longest prefix match, NAT, ARP, DHCP, ICMP",
            "Ch 4 Computer Networks (Routing): 4.10 Distance Vector Routing (8), 4.24 Routing (13), 4.25 Routing Protocols (1) — Bellman-Ford distance vector (count-to-infinity) & Dijkstra link-state routing",
            "Ch 4 Computer Networks (Transport & App): 4.1 Application Layer Protocols (12), 4.9 Congestion Control (6), 4.27 Sockets (4), 4.30 TCP (22), 4.31 Token Bucket (2), 4.32 UDP (4) — TCP 3-way handshake, seq/ack numbers, flow control, slow start & AIMD congestion window, UDP, sockets, DNS & HTTP",
            "Session focus: Solve all 133 IP, Subnetting, Routing, TCP/UDP & App Layer PYQs in Ch 4 — completes all 215 Computer Networks PYQs!",
        ],
        "da": [],
    },
    ("2026-12-22", "Unit 18"): {
        "cs": [],
        "da": [
            "DA AI Reasoning under Uncertainty 1 (Extends Engg Math Ch 7: 7.1 Bayes Theorem (1), 7.2 Bayesian Network (2), 7.5 Conditional Probability (14)): Representation of conditional independence in Directed Acyclic Graphs (DAGs)",
            "DA Bayesian Networks: Local Markov property, joint probability factorization P(X1,...,Xn) = Prod P(Xi | Parents(Xi)), d-separation (causal chain, common cause, common effect / V-structure explaining away) & CPT parameter counting",
            "Session focus: Solve Engg Math Ch 7 sections 7.1, 7.2, 7.5 + DA 2024–2026 Bayesian Network PYQs.",
        ],
    },
    ("2026-12-23", "Unit 19"): {
        "cs": [],
        "da": [
            "DA AI Reasoning under Uncertainty 2: Exact inference in Bayesian Networks via Variable Elimination (factor product, summing out hidden variables, elimination ordering complexity)",
            "DA Approximate Inference via Sampling: Prior sampling, Rejection sampling, Likelihood weighting (importance weights) & Gibbs sampling (Markov blanket transitions)",
            "Session focus: Trace Variable Elimination & Sampling methods by hand + solve DA 2024–2026 inference PYQs.",
        ],
    },
    ("2026-12-24", "Unit 20"): {
        "cs": [],
        "da": [
            "DA Machine Learning 1 (Applies Engg Math Ch 6 Projections & Matrix 6.6/6.11): Supervised regression setup, Simple & Multiple Linear Regression, ordinary least squares normal equations w* = (X^T X)^(-1) X^T y, residual orthogonality",
            "DA Ridge Regression (L2 Regularization): Objective ||y - Xw||_2^2 + lambda ||w||_2^2, closed-form w_ridge = (X^T X + lambda I)^(-1) X^T y, bias-variance effect of lambda",
            "Session focus: Master Linear & Ridge Regression derivations and numericals + solve DA 2024–2026 regression PYQs.",
        ],
    },
    ("2026-12-25", "Unit 21"): {
        "cs": [],
        "da": [
            "DA Machine Learning 2 (Applies Engg Math Ch 5 Calculus 5.3/5.6): Logistic Regression, sigmoid function sigma(z) = 1/(1+e^(-z)), log-odds / linear decision boundary, binary cross-entropy (negative log-likelihood) & gradient descent update",
            "DA k-Nearest Neighbour (k-NN): Euclidean, Manhattan & Minkowski distance metrics, effect of k on decision boundary smoothness and bias-variance",
            "Session focus: Master Logistic Regression & k-NN numericals + solve DA 2024–2026 classification PYQs.",
        ],
    },
    ("2026-12-26", "Unit 22"): {
        "cs": [],
        "da": [
            "DA Machine Learning 3 (Applies Engg Math Ch 7 Bayes 7.1 & Normal Dist 7.10): Generative vs discriminative classifiers, Naive Bayes conditional independence assumption, parameter counting for binary/categorical features & Laplace smoothing",
            "DA Linear Discriminant Analysis (LDA): Gaussian class-conditional densities with shared covariance Sigma, linear decision boundary w = Sigma^(-1)(mu_1 - mu_0) & Fisher's between-class / within-class scatter ratio",
            "Session focus: Master Naive Bayes & LDA numericals + solve DA 2024–2026 generative classifier PYQs.",
        ],
    },
    ("2026-12-28", "Unit 23"): {
        "cs": [],
        "da": [
            "DA Machine Learning 4 — Support Vector Machines (Part A): Linearly separable binary classification, hyperplane w^T x + b = 0, geometric margin 2/||w||, primal quadratic optimization min (1/2)||w||^2 s.t. y_i(w^T x_i + b) >= 1, identifying support vectors",
            "DA Soft-Margin SVM: Slack variables xi_i >= 0, hinge loss max(0, 1 - y_i f(x_i)) & regularization trade-off parameter C",
            "Session focus: Part A: Master hard-margin & soft-margin SVM geometry, support vector identification & margin calculation.",
        ],
    },
    ("2026-12-29", "Unit 23"): {
        "cs": [],
        "da": [
            "DA Machine Learning 4 — Support Vector Machines (Part B): Dual formulation, KKT complementary slackness conditions (alpha_i > 0 only for support vectors)",
            "DA Kernel Trick: Mercer's condition, polynomial kernel (x^T z + c)^d, Radial Basis Function (RBF / Gaussian) kernel exp(-gamma ||x - z||^2) & non-linear feature mapping",
            "Session focus: Part B: Solve dual/kernel SVM numericals + all DA 2024–2026 SVM PYQs.",
        ],
    },
    ("2026-12-30", "Unit 24"): {
        "cs": [],
        "da": [
            "DA Machine Learning 5 — Decision Trees: Impurity measures — Shannon Entropy H(S) = -sum p_i log2(p_i), Information Gain IG(S, A), Gini Impurity 1 - sum p_i^2, variance reduction for regression trees",
            "DA Tree Construction & Overfitting: ID3/CART recursive splitting, continuous attribute threshold selection, pre-pruning & post-pruning",
            "Session focus: Compute Entropy, Information Gain & Gini splits by hand + solve DA 2024–2026 Decision Tree PYQs.",
        ],
    },
    ("2026-12-31", "Unit 25"): {
        "cs": [],
        "da": [
            "DA Machine Learning 6 — Model Evaluation & Cross-Validation: Train/validation/test split, k-fold cross-validation & Leave-One-Out (LOO-CV) computational cost and variance",
            "DA Bias-Variance & Classification Metrics: Expected test MSE = Bias^2 + Variance + Irreducible Noise, underfitting vs overfitting, confusion matrix, Accuracy, Precision, Recall, F1-score, ROC curve & AUC",
            "Session focus: Master Bias-Variance decomposition, k-fold/LOO-CV & evaluation metrics + solve DA 2024–2026 PYQs.",
        ],
    },
    ("2027-01-01", "Unit 26"): {
        "cs": [],
        "da": [
            "DA Machine Learning 7 — Neural Networks: Multi-Layer Perceptron (MLP) & feed-forward architecture, total trainable weights & biases count across layers, XOR non-linear separability",
            "DA Activation Functions & Backpropagation: Sigmoid, Tanh, ReLU, Softmax & their derivatives; chain-rule backpropagation gradients & stochastic/mini-batch gradient descent weight updates",
            "Session focus: Practice network parameter counting & 1-step backpropagation numericals + solve DA 2024–2026 Neural Network PYQs.",
        ],
    },
    ("2027-01-02", "Unit 27"): {
        "cs": [],
        "da": [
            "DA Machine Learning 8 — Unsupervised Learning Part A (Clustering): k-means (Lloyd's algorithm, within-cluster sum of squares objective, centroid updates, initialization traps) & k-medoids (PAM, robustness to outliers/L1 distance)",
            "DA Hierarchical Clustering: Agglomerative (bottom-up) vs Divisive (top-down), dendrogram cutting, Single-linkage (min), Complete-linkage (max), Average-linkage & Ward's linkage distance matrix updates",
            "Session focus: Part A: Trace k-means, k-medoids & hierarchical linkage merges step-by-step + solve DA 2024–2026 clustering PYQs.",
        ],
    },
    ("2027-01-04", "Unit 27"): {
        "cs": [],
        "da": [
            "DA Machine Learning 8 — Unsupervised Learning Part B (PCA — Applies Engg Math Ch 6: 6.3 Eigen Value (33), 6.7 Orthonormality (2), 6.9 SVD (1)): Sample covariance matrix S = (1/n) X_c^T X_c, maximizing projected variance u^T S u, principal components as top eigenvectors of S",
            "DA PCA & Reconstruction: Proportion of variance explained lambda_k / sum(lambda_i), low-rank reconstruction error sum_{i > k} lambda_i & relation between SVD of centered data X_c = U Sigma V^T and eigenvalues of X_c^T X_c",
            "Session focus: Part B: Solve covariance/eigenvalue PCA problems + all DA 2024–2026 PCA & SVD PYQs (completes 100% of DA syllabus!).",
        ],
    },
    ("2027-01-05", "Second pass"): {
        "cs": [
            "Engg Math Ch 6 Linear Algebra (102 Qs): 6.1–6.12 starred PYQs & mistake-log re-solve",
            "Engg Math Ch 5 Calculus (63 Qs): 5.1–5.7 starred PYQs & mistake-log re-solve",
            "Discrete Math Ch 1 Combinatory (50 Qs), Ch 2 Graph Theory (83 Qs), Ch 3 Logic (77 Qs), Ch 4 Set Theory & Algebra (171 Qs): Starred PYQs & mistake-log re-solve",
            "Session focus: Rapid formula sheet revision (2 hrs) + timed mixed Math PYQ set (2 hrs) + re-solve every logged Math mistake (1.5 hrs).",
        ],
        "da": [
            "Engg Math Ch 6 Linear Algebra (102 Qs): 6.1–6.12 starred PYQs & mistake-log re-solve",
            "DA Linear Algebra Extensions: Projections, Idempotent/Orthogonal/Partition matrices, Quadratic Forms, SVD",
            "Engg Math Ch 5 Calculus (63 Qs): 5.1–5.7 starred PYQs & mistake-log re-solve",
            "DA Calculus Extensions: Taylor series & single-variable optimization",
            "Discrete Math Ch 3 Logic (77 Qs), Ch 1 Combinatory (1.1–1.3, 1.6), Ch 2 Graph Connectivity (2.2, 2.4)",
            "Session focus: Rapid formula sheet revision (2 hrs) + timed mixed Math PYQ set (2 hrs) + re-solve every logged Math mistake (1.5 hrs).",
        ],
    },
    ("2027-01-06", "Second pass"): {
        "cs": [
            "Engg Math Ch 7 Probability & Statistics (107 Qs): 7.1–7.19 starred PYQs & mistake-log re-solve",
            "Session focus: Rapid formula sheet revision (2 hrs) + timed mixed Probability/Stats/AI Uncertainty PYQ set (2 hrs) + mistake-log re-solve (1.5 hrs).",
        ],
        "da": [
            "Engg Math Ch 7 Probability & Statistics (107 Qs): 7.1–7.19 starred PYQs & mistake-log re-solve",
            "DA Statistics & Distributions Extensions: Joint/Marginal/Conditional PDFs, Covariance/Correlation, Tower Rule, CLT, t/Chi-square, Confidence Intervals, z/t/Chi-square Hypothesis Testing",
            "DA AI Uncertainty (Units 18–19): Bayesian Networks, d-separation, Variable Elimination & Sampling",
            "Session focus: Rapid formula sheet revision (2 hrs) + timed mixed Probability/Stats/AI Uncertainty PYQ set (2 hrs) + mistake-log re-solve (1.5 hrs).",
        ],
    },
    ("2027-01-07", "Second pass"): {
        "cs": [],
        "da": [
            "DA Machine Learning Complete Revision (Units 20–27): Linear & Ridge Regression, Logistic Regression, k-NN, Naive Bayes, LDA, SVM & Kernels, Decision Trees, Cross-Validation & Bias-Variance, MLP & Backprop, k-means/k-medoids/Hierarchical Clustering, PCA",
            "Session focus: Rapid ML formula sheet revision (2 hrs) + timed mixed DA ML PYQs & practice set (2 hrs) + re-solve all logged ML mistakes (1.5 hrs).",
        ],
    },
    ("2027-01-08", "Second pass"): {
        "cs": [
            "Core CS Ch 9 Programming in C (127 Qs): 9.1–9.19 starred output tracing, pointers, recursion & scope PYQs",
            "Core CS Ch 8 Data Structures (236 Qs): 8.1–8.15 starred Arrays, Stacks, Queues, Linked Lists, Binary Trees, BST, AVL, Heaps & Hashing PYQs",
            "Session focus: Rapid revision of C/Python & DS notes (2 hrs) + timed mixed Ch 8 & Ch 9 PYQ set (2 hrs) + re-solve all logged mistakes (1.5 hrs).",
        ],
        "da": [
            "DA Python Programming: Syntax, data types, lists/dicts/sets/slicing, closures & output tracing",
            "Core CS Ch 8 Data Structures (236 Qs): 8.1, 8.2, 8.4–8.10, 8.12–8.15 starred Arrays, Stacks, Queues, Linked Lists, Trees, BST, AVL & Hashing PYQs",
            "Session focus: Rapid revision of C/Python & DS notes (2 hrs) + timed mixed Ch 8 & Ch 9 PYQ set (2 hrs) + re-solve all logged mistakes (1.5 hrs).",
        ],
    },
    ("2027-01-09", "Second pass"): {
        "cs": [
            "Core CS Ch 1 Algorithms (334 Qs): 1.1–1.35 starred Asymptotics, Recurrences, Sorting, Divide & Conquer, BFS/DFS, Shortest Paths, MST, Greedy & Dynamic Programming PYQs",
            "Session focus: Rapid Algorithms & AI Search formula review (2 hrs) + timed mixed Ch 1 & AI Search PYQ set (2 hrs) + re-solve all logged mistakes (1.5 hrs).",
        ],
        "da": [
            "Core CS Ch 1 Algorithms (Shared): 1.1–1.4, 1.6–1.11, 1.13, 1.14, 1.16, 1.18–1.20, 1.22, 1.23, 1.26, 1.28–1.35 starred Complexity, Searching, Sorting & Graph PYQs",
            "DA AI Search (Units 40–42): Uninformed Search (BFS/DFS/UCS/IDS), Informed Search (Greedy Best-First, A*, admissibility/consistency) & Adversarial Search (Minimax, Alpha-Beta pruning)",
            "Session focus: Rapid Algorithms & AI Search formula review (2 hrs) + timed mixed Ch 1 & AI Search PYQ set (2 hrs) + re-solve all logged mistakes (1.5 hrs).",
        ],
    },
    ("2027-01-11", "Second pass"): {
        "cs": [
            "Core CS Ch 5 Databases (284 Qs): 5.1–5.20 starred B/B+ Trees, ER Model, Keys, Relational Algebra, TRC, SQL, Normalization (1NF–BCNF) & Transactions/Concurrency PYQs",
            "Session focus: Rapid DBMS & Warehousing revision (2 hrs) + timed mixed Ch 5 & Warehousing PYQ set (2 hrs) + re-solve all logged mistakes (1.5 hrs).",
        ],
        "da": [
            "Core CS Ch 5 Databases (Shared): 5.1, 5.2, 5.4–5.10, 5.12–5.18, 5.20 starred B/B+ Trees, ER Model, Keys, Relational Algebra, TRC, SQL & Normalization PYQs",
            "DA Data Warehousing (Units 49–50): Data Prep & Normalization/Transformation, Star/Snowflake/Galaxy Schemas, Cuboid Lattice & OLAP Measures",
            "Session focus: Rapid DBMS & Warehousing revision (2 hrs) + timed mixed Ch 5 & Warehousing PYQ set (2 hrs) + re-solve all logged mistakes (1.5 hrs).",
        ],
    },
    ("2027-01-12", "Second pass"): {
        "cs": [
            "Core CS Ch 10 Theory of Computation (286 Qs): 10.1–10.19 starred Finite Automata, Regular Expressions/Languages, CFG/CFL, PDA, Turing Machines & Decidability PYQs",
            "Core CS Ch 3 Compiler Design (234 Qs): 3.1–3.23 starred Lexical, FIRST/FOLLOW, LL(1)/LR Parsers, SDT, TAC, Runtime & Code Optimization PYQs",
            "Session focus: Rapid TOC & Compiler formula review (2 hrs) + timed mixed Ch 10 & Ch 3 PYQ set (2 hrs) + re-solve all logged mistakes (1.5 hrs).",
        ],
        "da": [],
    },
    ("2027-01-13", "Second pass"): {
        "cs": [
            "Core CS Ch 6 Digital Logic (303 Qs): 6.1–6.31 starred Boolean Algebra, K-Map, Combinational/Sequential Circuits, Counters & Number/IEEE-754 Representation PYQs",
            "Core CS Ch 2 CO & Architecture (238 Qs): 2.1–2.20 starred Addressing Modes, ISA, Datapath/Control, Pipelining, Cache Memory, AMAT, Interrupts & DMA PYQs",
            "Session focus: Rapid DL & COA formula review (2 hrs) + timed mixed Ch 6 & Ch 2 PYQ set (2 hrs) + re-solve all logged mistakes (1.5 hrs).",
        ],
        "da": [],
    },
    ("2027-01-14", "Second pass"): {
        "cs": [
            "Core CS Ch 7 Operating System (335 Qs): 7.1–7.27 starred Processes/Fork, Threads, CPU Scheduling, Synchronization/Semaphores, Deadlocks/Banker's, Paging/TLB/Virtual Memory, Page Replacement & Disk/File Systems PYQs",
            "Session focus: Rapid OS formula review (2 hrs) + timed mixed Ch 7 PYQ set (2 hrs) + re-solve all logged OS mistakes (1.5 hrs).",
        ],
        "da": [],
    },
    ("2027-01-15", "Second pass"): {
        "cs": [
            "Core CS Ch 4 Computer Networks (215 Qs): 4.1–4.32 starred Layering/Switching, Error Detection/CRC, CSMA/CD, Sliding Window, IPv4/Subnetting/Fragmentation/NAT, Routing (DV/LS), TCP Flow/Congestion Control, UDP, Sockets, DNS & HTTP PYQs",
            "Discrete Math Ch 3 Mathematical Logic (77 Qs): 3.1 First Order Logic (34), 3.2 Logical Reasoning (3), 3.3 Propositional Logic (40)",
            "Session focus: Rapid CN & Logic formula review (2 hrs) + timed mixed Ch 4 & Logic PYQ set (2 hrs) + re-solve all logged mistakes (1.5 hrs).",
        ],
        "da": [
            "Discrete Math Ch 3 Mathematical Logic (77 Qs): 3.1 First Order Logic (34), 3.2 Logical Reasoning (3), 3.3 Propositional Logic (40)",
            "Session focus: Rapid CN & Logic formula review (2 hrs) + timed mixed Ch 4 & Logic PYQ set (2 hrs) + re-solve all logged mistakes (1.5 hrs).",
        ],
    },
}

print("Loaded UNIT_UPDATES:", len(UNIT_UPDATES))


CUTOFF_KEEP = "2026-10-23"  # Everything <= 2026-10-23 is kept untouched!
WEEK_ANCHOR = date(2026, 10, 20)
WEEK_ANCHOR_NO = 3
TICK = "\u2610"


def week_of(iso: str) -> int:
    y, m, d = map(int, iso.split("-"))
    return WEEK_ANCHOR_NO + (date(y, m, d) - WEEK_ANCHOR).days // 7


def update_workbook_and_daily():
    wb_path = SITE / "workbook_plan.json"
    dr_path = SITE / "daily_resequenced.json"

    plan = json.loads(wb_path.read_text(encoding="utf-8-sig"))
    dump = json.loads(dr_path.read_text(encoding="utf-8"))
    rows = dump["Daily Checklist"]
    header, old = rows[0], rows[1:]

    # 1. Keep all days <= 2026-10-23 completely untouched!
    keep = [r for r in old if r and r[0][:10] <= CUTOFF_KEEP]
    old_by_date = {r[0][:10]: r for r in old if r and r[0]}

    ga_idx = 0
    math_idx = 0
    new_daily = []
    updated_plan = []

    for row in plan:
        dt, day, kind, phase, unit, topic, desc, scope, tier, routine = row
        if dt <= CUTOFF_KEEP:
            # Keep 2026-10-23 untouched in workbook_plan.json as well
            updated_plan.append(row)
            continue

        key = (dt, unit)
        upd = UNIT_UPDATES.get(key)

        if upd is not None:
            cs_items = upd["cs"]
            da_items = upd["da"]
            # Also build updated desc for workbook_plan.json
            parts = []
            both_items = [x for x in cs_items if x in da_items and not x.lower().startswith("session focus:")]
            cs_only = [x for x in cs_items if x not in da_items and not x.lower().startswith("session focus:")]
            da_only = [x for x in da_items if x not in cs_items and not x.lower().startswith("session focus:")]
            focus_items = [x for x in cs_items + da_items if x.lower().startswith("session focus:")]
            if both_items:
                parts.append("Both papers: " + "; ".join(both_items))
            if cs_only:
                parts.append("Computer Science: " + "; ".join(cs_only))
            if da_only:
                parts.append("Data Science and Artificial Intelligence: " + "; ".join(da_only))
            new_desc = " | ".join(parts)
            if focus_items:
                new_desc = (new_desc + "\n" + focus_items[0]).strip()
            row = [dt, day, kind, phase, unit, topic, new_desc, scope, tier, routine]
            updated_plan.append(row)

            label = f"{unit}: {topic}" if unit.startswith("Unit") else topic
            as_text = lambda items: "\n".join("\u2022 " + x for x in items) if items else ""
            cs_col = label if cs_items else ""
            cst_col = as_text(cs_items)
            da_col = label if da_items else ""
            dat_col = as_text(da_items)
        else:
            updated_plan.append(row)
            # Keep existing CS/DA columns from daily_resequenced.json if not in UNIT_UPDATES (e.g. Sunday catch-ups, Mock days)
            orig = old_by_date[dt]
            cs_col, cst_col, da_col, dat_col = orig[4], orig[5], orig[6], orig[7]

        # Build the 6 activity cells with rotated GA & Math book topics on Study/Revision sessions
        orig = old_by_date[dt]
        act_cells = list(orig[8:14])

        if kind == "Study session":
            math_topic = MATH_RECALL_ROTATION[math_idx % len(MATH_RECALL_ROTATION)]
            math_idx += 1
            ga_topic = GA_ROTATION[ga_idx % len(GA_ROTATION)]
            ga_idx += 1

            # Append specific book sections to the Math Recall & General Aptitude cells (idempotently)
            base_math_lines = [ln for ln in act_cells[1].split("\n") if ln.strip() and "Math Recall —" not in ln]
            base_math = "\n".join(base_math_lines).strip()
            act_cells[1] = f"{base_math}\n{TICK} {math_topic}" if base_math else f"{TICK} {math_topic}"

            base_ga_lines = [ln for ln in act_cells[2].split("\n") if ln.strip() and not ln.strip().startswith(f"{TICK} GA ")]
            base_ga = "\n".join(base_ga_lines).strip()
            act_cells[2] = f"{base_ga}\n{TICK} {ga_topic}" if base_ga else f"{TICK} {ga_topic}"
        elif kind == "Revision session":
            ga_topic = GA_ROTATION[ga_idx % len(GA_ROTATION)]
            ga_idx += 1
            base_ga_lines = [ln for ln in act_cells[2].split("\n") if ln.strip() and not ln.strip().startswith(f"{TICK} GA ")]
            base_ga = "\n".join(base_ga_lines).strip()
            act_cells[2] = f"{base_ga}\n{TICK} {ga_topic}" if base_ga else f"{TICK} {ga_topic}"

        new_daily.append([
            f"{dt} 00:00:00",
            day,
            str(week_of(dt)),
            phase,
            cs_col,
            cst_col,
            da_col,
            dat_col,
            *act_cells,
            TICK, TICK, TICK, TICK, TICK,
        ])

    wb_path.write_text(json.dumps(updated_plan, ensure_ascii=False, indent=4), encoding="utf-8")
    dump["Daily Checklist"] = [header] + keep + new_daily
    dr_path.write_text(json.dumps(dump, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Updated daily_resequenced.json: kept {len(keep)} days (<= {CUTOFF_KEEP}), updated {len(new_daily)} days (> {CUTOFF_KEEP}) -> {len(keep) + len(new_daily)} total")


def clean_data(dump: dict) -> dict:
    TIER_RE = re.compile(r"Tier (\d)")
    STOP = {"and", "the", "of", "for", "a", "an", "to", "in", "or", "with", "s"}

    def lines(cell: str):
        if not cell:
            return []
        out = []
        for ln in cell.split("\n"):
            ln = ln.strip().lstrip("☐").strip()
            if ln:
                out.append(ln)
        return out

    def toks(s):
        return {w for w in re.split(r"[^a-z0-9]+", s.lower()) if len(w) > 1 and w not in STOP}

    def sim(a, b):
        A, B = toks(a), toks(b)
        if not A or not B:
            return 0.0
        return len(A & B) / min(len(A), len(B))

    data = {}
    rs_path = SITE / "daily_resequenced.json"
    if rs_path.exists():
        rs = json.loads(rs_path.read_text(encoding="utf-8"))
        if rs.get("Daily Checklist"):
            dump = dict(dump)
            dump["Daily Checklist"] = rs["Daily Checklist"]
    src_days = dump["Daily Checklist"]
    days = []
    for r in src_days[1:]:
        if not r or not r[0]:
            continue
        cs, da = r[4], r[6]
        if cs and da and sim(cs, da) >= 0.5:
            track = "dual"
        elif cs and not da:
            track = "CS"
        elif da and not cs:
            track = "DA"
        elif not cs and not da:
            track = "rest"
        else:
            track = "dual"
        days.append({
            "date": r[0][:10], "day": r[1], "week": int(float(r[2])), "phase": r[3],
            "cs": r[4], "csT": r[5], "da": r[6], "daT": r[7], "track": track,
            "act": [lines(r[8]), lines(r[9]), lines(r[10]), lines(r[11]), lines(r[12]), lines(r[13])],
        })
    data["days"] = days

    ck_path = SITE / "checklist_data.json"
    ck = json.loads(ck_path.read_text(encoding="utf-8")) if ck_path.exists() else None
    if ck:
        data["checklist"] = ck

    topics = []
    for r in dump["Complete Topic Checklist"][1:]:
        if not r or not r[0]:
            continue
        m = TIER_RE.search(r[3])
        topics.append({"exam": "CS" if "Computer Science" in r[0] and "Data" not in r[0] else "DA",
                       "subject": r[1], "topic": r[2], "tier": int(m.group(1)) if m else 3})
    data["topics"] = topics

    key307 = lambda t: t["exam"] + t["subject"] + t["topic"]
    for i, t in enumerate(topics):
        if t["exam"] != "CS":
            continue
        for j, u in enumerate(topics):
            if u["exam"] != "DA" or "twin" in u:
                continue
            if sim(t["topic"], u["topic"]) >= 0.8 and sim(t["subject"], u["subject"]) >= 0.4:
                t["twin"] = key307(u)
                u["twin"] = key307(t)
                break

    link = {}
    if ck:
        def day_lines(s):
            return [x.strip().lstrip("•").strip() for x in s.split("\n") if x.strip().lstrip("•").strip()]

        for d in days:
            ent = {}
            for side, exam in (("cs", "CS"), ("da", "DA")):
                subj = d[side]
                t307, mc = [], []
                for L in day_lines(d[side + "T"]):
                    for t in topics:
                        if t["exam"] != exam or sim(subj, t["subject"]) < 0.4:
                            continue
                        k = key307(t)
                        if sim(L, t["topic"]) >= 0.65 and k not in t307:
                            t307.append(k)
                    if ck:
                        for gi, g in enumerate(ck["groups"]):
                            for ri, r in enumerate(g["rows"]):
                                if [gi, ri] in mc:
                                    continue
                                if sim(L, r["topic"]) >= 0.65 or any(sim(L, s["n"]) >= 0.65 for s in r["subs"]):
                                    mc.append([gi, ri])
                if t307 or mc:
                    ent[side] = {"mc": mc, "t": t307}
            if ent:
                link[d["date"]] = ent
    data["linkMap"] = link

    pyq = []
    for r in dump["Previous-Year Question Tracker"][1:]:
        if not r or not r[0]:
            continue
        pyq.append({"exam": "CS" if "Data" not in r[0] else "DA", "subject": r[1],
                    "p1": lines(r[2]), "p2": lines(r[3]), "err": lines(r[4]),
                    "acc": r[5], "notes": r[6]})
    data["pyq"] = pyq

    mocks = []
    for r in dump["Mock Test Tracker"][1:]:
        if not r or not r[0]:
            continue
        mocks.append({"n": r[0], "date": r[1][:10], "paper": r[2], "type": r[3]})
    data["mocks"] = mocks

    data["time"] = [{"type": r[0], "dur": r[1], "act": r[2], "instr": r[3]}
                    for r in dump["Daily Time Structure"][1:] if r and r[0]]
    data["guide"] = [{"item": r[0], "text": r[1]}
                     for r in dump["How to Use This Checklist"][1:] if r and r[0]]
    return data


def update_index_html():
    """Update DATA inside site/index.html while preserving all existing HTML, CSS, docs, and JS logic."""
    idx_path = SITE / "index.html"
    text = idx_path.read_text(encoding="utf-8")

    # Load base sample_sheet_dump.json and clean_data (which merges daily_resequenced.json and checklist_data.json)
    raw_dump = json.loads((PREP / "sample_sheet_dump.json").read_text(encoding="utf-8"))
    data = clean_data(raw_dump)

    m = re.search(r"^const DATA = (\{.*\});$", text, re.M)
    if not m:
        raise RuntimeError("Could not find `const DATA = {...};` in site/index.html")

    existing_data = json.loads(m.group(1))
    existing_days_keep = {d["date"]: d for d in existing_data.get("days", []) if d["date"] <= CUTOFF_KEEP}
    data["days"] = [existing_days_keep.get(d["date"], d) if d["date"] <= CUTOFF_KEEP else d for d in data["days"]]

    new_data_line = "const DATA = " + json.dumps(data, ensure_ascii=False).replace("</", "<\\/") + ";"
    new_text = text[:m.start()] + new_data_line + text[m.end():]
    idx_path.write_text(new_text, encoding="utf-8")
    print(f"Updated site/index.html ({idx_path.stat().st_size / 1024:.1f} KB, {len(data['days'])} days, {len(data['topics'])} topics, {len(data['checklist']['groups'])} checklist groups)")


if __name__ == "__main__":
    update_workbook_and_daily()
    update_index_html()
