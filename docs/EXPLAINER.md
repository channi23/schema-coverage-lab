# What I Built and How to Understand It

I built a tool to answer this question:

> **Have my test inputs demonstrated how each selected rule can independently change a JSON Schema decision?**

To explain that question, I first separate **validation** from **test coverage**.

- **Validation** asks: “Does this particular input pass the rules?”
- **Test coverage** asks: “What has my collection of test inputs actually demonstrated about those rules?”

A collection can contain passing and failing inputs while still leaving an important rule unexplained.

## 1. The crux of the research

**I use set theory to describe which inputs satisfy each selected schema rule, then use MC/DC-style comparisons to demonstrate whether each rule can independently change a decision.**

The connection has four parts:

| Part | Its job |
|---|---|
| Schema | Supplies the rules to examine. |
| Set theory | Describes the groups of inputs that satisfy or fail those rules. |
| MC/DC-style coverage | Specifies the two-input comparisons that demonstrate independent influence. |
| My tool | Searches actual candidate inputs for those comparisons and retains their evidence. |

The set model describes the regions I need evidence from. The implemented tool evaluates a finite collection of candidate inputs and finds qualifying pairs from their observed rule outcomes. It does not calculate every possible JSON input.

For example, if `17` should be rejected, an automated check of `17` **passes when the tool correctly rejects it**. A rejected input and a failed automated test are different things.

## 2. How sets describe accepted inputs

Consider this example:

```json
{
  "anyOf": [
    { "const": "red" },
    { "const": "blue" }
  ]
}
```

`const` means "equal this exact value." `anyOf` means "at least one rule must pass." This example accepts `"red"` or `"blue"` and rejects `"green"`.

A **set** is a collection of values.

Let:

$$
A = \{\text{"red"}\}
$$

This is the set of values accepted by the first rule.

Let:

$$
B = \{\text{"blue"}\}
$$

This is the set accepted by the second rule.

The **union** of two sets contains everything belonging to either set:

$$
A \cup B = \{\text{"red"},\text{"blue"}\}
$$

Read $\cup$ as **“union”** or **“in either collection.”**

That is exactly what `anyOf` does here.

Now imagine replacing `anyOf` with `allOf`:

```json
{
  "allOf": [
    { "const": "red" },
    { "const": "blue" }
  ]
}
```

`allOf` means **every rule must pass**. In set notation, this is an **intersection**:

$$
A \cap B = \varnothing
$$

Read $\cap$ as **“intersection”** or **“in both collections.”**

Read $\varnothing$ as **“the empty set.”**

No single value can equal both `"red"` and `"blue"`, so this second schema accepts nothing.

Sets give me a precise way to describe what a schema accepts. They do not, by themselves, tell me whether my tests are sufficient.

## 3. What does MC/DC add?

**MC/DC** means **Modified Condition/Decision Coverage**.

Its central idea is:

> Demonstrate that changing one selected condition’s outcome can change the decision, while the other selected conditions’ outcomes stay the same.

A **condition** is one of the selected yes/no checks. In my first schema:

- Condition A: “Does the input equal `"red"`?”
- Condition B: “Does the input equal `"blue"`?”

I keep the schema unchanged and try different inputs:

| Input | A: equals `"red"`? | B: equals `"blue"`? | Final decision |
|---|---:|---:|---|
| `"red"` | Yes | No | Pass |
| `"blue"` | No | Yes | Pass |
| `"green"` | No | No | Fail |

Compare `"red"` with `"green"`:

- A changes from Yes to No.
- B remains No.
- The final decision changes from Pass to Fail.

These two inputs demonstrate A’s **independent influence**.

Now compare `"blue"` with `"green"`:

- B changes from Yes to No.
- A remains No.
- The decision changes from Pass to Fail.

That demonstrates B’s independent influence.

Each useful comparison is a **witness pair**: two concrete inputs that provide the required evidence.

Each selected condition creates an **independence obligation**: a check I must demonstrate before claiming that condition is covered.

For this example, three inputs satisfy two obligations.

Importantly, “independent” refers to the selected rule outcomes. It does not mean that only one character or one data field must change.

## 4. Why do I need all three inputs?

Suppose I tested only `"red"` and `"blue"`.

Both pass. I have not shown either rule changing the final decision.

Suppose I tested only `"red"` and `"green"`.

