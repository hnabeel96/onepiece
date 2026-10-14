# Why can't Devil Fruit users swim?

| | |
|---|---|
| **Status** | Open: partly confirmed by canon (ch 1069), mechanism is ours |
| **Confidence** | High for the core claim, low for the Void Century extension |
| **Last checked against** | Chapter 1196 |
| **Related** | Seastone, Lineage Factor, Void Century, Ancient Weapons |

## Claim

The sea acts as the world's immune system. A Devil Fruit writes an
"abnormality" into the user's body. Sea energy suppresses abnormalities on
contact, and since the power lives in the user's body, it suppresses the
whole user. More contact means more suppression; willpower can resist at the
margins.

Canon gives half of this: Vegapunk says fruits embody what people wish to
become, and that the sea, "mother of all nature", treats those wishes as
abnormalities (ch 1069). This file adds the mechanism.

## Evidence

### 1. It is an energy drain, not a buoyancy problem
| Ch | What happens | Why it matters |
|---|---|---|
| 336 | Franky swims, proving he is not a user | The effect is fruit-specific |
| 676 | Seastone leaves Luffy barely able to raise his voice, on land | Drain works without any water |
| 926, 935 | Luffy works in seastone cuffs and treats it as training | Strong will pushes back partially |

### 2. The active ingredient is the sea's energy, not wetness
| Ch | What happens | Why it matters |
|---|---|---|
| 169 | Seastone described as a solid form of the sea | Same effect, no water |
| 924 | Seastone originates in Wano, refined only there | Source of concentrated sea energy is local |
| 456 | Salt, carrying the sea's power, ejects Moria's stolen shadows | Even a trace of sea works |
| 240 | Sea clouds (seastone-derived substance) still sink Luffy | Not seawater, same result |
| 1077, 1090 | Bubbles made from sea energy floor S-Snake, contain Seraphim | Sea energy can be engineered |

### 3. It targets the power in the blood, not the act of eating
| Ch | What happens | Why it matters |
|---|---|---|
| 1070 | Seraphim carry synthesized blood from a user's Lineage Factor; none ate a fruit | |
| 1077 | That blood alone makes S-Snake vulnerable to sea energy | **Strongest clue:** the sea reacts to the power itself |

## Mechanism

```
Fruit eaten / power-carrying blood
        └─▶ abnormality written into the body (Lineage Factor)
                └─▶ contact with sea energy (sea, seastone, salt, sea cloud)
                        └─▶ suppression ∝ contact  ──▶  loss of strength, can't swim
                                └─ resisted partially by willpower
```

## Competing explanations

| Theory | Fits? | Problem |
|---|---|---|
| Body becomes too dense to float | No | Seastone drains users on dry land |
| Unexplained curse | Partly | Explains nothing about seastone, salt or synthetic blood |
| **Sea as immune system** | **Yes** | One edge case, below |

## Weak points

- **Fresh water.** Robin is weakened half-submerged in a bath (ch 407),
  probably not seawater. Either still water counts because all water traces
  back to the sea, or there is a size threshold. Weakest link in the theory.
- **Fish-Man users.** Vander Decken is a Fish-Man with a fruit (ch 637).
  How exactly he is affected is worth checking.

## Speculative extension: the sinking of the world

During the Void Century the sea rose about 200 m and sank the ancient world
(ch 1115); Vegapunk speaks of world-sinking weapons (ch 1116); Elbaph's
history also sank (ch 1154). If sea energy suppresses fruit powers, sinking
the world spread an anti-fruit field over almost all of it. The rise may
have been a deliberate check on fruit-powered rulers, not only a disaster.

## Tests

- **Would kill it:** a user drained by rain or a splash; a material with no
  link to the sea that blocks fruit powers.
- **Would confirm it:** Imu or the Gorosei shown to be sea-weak; the ancient
  weapons tied to sea level.
- **Open:** whether Nika (the "freest wish") or awakened fruits resist the sea
  better than others.

## Database queries used

```sql
-- every chapter where seastone, salt or the sea interacts with fruit powers
SELECT number, title FROM chapters
WHERE long_summary LIKE '%Seastone%' OR long_summary LIKE '%energy of the sea%';

-- SBS entries on Devil Fruits (read them on the wiki)
SELECT volume, chapter, page FROM sbs_index
WHERE topics LIKE '%"Devil Fruit%' OR topics LIKE '%Seastone%';
```
