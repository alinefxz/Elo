# elo_front/static/css/elo.css: código e explicação

[Voltar ao índice](../LEIA_PRIMEIRO.md) · [Guia dos fluxos](../GUIA_ELO.md) · [Referência de chamadas](../REFERENCIA_CODIGO.md)

**Responsabilidade:** Regras visuais de seletores, componentes e tamanhos de tela.

**Arquivo original:** [elo_front/static/css/elo.css](<C:/Users/lb119/Elo/elo_front/static/css/elo.css>). As linhas referem-se à cópia desta data.

## Código integral

``````css
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,600;0,700;1,600;1,700&display=swap');

:root {
    --red: #bd1026;
    --red-dark: #a20d20;
    --red-light: #d64a59;
    --black: #17181b;
    --text: #37383d;
    --muted: #6f7076;
    --line: #e8e8e8;
    --soft: #f7f7f7;
    --white: #ffffff;
    --success: #177245;
    --warning: #bd1026;
    --shadow: 0 16px 40px rgba(20, 20, 20, .06);
}

* {
    box-sizing: border-box;
}

html {
    scroll-behavior: smooth;
}

body {
    margin: 0;
    color: var(--text);
    background: var(--white);
    font-family: "DM Sans", Arial, sans-serif;
    font-size: 16px;
    line-height: 1.6;
}

a {
    color: inherit;
    text-decoration: none;
}

button,
input,
select,
textarea {
    font: inherit;
}

.container {
    width: min(1160px, calc(100% - 80px));
    margin: 0 auto;
}

/* HEADER */

.site-header {
    height: 112px;
    background: var(--white);
    border-bottom: 1px solid var(--line);
    display: flex;
    align-items: center;
}

.header-inner {
    width: min(1160px, calc(100% - 80px));
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 40px;
}

.brand {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    color: var(--red);
    flex-shrink: 0;
}

.brand-mark {
    display: inline-block;
    flex-shrink: 0;
}

.site-header .brand-mark {
    width: 42px;
    height: 42px;
    background: url("logo-gota.png") center / contain no-repeat;
}

.brand-name {
    font-family: "Playfair Display", Georgia, serif;
    font-size: 36px;
    font-style: italic;
    font-weight: 700;
    line-height: 1;
    letter-spacing: 0;
}

.main-nav {
    display: flex;
    align-items: center;
    gap: 46px;
}

.main-nav > a {
    min-height: 44px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 15px;
    font-weight: 500;
    line-height: 1.2;
    text-align: center;
    color: #292a2d;
    transition: color .2s ease;
}

.main-nav > a:hover {
    color: var(--red);
}

.main-nav .nav-cta {
    color: var(--white);
    background: var(--red);
    border-radius: 5px;
    padding: 12px 25px;
    font-weight: 700;
}

.main-nav .nav-cta:hover {
    color: var(--white);
    background: var(--red-dark);
}

.menu-toggle {
    display: none;
    width: 44px;
    height: 44px;
    border: 0;
    background: transparent;
    cursor: pointer;
}

.menu-toggle span {
    display: block;
    width: 25px;
    height: 2px;
    background: var(--black);
    margin: 5px auto;
}

/* HERO */

.hero {
    min-height: 594px;
    background: var(--white);
    display: flex;
    align-items: center;
}

.hero-inner {
    padding: 78px 0 76px;
}

.hero-copy {
    max-width: 610px;
}

.eyebrow {
    margin: 0 0 22px;
    color: var(--red);
    font-size: 13px;
    line-height: 1.2;
    letter-spacing: 1.7px;
    font-weight: 700;
}

.hero h1 {
    margin: 0;
    color: var(--black);
    font-family: "Playfair Display", Georgia, serif;
    font-size: clamp(58px, 6.1vw, 82px);
    line-height: .99;
    letter-spacing: -3px;
    font-weight: 700;
}

.hero h1 em {
    color: var(--red);
    font-weight: 600;
}

.hero-text {
    max-width: 570px;
    margin: 32px 0 44px;
    color: #55565b;
    font-size: 17px;
    line-height: 1.7;
}

.hero-actions {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 25px;
}

.button {
    min-height: 50px;
    padding: 13px 26px;
    border-radius: 5px;
    display: inline-flex;
    justify-content: center;
    align-items: center;
    border: 1px solid transparent;
    font-weight: 700;
    font-size: 15px;
    line-height: 1.2;
    text-align: center;
    transition: .2s ease;
}

.button-primary {
    color: var(--white);
    background: var(--red);
}

.button-primary:hover {
    background: var(--red-dark);
    transform: translateY(-1px);
}

.button-outline {
    color: var(--red);
    background: transparent;
    border-color: var(--red);
}

.button-outline:hover {
    background: #fff5f6;
}

.button-small {
    min-width: 260px;
}

/* ESTOQUE */

.stock-section {
    background: #f6f6f6;
    padding: 64px 0 58px;
}

.section-heading h2,
.info-section h2,
.faq-section h2 {
    margin: 0;
    color: var(--black);
    font-family: "Playfair Display", Georgia, serif;
    font-size: 31px;
    line-height: 1.15;
    letter-spacing: -.5px;
}

.section-heading p {
    max-width: 640px;
    margin: 8px auto 0;
    color: #4c4d51;
    font-size: 16px;
    text-align: center;
}

.section-heading {
    text-align: center;
}

.blood-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 58px 40px;
    margin: 42px 35px 48px;
}