I have a passing input and a failing input, and I have demonstrated A’s influence. But B never passes, so its influence remains undemonstrated.

Adding `"blue"` completes the evidence.

This distinction is what I call **semantic independence coverage**:

- **Semantic** means I examine the meaning and outcomes of schema rules.
- **Independence** means the selected rule changes the decision while the other selected outcomes stay fixed.
- **Coverage** records which required demonstrations I have obtained.

It is different from measuring which lines of the validator’s program code executed.

## 5. How are coverage checks classified?

The same inputs can provide different kinds of evidence:

| Classification | What it asks |
|---|---|
| **Decision coverage** | Did the selected decision produce both Pass and Fail? |
| **Condition coverage** | Did each selected yes/no rule have both a Yes and a No outcome? |
| **Independence coverage** | Did a pair demonstrate one selected rule changing the decision while the other selected rule outcomes stayed fixed? |

In the color example, `"red"` and `"blue"` give both rules Yes and No outcomes, but both inputs pass. Adding `"green"` supplies a failing decision and the two required independence pairs.

A **test case** is an input with its expected result. A **coverage check** asks what a collection of those cases demonstrates. The **105 regression tests** mentioned later are automated checks of my tool's behavior, rather than 105 schema inputs or 105 schemas.

## 6. Exactly where sets and MC/DC meet

Consider a schema accepting whole-number ages from 18 through 60:

```json
{
  "type": "integer",
  "allOf": [
    { "minimum": 18 },
    { "maximum": 60 }
  ]
}
```

Suppose I consider these three candidate inputs:

```text
17, 30, 61
```

Among those inputs, let A contain the values satisfying the minimum rule and B the values satisfying the maximum rule:

$$
A = \{30, 61\}, \qquad B = \{17, 30\}
$$

The schema requires both rules to pass:

$$
A \cap B = \{30\}
$$

The other regions identify inputs failing just one selected rule:

$$
B \setminus A = \{17\}, \qquad A \setminus B = \{61\}
$$

Read $B \setminus A$ as "in B, but not in A."

| Region | Input | Meaning |
|---|---:|---|
| Both A and B | `30` | Both selected rules pass. |
| B, but not A | `17` | Only the minimum rule fails. |
| A, but not B | `61` | Only the maximum rule fails. |

MC/DC now tells me which regions to compare:

- **`30` with `17`:** the minimum rule changes, the maximum stays satisfied, and acceptance changes. This demonstrates the minimum rule's influence.
- **`30` with `61`:** the maximum rule changes, the minimum stays satisfied, and acceptance changes. This demonstrates the maximum rule's influence.

**These particular sets contain only the three considered inputs. They are not a list of every possible age.** The selected conditions here are the two children of `allOf`; the integer requirement also affects validation but is not an additional independence condition in this example's catalog.

This is the integration: **sets describe the input regions, MC/DC defines the useful comparisons between them, and the tool finds and checks concrete inputs for those comparisons.**

## 7. What does the tool output mean?

For the three-input example, a simplified expected report is:

```json
{
  "analysis_status": "supported",
  "counts": {
    "covered": 2,
    "unknown": 0
  }
}
```

Read it as:

- `supported`: this schema uses features my prototype can analyze.
- `covered: 2`: both selected conditions have valid witness pairs.
- `unknown: 0`: neither of those two obligations remains unresolved.

**Two covered obligations does not mean two test inputs.** This example uses three inputs.

The real report also records the inputs, their condition outcomes, the pairs used, and the checks performed.

## 8. What did I implement?

My tool performs the following steps:

1. **Generate candidate inputs.** These are possible test values, such as exact allowed values and values near numeric limits.
2. **Build a bounded candidate pool.** This is a finite collection with an explicit size limit. It does not contain every possible JSON value.
3. **Analyze outcomes and find witness pairs.** It identifies which independence obligations the pool demonstrates.
4. **Reduce the test suite.** A test suite is the selected collection of test inputs. Reduction tries to retain the demonstrated obligations using fewer distinct inputs.
5. **Independently replay the evidence.** A separate validator checks the recorded outcomes, and the tool recomputes the pair evidence.

**Pair-aware reduction** means keeping both inputs needed for a witness pair. Keeping only one endpoint does not preserve the demonstration.

**Reproducible** means I retain the source, inputs, settings, commands, and results so someone else can repeat and inspect the process.

## 9. What reduction means in the simplest terms

