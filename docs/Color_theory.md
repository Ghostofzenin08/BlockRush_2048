# Color Theory & Palette Strategy (Color_theory.md)

## 1. Design System & Palette Hierarchy
The visual color strategy for BlockRush is built around a vibrant 3D gaming palette derived from Figma node [`594-2`](https://www.figma.com/design/I0MbnU8Xks35mLwtkTcAKI/Projects?node-id=594-2). The system follows the **60-30-10 Rule** for visual balance.

```
60% Dominant Base (#000000 Dark / #FFFFFF Light)
└── 30% Structural Components (#1d1e2c Dark Card & Button Base)
    └── 10% Vibrant Accents (#ffbd00 Yellow, #9e0059 Pink, #04c7fd Cyan, #ff5400 Orange)
```

---

## 2. Color Palette Token Specification

| Color Token | Hex Code | Purpose / Component | WCAG Contrast |
| :--- | :--- | :--- | :--- |
| **Dark Background** | `#000000` | Deep canvas background | AAA (on white text) |
| **Light Background** | `#ffffff` | Light mode canvas background | AAA (on dark text) |
| **Card & Button Base** | `#1d1e2c` | Dark rounded pill buttons, cards, support containers | AAA |
| **Accent Yellow** | `#ffbd00` | Tile 2, Tile 32, Active support tab glow, Victory stars | AAA |
| **Accent Pink** | `#9e0059` | Tile 1024, Tile 2048, Primary "Rush the level" button | AAA |
| **Accent Orange** | `#ff5400` | Tile 4, Tile 256, Master mode badge | AAA |
| **Accent Cyan** | `#04c7fd` | Pro mode title, Document heading border accent | AAA |
| **Accent Purple** | `#390099` | Tile 16, Brand sub-logo block | AAA |

---

## 3. Dark & Light Theme Override System

```css
[data-theme="light"] {
  --bg-color: #ffffff;
  --text-color: #000000;
  --card-bg: #1d1e2c; /* Buttons remain dark pills in light mode per Figma design */
  --border-color: rgba(0, 0, 0, 0.1);
}

[data-theme="light"] .support-content,
[data-theme="light"] .pg-card {
  background: #ffffff;
  border: 1.5px solid #e0e0e0;
  color: #000000;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
}
```
