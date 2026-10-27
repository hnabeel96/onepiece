# Were the Empty Throne weapons the first Covenant?

| | |
|---|---|
| **Status** | Open |
| **Confidence** | Low–medium (core) / low (extensions) |
| **Last checked against** | Chapter 1195 |
| **Related** | Empty Throne, First Twenty weapons, Covenant, Omen, Gram, Longinus, Honebami Toshiro, Nefertari D. Lili, Vivi |

## Claim

The official story is that the 19 kings laid their weapons before the
Empty Throne as a vow that nobody would ever sit on it. Instead, handing
the weapons to the throne *was* the contract: the kings gave Imu their
power in exchange for ruling forever. Every World Noble family inherits a
Covenant through that weapon, and Imu can use any of them through Omen.

## Evidence

| Ch | What happens | Why it matters |
|---|---|---|
| 1084 | Cobra: weapons laid before the Empty Throne as a vow; only 19 because Lili stayed in Arabasta | The official story |
| 1084 | Imu sits on the Empty Throne | The vow was fake from the start |
| 1181 | Imu: "when someone chooses servitude out of self-interest, it leads to Covenants" | The Twenty traded loyalty for being World Nobles forever: this definition exactly |
| 1189 | Imu summons the Twenty's weapons through Omen and gives Gram and Longinus to Knights | He controls them like Covenant holders |
| 1189 | Sommers wields the Shepherd family's Gram "just like Imu can" through Omen | The weapon answers to Imu, not its family |
| 1193 | Gram turns its wielder's wrath into power | Weapons feed on the same vices as Imu's power |
| 1167 | Covenant tiers: Shallow, Depths, Abyssal | Individual Covenants follow the same deal |
| 1085 | Lili, the one who laid no weapon, carries the D. | The family that didn't sign is the opposing one |

## Mechanism

```
800 years ago: 19 kings lay their weapons at the throne
   └─▶ "servitude out of self-interest" → the first Covenant
         └─▶ each weapon holds its family's pledge
               └─▶ Imu pulls any of them out through Omen
                     └─▶ Knights' Shallow/Depths/Abyssal Covenants are
                         the same deal, offered to individuals
```

## Extensions

- **Breaking a weapon breaks the pledge.** Destroying Gram would weaken
  the Shepherd family's hold; a reason Imu keeps them in reserve.
- **Nefertari is the free bloodline.** No weapon, no Covenant: another
  reason Imu wants Vivi (ch 1179).
- **Zoro takes Honebami Toshiro.** A Japanese blade that just cost Gaban
  his arm (ch 1190); Zoro collects cursed legendary swords.

## Competing explanations

| Theory | Fits? | Problem |
|---|---|---|
| Omen lets Imu wield any weapon; the throne is just symbolism | Yes | Doesn't explain why these specific weapons are kept and lent out |
| Weapons are trophies Imu took from the kings | Partly | Cobra's account says the kings laid them down themselves |
| **Laying them down was the first Covenant** | **Yes** | No World Noble shown controlled by inheritance |

## Weak points

- Omen is "a power that resides in all things" (ch 1181), so Imu may be
  able to wield any weapon at all.
- World Nobles act freely; no inherited control has been shown.
- Shuri's father couldn't "awaken" something (ch 1186), hinting bloodline
  powers come from elsewhere.

## Tests

- **Would kill it:** Imu summons a weapon that never sat at the throne just
  as easily; the weapons shown to be ordinary relics.
- **Would confirm it:** a weapon breaks and its family reacts; a World
  Noble shown with a Covenant mark from birth; Vivi resists Imu's control.
- **Watch:** Gram and Longinus are with Sommers and Killingham; Zoro has
  just beaten Sommers (ch 1195).

## Database queries used

```sql
-- the Empty Throne and its weapons
SELECT number, title FROM chapters WHERE long_summary LIKE '%Empty Throne%';

-- Covenant rules and tiers
SELECT number, title FROM chapters WHERE long_summary LIKE '%Covenant%';
```