.blood-card {
    min-height: 112px;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.blood-type {
    color: #202125;
    font-size: 31px;
    line-height: 1;
    font-weight: 500;
}

.blood-line {
    width: 86px;
    height: 2px;
    background: var(--red-light);
    margin: 20px 0 11px;
}

.blood-status {
    font-size: 19px;
    line-height: 1.2;
    font-weight: 700;
}

.status-critical,
.status-alert {
    color: var(--red);
}

.status-stable {
    color: var(--red);
}

.center-action {
    display: flex;
    justify-content: center;
    text-align: center;
}

/* INFO */

.info-section {
    padding: 100px 0;
    border-bottom: 1px solid var(--line);
}

.info-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 80px;
    align-items: center;
}

.info-section h2 {
    max-width: 520px;
    font-size: 42px;
}

.info-text {
    max-width: 500px;
    color: var(--muted);
    font-size: 17px;
}

.text-link {
    color: var(--red);
    font-weight: 700;
}

.text-link:hover {
    text-decoration: underline;
}

/* DÚVIDAS */

.faq-section {
    padding: 90px 0;
}

.faq-section > .container > h2 {
    margin-top: 4px;
    margin-bottom: 35px;
}

.faq-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
}

.faq-grid details {
    background: var(--soft);
    border: 1px solid var(--line);
    padding: 22px;
    border-radius: 6px;
}

.faq-grid summary {
    cursor: pointer;
    color: var(--black);
    font-weight: 700;
}

.faq-grid p {
    color: var(--muted);
    margin-bottom: 0;
}

/* MENSAGENS */

.messages-wrap {
    width: min(1160px, calc(100% - 80px));
    margin: 20px auto 0;
}

.message {
    padding: 13px 16px;
    border: 1px solid var(--line);
    border-left: 4px solid var(--red);
    background: #fff8f8;
    border-radius: 4px;
}

/* FOOTER */

.site-footer {
    background: #17181b;
    color: #d9d9dc;
    padding: 44px 0;
}

.footer-inner {
    width: min(1160px, calc(100% - 80px));
    margin: 0 auto;
    display: grid;
    grid-template-columns: auto 1fr auto;
    gap: 30px;
    align-items: center;
}

.brand-footer .brand-name {
    font-size: 31px;
}

.brand-footer .brand-mark {
    display: none;
}

.footer-inner p {
    margin: 0;
    color: #a9aaae;
}

.footer-links {
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
}

.footer-links a {
    font-size: 14px;
    color: #d9d9dc;
}

.footer-links a:hover {
    color: var(--white);
}

/* FORMULÁRIOS / OUTRAS PÁGINAS */

main form:not(.plain-form) {
    max-width: 760px;
}

main input,
main select,
main textarea {
    border: 1px solid #d8d8db;
    border-radius: 5px;
    padding: 11px 13px;
    background: var(--white);
    color: var(--black);
}

main input:focus,
main select:focus,
main textarea:focus {
    outline: 2px solid rgba(189, 16, 38, .14);
    border-color: var(--red);
}

main button[type="submit"] {
    min-height: 48px;
    border: 0;
    border-radius: 5px;
    padding: 12px 22px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: var(--red);
    color: var(--white);
    font-weight: 700;
    line-height: 1.2;
    text-align: center;
    cursor: pointer;
}

main button[type="submit"]:hover {
    background: var(--red-dark);
}

.empty-state {
    grid-column: 1 / -1;
    color: var(--muted);
    text-align: center;
}

/* RESPONSIVO */

