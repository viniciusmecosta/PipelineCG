# Pipeline Gráfico 3D

## Configuração

### 1. Criar e ativar o ambiente virtual

**Windows:**

```bash
python -m venv venv
.\venv\Scripts\activate
````

**Linux / macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Instalar as dependências

```bash
pip install -r requirements.txt
```

---

## Como Executar

**Importante:**
Execute todos os comandos a partir da **pasta raiz do projeto** (a pasta pai de `app`).
Use a flag `-m` para garantir que o Python resolva corretamente os imports.

### Padrão do comando

```bash
python -m app.caminho.do.arquivo
```

### Exemplo

```bash
python -m app.scm
```

Basta substituir `app.scm` pelo caminho do módulo desejado, por exemplo:

* `app.solidos.cubo`
* `app.rasterizacao`

---