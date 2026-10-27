# Was Nefertari D. Lili the first Nidhöggr?

| | |
|---|---|
| **Status** | Open |
| **Confidence** | Low–medium (core) / low (Ragnir, Vivi extensions) |
| **Last checked against** | Chapter 1195 |
| **Related** | Ryu Ryu no Mi Model: Nidhöggr, Ragnir / Ratatoskr, Empty Throne, Poneglyphs, Imu, Vivi |

## Claim

The "Warrior God" who used the Nidhöggr fruit and Ragnir before Loki was
Nefertari D. Lili. She fought on Imu's side against the Sun God (Joy Boy),
then turned on Imu, used the dragon to scatter the Poneglyphs, and hid out
on Elbaph, where the fruit stayed for 800 years under Ragnir's guard.

## Evidence

### 1. The old Nidhöggr switched sides
| Ch | What happens | Why it matters |
|---|---|---|
| 1175 | Legend: a "Warrior God" wielded Ragnir and the fruit and fought the Sun God | The first user fought *against* Joy Boy |
| 1182 | Imu calls Nidhöggr a "traitor" | You only betray a side you were on |
| 1183 | Imu says Ragnir waited for someone who could fight back against *him* | Ragnir's old master ended up fighting Imu |
| 1181 | Imu smiles: Nidhöggr "has truly returned" | Imu knew the old user personally |

### 2. Lili is the one known defector from the First Twenty
| Ch | What happens | Why it matters |
|---|---|---|
| 1084 | Lili never went to Mary Geoise; only 19 weapons before the Empty Throne | Broke from the Twenty |
| 1085 | Imu blames Lili's "mistake" for the Poneglyphs reaching the world | Imu treats her as the betrayer |
| 1085 | Lili's full name carries "D.", the name of Imu's opposers | A D. inside the founding alliance |
| 1084 | Cobra: Lili never made it back home; her younger brother ruled | She vanished somewhere |

### 3. Lili and the fruit end up in the same place
| Ch | What happens | Why it matters |
|---|---|---|
| 1195 | Biblo: a human named Lili once lived on Elbaph | Where she went |
| 1175 | Imu is furious the fruit "was in Elbaph all along" | Someone hid it; the defector knew where |
| 1193 | Biblo's chest holds letters and tools passed down since his grandfather's time | Lili is known through letters |

## Mechanism

```
Void Century: Lili (hidden D.) fights the Sun God as Nidhöggr, on Imu's side
   └─▶ turns on Imu ("traitor")
         └─▶ flies the largest dragon alive across the world, scattering Poneglyphs
               └─▶ settles on Elbaph, dies there
                     └─▶ Ratatoskr moves into Ragnir, guards the fruit, waits for
                         someone who can fight Imu (Loki, ch 1170)
```

Why a dragon matters: getting indestructible stone blocks to places like
Zunesha's back across the whole world in one lifetime is far easier for a
flier than for ships.

## Extensions (bigger leaps)

- **Ragnir is the missing 20th weapon.** Imu summons the Twenty's weapons
  from before the Empty Throne through Omen (ch 1189). The one weapon never
  laid there would be the one that picks its own master and hates Imu.
- **Imu wants Vivi because she looks like Lili.** Imu sees Joy Boy in
  Luffy's face (ch 1188) and recognises Shuri on sight. In ch 1179 he
  complains about Joy Boy and Davy Jones, then says all he wants is Vivi.
  Pattern: Nika→Luffy, Davy Jones→Rocks, Lili→Vivi.
- **Ratatoskr as messenger.** The Norse squirrel carries messages up and
  down the world tree; Lili is remembered through letters.

## Competing explanations

| Theory | Fits? | Problem |
|---|---|---|
| Warrior God was an ancient giant | Yes | Doesn't explain "traitor" or why Imu cares where the fruit was |
| "Traitor" refers to the dragon/fruit lineage, not a person | Partly | Imu reacts to Loki as a returning individual |
| **Lili was the Warrior God** | **Yes** | Size, below |

## Weak points

- **Size.** Ragnir is too heavy for Hajrudin to lift (ch 1143) and the
  dragon scales with its user (ch 1175). A giant is the simpler reading.
- **Lili's stay on Elbaph** could have been brief or late, unrelated to the
  fruit.
- **Weapon names** mix world myths (Gram, Longinus, Xingtian, Fragarach), so
  a Norse hammer says nothing about Egypt either way.

## Tests

- **Would kill it:** the chest or Imu names a giant (or anyone else) as the
  old Nidhöggr; Lili's letters show she arrived after the fruit was hidden.
- **Would confirm it:** Lili's letters mention the dragon, Ratatoskr or
  Ragnir; Imu links Vivi's face to Lili; a 20th weapon slot is shown.
- **Open:** what tools are in Biblo's chest (ch 1196+).

## Database queries used

```sql
-- every chapter mentioning the key names
SELECT number, title FROM chapters
WHERE long_summary LIKE '%Nidh%' OR long_summary LIKE '%Ragnir%'
   OR long_summary LIKE '%Lili %' OR long_summary LIKE '%Empty Throne%';

-- Imu's lines about Vivi, Joy Boy and Davy Jones
SELECT number, title FROM chapters
WHERE long_summary LIKE '%Davy Jones%' AND number >= 1150;
```