@media (max-width: 900px) {
    .container,
    .header-inner,
    .footer-inner,
    .messages-wrap {
        width: min(100% - 40px, 720px);
    }

    .site-header {
        height: 84px;
    }

    .menu-toggle {
        display: block;
    }

    .main-nav {
        position: absolute;
        left: 20px;
        right: 20px;
        top: 84px;
        z-index: 20;
        display: none;
        flex-direction: column;
        align-items: stretch;
        gap: 0;
        background: var(--white);
        border: 1px solid var(--line);
        box-shadow: var(--shadow);
    }

    .main-nav.is-open {
        display: flex;
    }

    .main-nav > a {
        padding: 15px 18px;
        border-bottom: 1px solid var(--line);
    }

    .main-nav .nav-cta {
        margin: 12px;
        text-align: center;
        border-bottom: 0;
    }

    .hero {
        min-height: auto;
    }

    .hero-copy {
        margin: 0 auto;
        text-align: center;
    }

    .hero-inner {
        padding: 65px 0 70px;
    }

    .hero-actions {
        justify-content: center;
    }

    .hero h1 {
        font-size: clamp(52px, 12vw, 72px);
    }

    .blood-grid {
        grid-template-columns: repeat(2, 1fr);
        gap: 35px 20px;
        margin-left: 0;
        margin-right: 0;
    }

    .info-grid,
    .faq-grid {
        grid-template-columns: 1fr;
        gap: 35px;
    }

    .footer-inner {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 520px) {
    .container,
    .header-inner,
    .footer-inner,
    .messages-wrap {
        width: calc(100% - 32px);
    }

    .brand-name {
        font-size: 31px;
    }

    .brand-mark {
        width: 36px;
        height: 36px;
    }

    .site-header .brand-mark {
        width: 36px;
        height: 36px;
    }

    .hero h1 {
        font-size: 51px;
        letter-spacing: -2px;
    }

    .hero-text {
        font-size: 16px;
    }

    .hero-actions {
        flex-direction: column;
        align-items: stretch;
    }

    .button {
        width: 100%;
    }

    .blood-grid {
        grid-template-columns: repeat(2, 1fr);
    }

    .blood-type {
        font-size: 27px;
    }

    .info-section h2 {
        font-size: 34px;
    }

    .footer-links {
        flex-direction: column;
        gap: 8px;
    }
}
``````

## Leitura das regras visuais

Seletores escolhem os elementos; declarações definem aparência. Regras posteriores e maior especificidade podem prevalecer. @media limita regras ao tamanho/condição indicado.

### Seletor `@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,600;0,700;1,600;1,700&display=swap');

:root`

```css
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,600;0,700;1,600;1,700&display=swap');

:root {
    --red: #bd1026;
    --red-dark: #a20d20;
    --red-light: #d64a59;
    --black: #17181b;
    --text: #37383d;
    --muted: #6f7076;
    --line: #e8e8e8;
    --soft: #f7f7f7;
    --white: #ffffff;
    --success: #177245;
    --warning: #bd1026;
    --shadow: 0 16px 40px rgba(20, 20, 20, .06);
}
```

- `--red: #bd1026`: define propriedade CSS aplicada ao seletor.
- `--red-dark: #a20d20`: define propriedade CSS aplicada ao seletor.
- `--red-light: #d64a59`: define propriedade CSS aplicada ao seletor.
- `--black: #17181b`: define propriedade CSS aplicada ao seletor.
- `--text: #37383d`: define propriedade CSS aplicada ao seletor.
- `--muted: #6f7076`: define propriedade CSS aplicada ao seletor.
- `--line: #e8e8e8`: define propriedade CSS aplicada ao seletor.
- `--soft: #f7f7f7`: define propriedade CSS aplicada ao seletor.
- `--white: #ffffff`: define propriedade CSS aplicada ao seletor.
- `--success: #177245`: define propriedade CSS aplicada ao seletor.
- `--warning: #bd1026`: define propriedade CSS aplicada ao seletor.
- `--shadow: 0 16px 40px rgba(20, 20, 20, .06)`: define propriedade CSS aplicada ao seletor.

### Seletor `*`

```css
* {
    box-sizing: border-box;
}
```

- `box-sizing: border-box`: define propriedade CSS aplicada ao seletor.

### Seletor `html`

```css
html {
    scroll-behavior: smooth;
}
```

- `scroll-behavior: smooth`: define propriedade CSS aplicada ao seletor.

### Seletor `body`

```css
body {
    margin: 0;
    color: var(--text);
    background: var(--white);
    font-family: "DM Sans", Arial, sans-serif;
    font-size: 16px;
    line-height: 1.6;
}
```

- `margin: 0`: define espaço externo.
- `color: var(--text)`: define cor do texto.
- `background: var(--white)`: define fundo.
- `font-family: "DM Sans", Arial, sans-serif`: define propriedade CSS aplicada ao seletor.
- `font-size: 16px`: define tamanho das letras.
- `line-height: 1.6`: define altura da linha de texto.

### Seletor `a`

```css
a {
    color: inherit;
    text-decoration: none;
}
```

- `color: inherit`: define cor do texto.
- `text-decoration: none`: define propriedade CSS aplicada ao seletor.

### Seletor `button,
input,
select,
textarea`

```css
button,
input,
select,
textarea {
    font: inherit;
}
```

- `font: inherit`: define propriedade CSS aplicada ao seletor.

### Seletor `.container`

```css
.container {
    width: min(1160px, calc(100% - 80px));
    margin: 0 auto;
}
```

- `width: min(1160px, calc(100% - 80px))`: define largura.
- `margin: 0 auto`: define espaço externo.

### Seletor `.site-header`

```css
.site-header {
    height: 112px;
    background: var(--white);
    border-bottom: 1px solid var(--line);
    display: flex;
    align-items: center;
}
```

- `height: 112px`: define altura.
- `background: var(--white)`: define fundo.
- `border-bottom: 1px solid var(--line)`: define propriedade CSS aplicada ao seletor.
- `display: flex`: define modo de organização dos elementos.
- `align-items: center`: define alinhamento no eixo transversal.

### Seletor `.header-inner`

```css
.header-inner {
    width: min(1160px, calc(100% - 80px));
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 40px;
}
```

- `width: min(1160px, calc(100% - 80px))`: define largura.
- `margin: 0 auto`: define espaço externo.
- `display: flex`: define modo de organização dos elementos.
- `align-items: center`: define alinhamento no eixo transversal.
- `justify-content: space-between`: define distribuição no eixo principal.
- `gap: 40px`: define intervalo entre itens.

### Seletor `.brand`

```css
.brand {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    color: var(--red);
    flex-shrink: 0;
}
```

- `display: inline-flex`: define modo de organização dos elementos.
- `align-items: center`: define alinhamento no eixo transversal.
- `gap: 10px`: define intervalo entre itens.
- `color: var(--red)`: define cor do texto.
- `flex-shrink: 0`: define propriedade CSS aplicada ao seletor.

### Seletor `.brand-mark`

```css
.brand-mark {
    display: inline-block;
    flex-shrink: 0;
}
```

- `display: inline-block`: define modo de organização dos elementos.
- `flex-shrink: 0`: define propriedade CSS aplicada ao seletor.

### Seletor `.site-header .brand-mark`

```css
.site-header .brand-mark {
    width: 42px;
    height: 42px;
    background: url("logo-gota.png") center / contain no-repeat;
}
```

- `width: 42px`: define largura.
- `height: 42px`: define altura.
- `background: url("logo-gota.png") center / contain no-repeat`: define fundo.

### Seletor `.brand-name`

```css
.brand-name {
    font-family: "Playfair Display", Georgia, serif;
    font-size: 36px;
    font-style: italic;
    font-weight: 700;
    line-height: 1;
    letter-spacing: 0;
}
```

- `font-family: "Playfair Display", Georgia, serif`: define propriedade CSS aplicada ao seletor.
- `font-size: 36px`: define tamanho das letras.
- `font-style: italic`: define propriedade CSS aplicada ao seletor.
- `font-weight: 700`: define peso das letras.
- `line-height: 1`: define altura da linha de texto.
- `letter-spacing: 0`: define propriedade CSS aplicada ao seletor.

### Seletor `.main-nav`

```css
.main-nav {
    display: flex;
    align-items: center;
    gap: 46px;
}
```

- `display: flex`: define modo de organização dos elementos.
- `align-items: center`: define alinhamento no eixo transversal.
- `gap: 46px`: define intervalo entre itens.

### Seletor `.main-nav > a`

```css
.main-nav > a {
    min-height: 44px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 15px;
    font-weight: 500;
    line-height: 1.2;
    text-align: center;
    color: #292a2d;
    transition: color .2s ease;
}
```

- `min-height: 44px`: define propriedade CSS aplicada ao seletor.
- `display: inline-flex`: define modo de organização dos elementos.
- `align-items: center`: define alinhamento no eixo transversal.
- `justify-content: center`: define distribuição no eixo principal.
- `font-size: 15px`: define tamanho das letras.
- `font-weight: 500`: define peso das letras.
- `line-height: 1.2`: define altura da linha de texto.
- `text-align: center`: define propriedade CSS aplicada ao seletor.
- `color: #292a2d`: define cor do texto.
- `transition: color .2s ease`: define transição visual entre valores.

### Seletor `.main-nav > a:hover`

```css
.main-nav > a:hover {
    color: var(--red);
}
```

- `color: var(--red)`: define cor do texto.

### Seletor `.main-nav .nav-cta`

```css
.main-nav .nav-cta {
    color: var(--white);
    background: var(--red);
    border-radius: 5px;
    padding: 12px 25px;
    font-weight: 700;
}
```

- `color: var(--white)`: define cor do texto.
- `background: var(--red)`: define fundo.
- `border-radius: 5px`: define arredondamento.
- `padding: 12px 25px`: define espaço interno.
- `font-weight: 700`: define peso das letras.

### Seletor `.main-nav .nav-cta:hover`

```css
.main-nav .nav-cta:hover {
    color: var(--white);
    background: var(--red-dark);
}
```

- `color: var(--white)`: define cor do texto.
- `background: var(--red-dark)`: define fundo.

### Seletor `.menu-toggle`

```css
.menu-toggle {
    display: none;
    width: 44px;
    height: 44px;
    border: 0;
    background: transparent;
    cursor: pointer;
}
```

- `display: none`: define modo de organização dos elementos.
- `width: 44px`: define largura.
- `height: 44px`: define altura.
- `border: 0`: define borda.
- `background: transparent`: define fundo.
- `cursor: pointer`: define propriedade CSS aplicada ao seletor.

### Seletor `.menu-toggle span`

```css
.menu-toggle span {
    display: block;
    width: 25px;
    height: 2px;
    background: var(--black);
    margin: 5px auto;
}
```

- `display: block`: define modo de organização dos elementos.
- `width: 25px`: define largura.
- `height: 2px`: define altura.
- `background: var(--black)`: define fundo.
- `margin: 5px auto`: define espaço externo.

### Seletor `.hero`

```css
.hero {
    min-height: 594px;
    background: var(--white);
    display: flex;
    align-items: center;
}
```

- `min-height: 594px`: define propriedade CSS aplicada ao seletor.
- `background: var(--white)`: define fundo.
- `display: flex`: define modo de organização dos elementos.
- `align-items: center`: define alinhamento no eixo transversal.

### Seletor `.hero-inner`

```css
.hero-inner {
    padding: 78px 0 76px;
}
```

- `padding: 78px 0 76px`: define espaço interno.

### Seletor `.hero-copy`

```css
.hero-copy {
    max-width: 610px;
}
```

- `max-width: 610px`: define limite máximo de largura.

### Seletor `.eyebrow`

```css
.eyebrow {
    margin: 0 0 22px;
    color: var(--red);
    font-size: 13px;
    line-height: 1.2;
    letter-spacing: 1.7px;
    font-weight: 700;
}
```

- `margin: 0 0 22px`: define espaço externo.
- `color: var(--red)`: define cor do texto.
- `font-size: 13px`: define tamanho das letras.
- `line-height: 1.2`: define altura da linha de texto.
- `letter-spacing: 1.7px`: define propriedade CSS aplicada ao seletor.
- `font-weight: 700`: define peso das letras.

### Seletor `.hero h1`

```css
.hero h1 {
    margin: 0;
    color: var(--black);
    font-family: "Playfair Display", Georgia, serif;
    font-size: clamp(58px, 6.1vw, 82px);
    line-height: .99;
    letter-spacing: -3px;
    font-weight: 700;
}
```

- `margin: 0`: define espaço externo.
- `color: var(--black)`: define cor do texto.
- `font-family: "Playfair Display", Georgia, serif`: define propriedade CSS aplicada ao seletor.
- `font-size: clamp(58px, 6.1vw, 82px)`: define tamanho das letras.
- `line-height: .99`: define altura da linha de texto.
- `letter-spacing: -3px`: define propriedade CSS aplicada ao seletor.
- `font-weight: 700`: define peso das letras.

### Seletor `.hero h1 em`

```css
.hero h1 em {
    color: var(--red);
    font-weight: 600;
}
```

- `color: var(--red)`: define cor do texto.
- `font-weight: 600`: define peso das letras.

### Seletor `.hero-text`

```css
.hero-text {
    max-width: 570px;
    margin: 32px 0 44px;
    color: #55565b;
    font-size: 17px;
    line-height: 1.7;
}
```

- `max-width: 570px`: define limite máximo de largura.
- `margin: 32px 0 44px`: define espaço externo.
- `color: #55565b`: define cor do texto.
- `font-size: 17px`: define tamanho das letras.
- `line-height: 1.7`: define altura da linha de texto.

### Seletor `.hero-actions`

```css
.hero-actions {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 25px;
}
```

- `display: flex`: define modo de organização dos elementos.
- `align-items: center`: define alinhamento no eixo transversal.
- `flex-wrap: wrap`: define propriedade CSS aplicada ao seletor.
- `gap: 25px`: define intervalo entre itens.

### Seletor `.button`

```css
.button {
    min-height: 50px;
    padding: 13px 26px;
    border-radius: 5px;
    display: inline-flex;
    justify-content: center;
    align-items: center;
    border: 1px solid transparent;
    font-weight: 700;
    font-size: 15px;
    line-height: 1.2;
    text-align: center;
    transition: .2s ease;
}
```

- `min-height: 50px`: define propriedade CSS aplicada ao seletor.
- `padding: 13px 26px`: define espaço interno.
- `border-radius: 5px`: define arredondamento.
- `display: inline-flex`: define modo de organização dos elementos.
- `justify-content: center`: define distribuição no eixo principal.
- `align-items: center`: define alinhamento no eixo transversal.
- `border: 1px solid transparent`: define borda.
- `font-weight: 700`: define peso das letras.
- `font-size: 15px`: define tamanho das letras.
- `line-height: 1.2`: define altura da linha de texto.
- `text-align: center`: define propriedade CSS aplicada ao seletor.
- `transition: .2s ease`: define transição visual entre valores.

### Seletor `.button-primary`

```css
.button-primary {
    color: var(--white);
    background: var(--red);
}
```

- `color: var(--white)`: define cor do texto.
- `background: var(--red)`: define fundo.

### Seletor `.button-primary:hover`

```css
.button-primary:hover {
    background: var(--red-dark);
    transform: translateY(-1px);
}
```

- `background: var(--red-dark)`: define fundo.
- `transform: translateY(-1px)`: define propriedade CSS aplicada ao seletor.

### Seletor `.button-outline`

```css
.button-outline {
    color: var(--red);
    background: transparent;
    border-color: var(--red);
}
```

- `color: var(--red)`: define cor do texto.
- `background: transparent`: define fundo.
- `border-color: var(--red)`: define propriedade CSS aplicada ao seletor.

### Seletor `.button-outline:hover`

```css
.button-outline:hover {
    background: #fff5f6;
}
```

- `background: #fff5f6`: define fundo.

### Seletor `.button-small`

```css
.button-small {
    min-width: 260px;
}
```

- `min-width: 260px`: define propriedade CSS aplicada ao seletor.

### Seletor `.stock-section`

```css
.stock-section {
    background: #f6f6f6;
    padding: 64px 0 58px;
}
```

- `background: #f6f6f6`: define fundo.
- `padding: 64px 0 58px`: define espaço interno.

### Seletor `.section-heading h2,
.info-section h2,
.faq-section h2`

```css
.section-heading h2,
.info-section h2,
.faq-section h2 {
    margin: 0;
    color: var(--black);
    font-family: "Playfair Display", Georgia, serif;
    font-size: 31px;
    line-height: 1.15;
    letter-spacing: -.5px;
}
```

- `margin: 0`: define espaço externo.
- `color: var(--black)`: define cor do texto.
- `font-family: "Playfair Display", Georgia, serif`: define propriedade CSS aplicada ao seletor.
- `font-size: 31px`: define tamanho das letras.
- `line-height: 1.15`: define altura da linha de texto.
- `letter-spacing: -.5px`: define propriedade CSS aplicada ao seletor.

### Seletor `.section-heading p`

```css
.section-heading p {
    max-width: 640px;
    margin: 8px auto 0;
    color: #4c4d51;
    font-size: 16px;
    text-align: center;
}
```

- `max-width: 640px`: define limite máximo de largura.
- `margin: 8px auto 0`: define espaço externo.
- `color: #4c4d51`: define cor do texto.
- `font-size: 16px`: define tamanho das letras.
- `text-align: center`: define propriedade CSS aplicada ao seletor.

### Seletor `.section-heading`

```css
.section-heading {
    text-align: center;
}
```

- `text-align: center`: define propriedade CSS aplicada ao seletor.

### Seletor `.blood-grid`

```css
.blood-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 58px 40px;
    margin: 42px 35px 48px;
}
```

- `display: grid`: define modo de organização dos elementos.
- `grid-template-columns: repeat(4, 1fr)`: define colunas da grade.
- `gap: 58px 40px`: define intervalo entre itens.
- `margin: 42px 35px 48px`: define espaço externo.

### Seletor `.blood-card`

```css
.blood-card {
    min-height: 112px;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}
```

- `min-height: 112px`: define propriedade CSS aplicada ao seletor.
- `text-align: center`: define propriedade CSS aplicada ao seletor.
- `display: flex`: define modo de organização dos elementos.
- `flex-direction: column`: define direção dos itens flex.
- `align-items: center`: define alinhamento no eixo transversal.
- `justify-content: center`: define distribuição no eixo principal.

### Seletor `.blood-type`

```css
.blood-type {
    color: #202125;
    font-size: 31px;
    line-height: 1;
    font-weight: 500;
}
```

- `color: #202125`: define cor do texto.
- `font-size: 31px`: define tamanho das letras.
- `line-height: 1`: define altura da linha de texto.
- `font-weight: 500`: define peso das letras.

### Seletor `.blood-line`

```css
.blood-line {
    width: 86px;
    height: 2px;
    background: var(--red-light);
    margin: 20px 0 11px;
}
```

- `width: 86px`: define largura.
- `height: 2px`: define altura.
- `background: var(--red-light)`: define fundo.
- `margin: 20px 0 11px`: define espaço externo.

### Seletor `.blood-status`

```css
.blood-status {
    font-size: 19px;
    line-height: 1.2;
    font-weight: 700;
}
```

- `font-size: 19px`: define tamanho das letras.
- `line-height: 1.2`: define altura da linha de texto.
- `font-weight: 700`: define peso das letras.

### Seletor `.status-critical,
.status-alert`

```css
.status-critical,
.status-alert {
    color: var(--red);
}
```

- `color: var(--red)`: define cor do texto.

### Seletor `.status-stable`

```css
.status-stable {
    color: var(--red);
}
```

- `color: var(--red)`: define cor do texto.

### Seletor `.center-action`

```css
.center-action {
    display: flex;
    justify-content: center;
    text-align: center;
}
```

- `display: flex`: define modo de organização dos elementos.
- `justify-content: center`: define distribuição no eixo principal.
- `text-align: center`: define propriedade CSS aplicada ao seletor.

### Seletor `.info-section`

```css
.info-section {
    padding: 100px 0;
    border-bottom: 1px solid var(--line);
}
```

- `padding: 100px 0`: define espaço interno.
- `border-bottom: 1px solid var(--line)`: define propriedade CSS aplicada ao seletor.

### Seletor `.info-grid`

```css
.info-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 80px;
    align-items: center;
}
```

- `display: grid`: define modo de organização dos elementos.
- `grid-template-columns: 1fr 1fr`: define colunas da grade.
- `gap: 80px`: define intervalo entre itens.
- `align-items: center`: define alinhamento no eixo transversal.

### Seletor `.info-section h2`

```css
.info-section h2 {
    max-width: 520px;
    font-size: 42px;
}
```

- `max-width: 520px`: define limite máximo de largura.
- `font-size: 42px`: define tamanho das letras.

### Seletor `.info-text`

```css
.info-text {
    max-width: 500px;
    color: var(--muted);
    font-size: 17px;
}
```

- `max-width: 500px`: define limite máximo de largura.
- `color: var(--muted)`: define cor do texto.
- `font-size: 17px`: define tamanho das letras.

### Seletor `.text-link`

```css
.text-link {
    color: var(--red);
    font-weight: 700;
}
```

- `color: var(--red)`: define cor do texto.
- `font-weight: 700`: define peso das letras.

### Seletor `.text-link:hover`

```css
.text-link:hover {
    text-decoration: underline;
}
```

- `text-decoration: underline`: define propriedade CSS aplicada ao seletor.

### Seletor `.faq-section`

```css
.faq-section {
    padding: 90px 0;
}
```

- `padding: 90px 0`: define espaço interno.

### Seletor `.faq-section > .container > h2`

```css
.faq-section > .container > h2 {
    margin-top: 4px;
    margin-bottom: 35px;
}
```

- `margin-top: 4px`: define propriedade CSS aplicada ao seletor.
- `margin-bottom: 35px`: define propriedade CSS aplicada ao seletor.

### Seletor `.faq-grid`

```css
.faq-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
}
```

- `display: grid`: define modo de organização dos elementos.
- `grid-template-columns: repeat(3, 1fr)`: define colunas da grade.
- `gap: 20px`: define intervalo entre itens.

### Seletor `.faq-grid details`

```css
.faq-grid details {
    background: var(--soft);
    border: 1px solid var(--line);
    padding: 22px;
    border-radius: 6px;
}
```

- `background: var(--soft)`: define fundo.
- `border: 1px solid var(--line)`: define borda.
- `padding: 22px`: define espaço interno.
- `border-radius: 6px`: define arredondamento.

### Seletor `.faq-grid summary`

```css
.faq-grid summary {
    cursor: pointer;
    color: var(--black);
    font-weight: 700;
}
```

- `cursor: pointer`: define propriedade CSS aplicada ao seletor.
- `color: var(--black)`: define cor do texto.
- `font-weight: 700`: define peso das letras.

### Seletor `.faq-grid p`

```css
.faq-grid p {
    color: var(--muted);
    margin-bottom: 0;
}
```

- `color: var(--muted)`: define cor do texto.
- `margin-bottom: 0`: define propriedade CSS aplicada ao seletor.

### Seletor `.messages-wrap`

```css
.messages-wrap {
    width: min(1160px, calc(100% - 80px));
    margin: 20px auto 0;
}
```

- `width: min(1160px, calc(100% - 80px))`: define largura.
- `margin: 20px auto 0`: define espaço externo.

### Seletor `.message`

```css
.message {
    padding: 13px 16px;
    border: 1px solid var(--line);
    border-left: 4px solid var(--red);
    background: #fff8f8;
    border-radius: 4px;
}
```

- `padding: 13px 16px`: define espaço interno.
- `border: 1px solid var(--line)`: define borda.
- `border-left: 4px solid var(--red)`: define propriedade CSS aplicada ao seletor.
- `background: #fff8f8`: define fundo.
- `border-radius: 4px`: define arredondamento.

