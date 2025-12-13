# Trabalho de Computação Gráfica - 2ª Etapa

**1) Modele os seguintes sólidos/objetos:**

* **a. Cubo:** Definido usando uma base em uma **aresta**.
* **b. Cano Curvado:** Definido usando uma base em um **raio** e uma **curva** (Bezier ou Hermite).
* **c. Toro:** Definido usando uma base em um **raio interno** e outro **externo**.
* **d. Malha de Polígonos:** Para cada um dos sólidos acima, crie uma **malha de polígonos (triângulos)** usando algum algoritmo próprio ou o algoritmo **marching cubes** (não precisa implementar esse algoritmo, basta usar de alguma API).

> **Nota:** Na construção dos sólidos, crie uma função que **retorne o sólido** (ou seja, retorne a **matriz de vértices e arestas**). Perceba que cada objeto é descrito indiretamente (no caso do cone, por exemplo, pelo raio e pela altura). A **origem** do objeto pode ser definida de forma fixa dentro da função ou, opcionalmente, pode ser passada também como parâmetro da função.

---

**2) Componha uma cena contendo os diversos sólidos modelados:**

Componha a cena em um **sistema de coordenadas do mundo**, de tal maneira a **não haver sobreposição ou intersecção** entre tais objetos, usando transformações em **escala, rotação e translação**.

* **a. Limites:** O maior valor possível para cada uma das componentes de um vértice deve ser igual a **8**. Se necessário, aplique transformações em **escala** para que os sólidos sejam localizados respeitando tais limites.
* **b. Visualização:** Mostre os diversos sólidos neste sistema de coordenadas em **3D**.

---

**3) Escolha um ponto como origem para o sistema de coordenadas da câmera:**

* **a. Base Vetorial:** Compute a base vetorial (**u, v e z**) do novo sistema de coordenadas.
* **b. Transformação:** Transforme os objetos do **sistema de coordenadas do mundo** para o **sistema de coordenadas da câmera**.
* **c. Visualização:** Mostre os diversos sólidos neste sistema de coordenadas em **3D**.
* **d. Origem:** Coloque um ponto informando a **origem** do sistema de coordenadas do mundo.

---

**4) Faça uma transformação de projeção em perspectiva:**

Projete os sólidos contidos no volume de visão em **2 dimensões** na **janela de projeção**. Cada sólido deve conter **arestas com mesma cor**, mas sólidos diferentes devem ter **cores diferentes**.

* **a. Resultado:** Apresente tais objetos em **2D**.

---

**5) Rasterize os objetos (polígonos) em pelo menos 3 resoluções diferentes.**

---

### Observações Importantes:

* **Obs1:** Faça um **relatório completo** com: **capa, introdução, objetivo, desenvolvimento, simulações computacionais, conclusão e referências**.
* **Obs2:** Na entrega, subam **2 arquivos apenas**: um **zip com código** e um **pdf com o relatório**.
* **Obs3:** Trabalho em **dupla**.
* **Obs4:** Haverá **apresentação** do trabalho em dia específico.