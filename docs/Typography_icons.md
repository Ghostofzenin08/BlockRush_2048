# Typography & Icons Strategy (Typography_icons.md)

## 1. Typography Hierarchy & Font Families
The BlockRush UI specifies **`Instrument Sans`** and **`Inria Sans`** as primary Google Font families.

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inria+Sans:wght@400;700&family=Instrument+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
```

---

## 2. Typography Token Scale

| Level | Font Family | Size | Weight | Target Element |
| :--- | :--- | :--- | :--- | :--- |
| **Hero Title** | `Instrument Sans` | 35px | 700 (Bold) | Main Menu "BlockRush" Title |
| **Screen Title** | `Instrument Sans` | 32px | 700 (Bold) | Playground / Support / T&C Headings |
| **Section Heading** | `Instrument Sans` | 22px - 24px | 700 (Bold) | Support Document Headings, Math Banner |
| **Button Label** | `Instrument Sans` | 18px - 20px | 500 / 600 | Menu Dark Pill Buttons, Start Challenge |
| **Body Text** | `Instrument Sans` | 15px - 16px | 400 (Regular) | Support paragraphs, T&C legal text |
| **Tile Numbers** | `Instrument Sans` | 24px - 42px | 800 (ExtraBold)| 2048 Game Board Block Numbers |

---

## 3. Global CSS Typography Rule
```css
* {
  font-family: 'Instrument Sans', 'Inria Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}
```

---

## 4. UI Icons System
UI icons rely on inline SVGs and Material Symbols:
- **Navigation Controls**: Left back arrow (`←`), Exit (`🚪`), Pause (`⏸`), Audio (`🔊`), Theme (`🌙` / `☀️`).
- **Mode Icons**: Beginner Shield (`🛡️`), Pro Lightning (`⚡`), Master Crown (`👑`), Math Controller (`🎮`).
- **Status Icons**: Challenge checkmark (`✓`), Star ratings (`★`).