### Seletor `.site-footer`

```css
.site-footer {
    background: #17181b;
    color: #d9d9dc;
    padding: 44px 0;
}
```

- `background: #17181b`: define fundo.
- `color: #d9d9dc`: define cor do texto.
- `padding: 44px 0`: define espaço interno.

### Seletor `.footer-inner`

```css
.footer-inner {
    width: min(1160px, calc(100% - 80px));
    margin: 0 auto;
    display: grid;
    grid-template-columns: auto 1fr auto;
    gap: 30px;
    align-items: center;
}
```

- `width: min(1160px, calc(100% - 80px))`: define largura.
- `margin: 0 auto`: define espaço externo.
- `display: grid`: define modo de organização dos elementos.
- `grid-template-columns: auto 1fr auto`: define colunas da grade.
- `gap: 30px`: define intervalo entre itens.
- `align-items: center`: define alinhamento no eixo transversal.

### Seletor `.brand-footer .brand-name`

```css
.brand-footer .brand-name {
    font-size: 31px;
}
```

- `font-size: 31px`: define tamanho das letras.

### Seletor `.brand-footer .brand-mark`

```css
.brand-footer .brand-mark {
    display: none;
}
```

- `display: none`: define modo de organização dos elementos.

### Seletor `.footer-inner p`