**Reduction means removing inputs that repeat evidence already supplied by other inputs, while keeping the demonstrated checks I chose to preserve.**

For the age schema above, imagine starting with six inputs:

```text
17, 20, 30, 40, 50, 61
```

For the two selected rule-influence checks, I can keep just:

```text
17, 30, 61
```

- Comparing `17` with `30` demonstrates the minimum rule's influence.
- Comparing `30` with `61` demonstrates the maximum rule's influence.

The additional values `20`, `40`, and `50` do not add another independent-influence demonstration for those two selected rules. The smaller collection retains that particular evidence.

This does **not** mean removed inputs are useless for finding other mistakes. The next example explains why coverage preservation is a narrower guarantee than detecting every bug. The greedy reduction algorithm also does not promise the smallest possible suite.

## 10. Does complete coverage mean I will find every mistake?

No. Consider:

```json
{
  "allOf": [
    { "type": "integer" },
    { "minimum": 18 }
  ]
}
```

This accepts whole numbers starting at 18.

The inputs `19`, `17`, and `"x"` can demonstrate both selected conditions:

- `19` passes.
- `17` fails the minimum.
- `"x"` fails the integer requirement. The numeric minimum rule itself does not reject text, because it applies only to numbers.

Now deliberately change the minimum from 18 to 19.

All three inputs produce the same final results as before:

```text
19  → Still passes
17  → Still fails
"x" → Still fails
```

The changed rule is exposed by testing **18**, which now incorrectly fails.

This deliberate rule change is a **mutation**. **Mutation detection** asks whether a test suite notices that change.

The example explains why independence coverage can be complete for the selected conditions while still missing an important boundary mistake.

My experiments found this distinction in practice: higher independence coverage did not consistently produce better mutation detection.

## 11. What did the recorded study achieve?

- **105 regression tests passed.** These are automated checks of intended tool behavior, including checks that previously working behavior remains correct.
- I studied **32 selected schemas**.
- I recorded **2,304 equal-budget comparisons**. “Equal budget” means methods could select the same number of distinct inputs. It does not mean their preparation time or computing costs were identical.
- On **21 schemas with witnessed independence targets**, reduction selected **64 tests from 451 candidate inputs**, preserving all **50 witnessed obligations**.

Those 50 obligations are required demonstrations across the selected decisions. They are not 50 schemas or necessarily 50 different witness pairs. One input can participate in several pairs.

The 451-to-64 reduction was performed separately for each of the 21 schemas and then added together:

| Across the 21 schema-specific collections | Before reduction | After reduction |
|---|---:|---:|
| Test inputs | 451 | 64 |
| Demonstrated selected rule-influence checks | 50 | The same 50 |

These are totals across separate schema-specific collections. This is not one 64-input collection guaranteed to work for every schema. An input value used against two different schemas is counted in each schema's collection.

**The research outcome is a working, checked method for collecting and preserving this selected form of evidence. It does not establish a new universal mathematical principle or generally better bug detection.**

These results support the bounded tool and recorded study. They do not establish full JSON Schema support or prove that this method finds more real bugs than alternatives.

Also, **“I did not find a pair in this finite pool” is different from “no pair can exist anywhere.”** The tool keeps that uncertainty visible.

## 12. Where should I read next?

The **repository**, or **repo**, is the shared project folder on GitHub containing my code, documents, inputs, and results.

| Your question | Where to read |
|---|---|
| “How do I run the tool and interpret its output?” | [Usage guide](https://github.com/channi23/schema-coverage-lab/blob/main/docs/USAGE.md) |
| “How are the parts of the tool connected?” | [Architecture](https://github.com/channi23/schema-coverage-lab/blob/main/docs/ARCHITECTURE.md) |
| “What are the precise mathematical definitions?” | [Set-theoretic model](https://github.com/channi23/schema-coverage-lab/blob/main/docs/research/03-set-model.md) |
| “What did the experiments measure?” | [Experiment summary](https://github.com/channi23/schema-coverage-lab/blob/main/results/milestone-2/summary.json) |
| “What did I actually do and verify?” | [Evidence log](https://github.com/channi23/schema-coverage-lab/blob/main/docs/EVIDENCE_LOG.md) |

**My achievement is a working way to show and independently check the evidence behind selected JSON Schema coverage claims. The evidence and its limits matter more than the percentage alone.**
