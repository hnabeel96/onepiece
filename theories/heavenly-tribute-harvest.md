# Is the Heavenly Tribute a way to harvest people?

| | |
|---|---|
| **Status** | Open |
| **Confidence** | Medium (pattern) / low (Esperia smog planted) / low (Arabasta aimed at Vivi) |
| **Last checked against** | Chapter 1195 |
| **Related** | Heavenly Tribute, Esperia, Shuri / Gunko, Manmayer Gurou, Bipolar Irises, Arabasta, Dance Powder, Vivi |

## Claim

The Heavenly Tribute isn't really about money. It turns a ruined country
into people the World Government wants: wreck the economy, wait for the
payment to fail, then accept a "compromise" paid in people. Esperia's smog
was planted to collect Shuri; Arabasta's drought was the same trap aimed
at Vivi.

## Evidence

### 1. Failed tribute gets paid in people
| Ch | What happens | Why it matters |
|---|---|---|
| 1049 | Vodka Kingdom can't pay and hands young Kaidou to the Government | People as payment |
| 1097 | Sorbet's king cuts off his poor to lower the population-based bill | The tribute shapes who counts as a citizen |
| 762, 765 | Government knew Amber Lead was poison and kept it quiet for money | Willing to let a disaster run |
| 1185 | Esperia fails the tribute; Government demands 1,000 slaves | The "compromise" |
| 1186 | Shuri: the real demand was her | The slaves were a cover |

### 2. Esperia's smog looks targeted
| Ch | What happens | Why it matters |
|---|---|---|
| 1185 | Mist arrives when Shuri is 15, lasts half a year, turns to smog | Timing |
| 1185 | It corrodes instruments and stops people singing | Hits exactly what a music kingdom earns from |
| 1186 | Gurou: he wouldn't normally come for a child, but bipolar irises are rare and valued by Imu | Motive |
| 1186 | Imu is present, possessing Mars | Imu only leaves for things he wants |

### 3. Arabasta fits the same shape
| Ch | What happens | Why it matters |
|---|---|---|
| 161 | Three years of drought from Dance Powder | Kills what the country runs on |
| — | Crocodile, behind it, was a Government Warlord | Government-adjacent |
| 908 | Imu carries Vivi's picture to the Empty Throne | Imu wants her specifically |
| 1179 | Imu: all he wants is Vivi | Same |

## Mechanism

```
Imu wants a person (eyes, bloodline, children)
   └─▶ their country is hit by a disaster that targets its income
         └─▶ it can't pay the Heavenly Tribute
               └─▶ Government offers a "compromise" paid in people
                     └─▶ the person Imu wanted is inside that payment
```

## Competing explanations

| Theory | Fits? | Problem |
|---|---|---|
| Tribute is just greed; Esperia was bad luck the Government exploited | Yes | Doesn't explain the timing with Gurou's visit |
| **Disasters are engineered to force payment in people** | **Yes** | No direct proof of who made the mist |

## Weak points

- Crocodile wanted Pluton for himself, not to deliver Vivi; at best he was
  a tool.
- Nothing shows who or what made the mist. Brook's past is 70+ years ago,
  so not Vegapunk; a fruit or older Government science.
- Esperia could be opportunistic: they saw the debt and used it.

## Tests

- **Would kill it:** the smog is natural or tied to a cause unrelated to
  the Government.
- **Would confirm it:** the mist linked to a Government agent or Knight's
  power; Gunko remembers being told about it; Dance Powder traced to
  Mary Geoise.
- **Open:** what Shuri's eyes can "awaken" (ch 1186); whether Imu wants
  Vivi for a trait as well.

## Database queries used

```sql
-- every mention of the tribute
SELECT number, title FROM chapters WHERE long_summary LIKE '%Heavenly Tribute%';

-- Esperia flashback
SELECT number, title FROM chapters WHERE number BETWEEN 1183 AND 1186;

-- Imu and Vivi
SELECT number, title FROM chapters
WHERE long_summary LIKE '%Vivi%' AND long_summary LIKE '%Imu%';
```
