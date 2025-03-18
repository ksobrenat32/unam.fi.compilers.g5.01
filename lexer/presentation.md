---
title:
- "Lexer"
author:
- \textsc{Enrique Calderón} \newline
- \textsc{Luis Salazar} \newline
- \textsc{Hansel Tepal} \newline
- \textsc{Luis Ugartechea} \newline
institute:
- \textit{Universidad Nacional Autónoma de México\\ Facultad de Ingeniería}
date:
- March 18, 2025
---

# Introduction

Our lexical analizer follows the KISS principle, as you would expect for a software implementation. As we know the process is essential for the compiler to work, we need to take into consideration that this should reduce future problems during the next steps of analysis.

![Our lexer :)](./presentation_img/intro.png)

# Rules for the lexer

In order to design and implement a lexical analyzer we should be able to identify tokens, which are the smallest unit of a program. Each token most follow a grammatical rule depending on his type, for the output we will classify the tokes and print the total amount for the lexem input.

![Block diagram](./presentation_img/block_diag.png)