```css
.footer-inner p {
    margin: 0;
    color: #a9aaae;
}
```

- `margin: 0`: define espaço externo.
- `color: #a9aaae`: define cor do texto.

### Seletor `.footer-links`

```css
.footer-links {
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
}
```

- `display: flex`: define modo de organização dos elementos.
- `gap: 20px`: define intervalo entre itens.
- `flex-wrap: wrap`: define propriedade CSS aplicada ao seletor.

### Seletor `.footer-links a`

```css
.footer-links a {
    font-size: 14px;
    color: #d9d9dc;
}
```

- `font-size: 14px`: define tamanho das letras.
- `color: #d9d9dc`: define cor do texto.

### Seletor `.footer-links a:hover`

```css
.footer-links a:hover {
    color: var(--white);
}
```

- `color: var(--white)`: define cor do texto.

### Seletor `main form:not(.plain-form)`

```css
main form:not(.plain-form) {
    max-width: 760px;
}
```

- `max-width: 760px`: define limite máximo de largura.

### Seletor `main input,
main select,
main textarea`

```css
main input,
main select,
main textarea {
    border: 1px solid #d8d8db;
    border-radius: 5px;
    padding: 11px 13px;
    background: var(--white);
    color: var(--black);
}
```

- `border: 1px solid #d8d8db`: define borda.
- `border-radius: 5px`: define arredondamento.
- `padding: 11px 13px`: define espaço interno.
- `background: var(--white)`: define fundo.
- `color: var(--black)`: define cor do texto.

