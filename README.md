# Mini Roguelike

Um pequeno jogo feito com Pygame Zero (PgZero). Movimente o herói pelo mapa, evite os inimigos e tente sobreviver o máximo possível.

## Requisitos
- Python 3.8+
- Pygame Zero (pgzero)

Instalação do PgZero:
```bash
pip install pgzero
```

## Como executar
Na pasta do projeto:
```bash
pgzrun main.py
```

## Controles
- Setas ou WASD: mover o herói (uma célula por vez)
- ESC: voltar ao menu
- ENTER (no menu): iniciar o jogo
- Clique no botão "Music/Sounds": alterna ligar/desligar áudio
- Clique em "Exit": sair do jogo

## Objetivo
- Desviar dos inimigos no mapa. Se um inimigo ocupar a mesma célula do herói, é "Game Over".

## Estados do jogo
- Menu: três botões (Start Game, Music/Sounds, Exit)
- Jogando: o herói e inimigos se movimentam pelo grid
- Game Over: mensagem na tela e opção de retornar ao menu (ENTER ou clique)

## Áudio
- Música de fundo (quando disponível) e efeitos de passo/ataque.
- Você pode alternar entre ligado/desligado no menu.

## Gráficos
- Tiles do mapa (piso/parede) estão em `images/`.
- Personagens usam sprites se existirem:
  - `images/hero.png`
  - `images/enemy.png`
  - `images/enemy_02.png`
- Se uma imagem não puder ser carregada, o jogo usa um desenho simples como fallback.

## Estrutura do projeto
```
pgz-roguelike/
├─ main.py
├─ images/
├─ sounds/
├─ music/
└─ tools/
```

## Créditos
- Código-base: Cley Gabriel (referência no menu do jogo)

## Licença
Este projeto é para fins educacionais/demonstrativos. Ajuste a licença conforme necessário.

## Licenças e Referências dos Assets
Todos os gráficos utilizados foram obtidos do pacote "Tiny Dungeon (1.0)" por Kenney.

- Site do autor: https://www.kenney.nl
- Página do asset: https://www.kenney.nl/assets/tiny-dungeon
- Licença: Creative Commons Zero (CC0)
  - Texto oficial: http://creativecommons.org/publicdomain/zero/1.0/
- Observação: O uso é livre para projetos pessoais, educacionais e comerciais. Crédito a "Kenney" ou "www.kenney.nl" é apreciado, porém não obrigatório.

Itens usados neste projeto (todos cobertos pela licença acima):
- `images/hero.png` — Kenney, Tiny Dungeon (1.0), CC0
- `images/enemy.png` — Kenney, Tiny Dungeon (1.0), CC0
- `images/enemy_02.png` — Kenney, Tiny Dungeon (1.0), CC0
- `images/piso.png` — Kenney, Tiny Dungeon (1.0), CC0
- `images/parede.png` — Kenney, Tiny Dungeon (1.0), CC0
- `images/bau.png` — Kenney, Tiny Dungeon (1.0), CC0
