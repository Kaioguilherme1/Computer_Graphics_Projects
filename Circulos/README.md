## 1. Introdução

Este relatório visa comparar três algoritmos para desenhar círculos em um ambiente computacional. Cada algoritmo utiliza uma abordagem diferente para gerar o contorno de um círculo, permitindo uma análise de eficiência e complexidade. Os três algoritmos são:

1. **Algoritmo Incremental com Simetria**: Utiliza a técnica de simetria para desenhar um círculo com base em cálculos incrementais.
2. **Equação Paramétrica**: Desenha o círculo utilizando a formulação trigonométrica para calcular os pontos da borda.
3. **Método de Bresenham**: Um algoritmo clássico de rasterização de círculos que usa uma abordagem incremental com uma equação de decisão.

### Algoritmos Analisados

1. **Algoritmo Incremental com Simetria**: Desenha um círculo de forma eficiente utilizando simetria e incrementos ao longo dos octantes.
2. **Equação Paramétrica**: Usa a equação  e  para calcular os pontos ao longo da circunferência.

   x=xc+r⋅cos⁡(θ)x = xc + r \cdot \cos(\theta)

   y=yc+r⋅sin⁡(θ)y = yc + r \cdot \sin(\theta)

3. **Método de Bresenham**: Um algoritmo de rasterização baseado em decisões incrementais com a escolha do ponto mais próximo da circunferência ideal.

---

## 2. Descrição do Funcionamento

### 2.1 Algoritmo **Incremental com Simetria**

Este algoritmo utiliza a simetria dos círculos para desenhar todos os 8 octantes ao mesmo tempo. Ele começa com um ponto inicial no topo do círculo e, em seguida, calcula os pontos sucessivos baseando-se em decisões incrementais.

- **Processo**:
    1. Calcula o raio do círculo a partir do centro e de um ponto de extremidade.
    2. Desenha o ponto inicial (topo do círculo).
    3. Utiliza a simetria para desenhar os 8 pontos ao mesmo tempo.
    4. A cada iteração, a posição dos pontos é ajustada com base em um parâmetro de decisão.
    5. O desenho é feito diretamente na tela, com um controle de velocidade para a renderização.


### 2.2 Algoritmo **Equação Paramétrica**

O algoritmo **Equação Paramétrica** utiliza a equação trigonométrica para calcular os pontos do círculo. O parâmetro tt varia de 1 a 360 graus, sendo utilizado para calcular as coordenadas xx e yy para cada ponto do círculo.

- **Processo**:
    1. Calcula o raio do círculo com base nas coordenadas do centro e da extremidade.
    2. Utiliza a equação paramétrica para calcular as coordenadas  e  dos pontos ao longo da circunferência.

       xx

       yy

    3. Desenha os pontos calculados diretamente na tela.
    4. A velocidade de renderização é controlada com um atraso entre as operações.


### 2.3 Algoritmo **Método de Bresenham**

O **Método de Bresenham** é uma abordagem eficiente para rasterizar círculos, utilizando um algoritmo de decisão baseado em incrementos que escolhe o ponto mais próximo da circunferência ideal.

- **Processo**:
    1. Calcula o raio do círculo.
    2. Desenha os primeiros pontos simétricos baseados no raio e centro.
    3. A cada iteração, avalia a posição do próximo ponto com base em uma decisão incremental.
    4. O algoritmo desenha os pontos simétricos dos 8 octantes do círculo.

---

## 3. Diferenças Entre os Algoritmos

| Característica | **Incremental com Simetria** | **Equação Paramétrica** | **Método de Bresenham** |
| --- | --- | --- | --- |
| **Tipo de Algoritmo** | Incremental com simetria | Trigonométrico | Incremental com decisão |
| **Velocidade** | Controlada por parâmetro de decisão | Controlada por t e atraso | Controlada por parâmetro de decisão |
| **Precisão** | Alta, especialmente para círculos pequenos | Alta para qualquer círculo | Alta, mesmo em círculos grandes |
| **Limitações** | Desempenho pode cair em áreas muito grandes | Dependente de precisões angulares | Pode sofrer de erros de arredondamento em círculos grandes |

---

## 4. Análise de Desempenho

Os algoritmos **Incremental com Simetria**, **Equação Paramétrica** e **Método de Bresenham** são executados simultaneamente, cada um em uma thread separada para garantir que o desempenho de um não interfira no outro. O algoritmo Incremental com Simetria utiliza a simetria dos 8 octantes para desenhar o círculo em tempo real, enquanto o de Equação Paramétrica calcula os pontos com base nas funções trigonométricas e oferece controle através de um parâmetro de velocidade. Já o Método de Bresenham, amplamente utilizado por sua eficiência, utiliza cálculos incrementais para determinar o ponto mais próximo da circunferência ideal. A execução independente dos algoritmos pode ser visualizada no GIF abaixo, destacando as características e a performance de cada um.

![Tese_Circufferencia.gif](Tese_Circufferencia.gif)
Foram usadas matrizes de 400x400 pixel em escala 1:1
---

## 5. Conclusão

Os três algoritmos têm suas vantagens e limitações, mas a escolha do algoritmo adequado depende do tipo de aplicação e dos requisitos específicos de desempenho. O **Incremental com Simetria** é eficiente e simples, ideal para círculos pequenos e médios. O **Equação Paramétrica** oferece uma abordagem matemática precisa, sendo útil quando a precisão dos pontos é essencial. O **Método de Bresenham**, por outro lado, é muito eficiente para grandes círculos, especialmente quando a precisão é importante, e sua abordagem incremental permite um controle fino sobre os pontos desenhados.

A decisão de qual algoritmo usar deve levar em conta os requisitos de desempenho, precisão e complexidade da implementação desejada.