### Seletor `main input:focus,
main select:focus,
main textarea:focus`

```css
main input:focus,
main select:focus,
main textarea:focus {
    outline: 2px solid rgba(189, 16, 38, .14);
    border-color: var(--red);
}
```

- `outline: 2px solid rgba(189, 16, 38, .14)`: define propriedade CSS aplicada ao seletor.
- `border-color: var(--red)`: define propriedade CSS aplicada ao seletor.

### Seletor `main button[type="submit"]`

```css
main button[type="submit"] {
    min-height: 48px;
    border: 0;
    border-radius: 5px;
    padding: 12px 22px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: var(--red);
    color: var(--white);
    font-weight: 700;
    line-height: 1.2;
    text-align: center;
    cursor: pointer;
}
```

- `min-height: 48px`: define propriedade CSS aplicada ao seletor.
- `border: 0`: define borda.
- `border-radius: 5px`: define arredondamento.
- `padding: 12px 22px`: define espaço interno.
- `display: inline-flex`: define modo de organização dos elementos.
- `align-items: center`: define alinhamento no eixo transversal.
- `justify-content: center`: define distribuição no eixo principal.
- `background: var(--red)`: define fundo.
- `color: var(--white)`: define cor do texto.
- `font-weight: 700`: define peso das letras.
- `line-height: 1.2`: define altura da linha de texto.
- `text-align: center`: define propriedade CSS aplicada ao seletor.
- `cursor: pointer`: define propriedade CSS aplicada ao seletor.

### Seletor `main button[type="submit"]:hover`

```css
main button[type="submit"]:hover {
    background: var(--red-dark);
}
```

- `background: var(--red-dark)`: define fundo.

### Seletor `.empty-state`

```css
.empty-state {
    grid-column: 1 / -1;
    color: var(--muted);
    text-align: center;
}
```

- `grid-column: 1 / -1`: define propriedade CSS aplicada ao seletor.
- `color: var(--muted)`: define cor do texto.
- `text-align: center`: define propriedade CSS aplicada ao seletor.

### Seletor `.container,
    .header-inner,
    .footer-inner,
    .messages-wrap`

```css
.container,
    .header-inner,
    .footer-inner,
    .messages-wrap {
        width: min(100% - 40px, 720px);
    }
