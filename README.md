# Pipeline Gráfico 3D

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)
![Scikit-Image](https://img.shields.io/badge/scikit--image-%23343434.svg?style=for-the-badge&logo=scikit-image&logoColor=white)

Implementação de um pipeline gráfico 3D abrangendo modelagem, transformações geométricas, projeção e rasterização. Desenvolvido em Python com bibliotecas de processamento numérico e de imagem.

---

## Resultados Visuais

### 1. Sistema de Coordenadas do Mundo
Visualização dos sólidos (Cubo, Toro e Cano) posicionados no espaço global após aplicação de transformações afins.

<p align="center">
  <img src="imagens/scm.png" width="324" alt="Sistema de Coordenadas do Mundo">
</p>

### 2. Sistema de Coordenadas da Câmera
Comparativo entre a cena original e a visualização transformada para o espaço do olho (vetores UVN).

<p align="center">
  <img src="imagens/scc.png" width="564" alt="Sistema de Coordenadas da Câmera">
</p>

### 3. Projeção em Perspectiva
Projeção dos objetos 3D no plano 2D (NDC).

<p align="center">
  <img src="imagens/projecao.png" width="324" alt="Projeção 2D">
</p>

### 4. Rasterização
Conversão da geometria vetorial em fragmentos utilizando algoritmo scanline em múltiplas resoluções.

<p align="center">
  <img src="imagens/rasterizacao.png" width="740" alt="Rasterização">
</p>

---

## Configuração do Ambiente

### 1. Ambiente Virtual

**Windows:**

```bash
python -m venv venv
.\venv\Scripts\activate

```

**Linux / macOS:**

```bash
python3 -m venv venv
source venv/bin/activate

```

### 2. Dependências

```bash
pip install -r requirements.txt

```

---

## Execução

Execute os comandos a partir da raiz do projeto, utilizando a flag `-m` para resolução de módulos.

### Sintaxe

```bash
python -m app.<modulo>

```

### Exemplos

* **Cena no Mundo:** `python -m app.scm`
* **Câmera:** `python -m app.scc`
* **Projeção:** `python -m app.projecao`
* **Rasterização:** `python -m app.rasterizacao`
* **Sólidos:**
* `python -m app.solidos.cubo`
* `python -m app.solidos.toro`
* `python -m app.solidos.cano`