```

- `width: min(100% - 40px, 720px)`: define largura.

### Seletor `.site-header`

```css
.site-header {
        height: 84px;
    }
```

- `height: 84px`: define altura.

### Seletor `.menu-toggle`

```css
.menu-toggle {
        display: block;
    }
```

- `display: block`: define modo de organização dos elementos.

### Seletor `.main-nav`

```css
.main-nav {
        position: absolute;
        left: 20px;
        right: 20px;
        top: 84px;
        z-index: 20;
        display: none;
        flex-direction: column;
        align-items: stretch;
        gap: 0;
        background: var(--white);
        border: 1px solid var(--line);
        box-shadow: var(--shadow);
    }
```

- `position: absolute`: define modelo de posicionamento.
- `left: 20px`: define propriedade CSS aplicada ao seletor.
- `right: 20px`: define propriedade CSS aplicada ao seletor.
- `top: 84px`: define propriedade CSS aplicada ao seletor.
- `z-index: 20`: define ordem de sobreposição.
- `display: none`: define modo de organização dos elementos.
- `flex-direction: column`: define direção dos itens flex.
- `align-items: stretch`: define alinhamento no eixo transversal.
- `gap: 0`: define intervalo entre itens.
- `background: var(--white)`: define fundo.
- `border: 1px solid var(--line)`: define borda.
- `box-shadow: var(--shadow)`: define sombra.

### Seletor `.main-nav.is-open`

```css
.main-nav.is-open {
        display: flex;
    }
```

- `display: flex`: define modo de organização dos elementos.

### Seletor `.main-nav > a`

```css
.main-nav > a {
        padding: 15px 18px;
        border-bottom: 1px solid var(--line);
    }
```

- `padding: 15px 18px`: define espaço interno.
- `border-bottom: 1px solid var(--line)`: define propriedade CSS aplicada ao seletor.

### Seletor `.main-nav .nav-cta`

```css
.main-nav .nav-cta {
        margin: 12px;
        text-align: center;
        border-bottom: 0;
    }
```

- `margin: 12px`: define espaço externo.
- `text-align: center`: define propriedade CSS aplicada ao seletor.
- `border-bottom: 0`: define propriedade CSS aplicada ao seletor.

### Seletor `.hero`

```css
.hero {
        min-height: auto;
    }
```

- `min-height: auto`: define propriedade CSS aplicada ao seletor.

### Seletor `.hero-copy`

```css
.hero-copy {
        margin: 0 auto;
        text-align: center;
    }
```

- `margin: 0 auto`: define espaço externo.
- `text-align: center`: define propriedade CSS aplicada ao seletor.

### Seletor `.hero-inner`

```css
.hero-inner {
        padding: 65px 0 70px;
    }
```

- `padding: 65px 0 70px`: define espaço interno.

### Seletor `.hero-actions`

```css
.hero-actions {
        justify-content: center;
    }
```

- `justify-content: center`: define distribuição no eixo principal.

### Seletor `.hero h1`

```css
.hero h1 {
        font-size: clamp(52px, 12vw, 72px);
    }
```

- `font-size: clamp(52px, 12vw, 72px)`: define tamanho das letras.

### Seletor `.blood-grid`

```css
.blood-grid {
        grid-template-columns: repeat(2, 1fr);
        gap: 35px 20px;
        margin-left: 0;
        margin-right: 0;
    }
```

- `grid-template-columns: repeat(2, 1fr)`: define colunas da grade.
- `gap: 35px 20px`: define intervalo entre itens.
- `margin-left: 0`: define propriedade CSS aplicada ao seletor.
- `margin-right: 0`: define propriedade CSS aplicada ao seletor.

### Seletor `.info-grid,
    .faq-grid`

```css
.info-grid,
    .faq-grid {
        grid-template-columns: 1fr;
        gap: 35px;
    }
```

- `grid-template-columns: 1fr`: define colunas da grade.
- `gap: 35px`: define intervalo entre itens.

### Seletor `.footer-inner`

```css
.footer-inner {
        grid-template-columns: 1fr;
    }
```

- `grid-template-columns: 1fr`: define colunas da grade.

### Seletor `.container,
    .header-inner,
    .footer-inner,
    .messages-wrap`

```css
.container,
    .header-inner,
    .footer-inner,
    .messages-wrap {
        width: calc(100% - 32px);
    }
```

- `width: calc(100% - 32px)`: define largura.

### Seletor `.brand-name`

```css
.brand-name {
        font-size: 31px;
    }
```

- `font-size: 31px`: define tamanho das letras.

### Seletor `.brand-mark`

```css
.brand-mark {
        width: 36px;
        height: 36px;
    }
```

- `width: 36px`: define largura.
- `height: 36px`: define altura.

### Seletor `.site-header .brand-mark`

```css
.site-header .brand-mark {
        width: 36px;
        height: 36px;
    }
```

- `width: 36px`: define largura.
- `height: 36px`: define altura.

### Seletor `.hero h1`

```css
.hero h1 {
        font-size: 51px;
        letter-spacing: -2px;
    }
```

- `font-size: 51px`: define tamanho das letras.
- `letter-spacing: -2px`: define propriedade CSS aplicada ao seletor.

### Seletor `.hero-text`

```css
.hero-text {
        font-size: 16px;
    }
```

- `font-size: 16px`: define tamanho das letras.

### Seletor `.hero-actions`

```css
.hero-actions {
        flex-direction: column;
        align-items: stretch;
    }
```

- `flex-direction: column`: define direção dos itens flex.
- `align-items: stretch`: define alinhamento no eixo transversal.

### Seletor `.button`

```css
.button {
        width: 100%;
    }
```

- `width: 100%`: define largura.

### Seletor `.blood-grid`

```css
.blood-grid {
        grid-template-columns: repeat(2, 1fr);
    }
```

- `grid-template-columns: repeat(2, 1fr)`: define colunas da grade.

### Seletor `.blood-type`

```css
.blood-type {
        font-size: 27px;
    }
```

- `font-size: 27px`: define tamanho das letras.

### Seletor `.info-section h2`

```css
.info-section h2 {
        font-size: 34px;
    }
```

- `font-size: 34px`: define tamanho das letras.

### Seletor `.footer-links`

```css
.footer-links {
        flex-direction: column;
        gap: 8px;
    }
```

- `flex-direction: column`: define direção dos itens flex.
- `gap: 8px`: define intervalo entre itens.

