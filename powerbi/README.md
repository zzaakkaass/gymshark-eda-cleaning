# dashboard de análise prescritiva — roteiro para power bi

este diretório contém os dados já preparados para montar, no power bi desktop,
uma apresentação da análise prescritiva que está no README principal do
projeto. eu não consigo gerar o `.pbix` (é um app gráfico de windows, não
roda no ambiente onde eu executo), então aqui vai tudo pronto pra você montar
rápido: os dados certos e um roteiro de quais visuais criar em cada página.

## dados

as tabelas pequenas abaixo já estão neste diretório, versionadas no git.
a tabela produto-a-produto (44.830 linhas) não é versionada — gere localmente:

```
PYTHONPATH=src python powerbi/prepare_data.py
```

isso cria/atualiza:

| arquivo | linhas | conteúdo |
|---|---|---|
| `data/category_counts.csv` | 90 | contagem de produtos por `product_type` |
| `data/price_outliers.csv` | 12 | os 12 produtos com preço > usd 500 |
| `data/image_fill_funnel.csv` | 4 | quantos produtos cada camada do greedy filler resolveu |
| `data/category_fragmentation.csv` | 12 | pares de `product_type` que só diferem por maiúscula/espaço |
| `data/processed/powerbi_products.csv` (raiz do repo, não versionado) | 44.830 | tabela completa: handle, title, product_type, vendor, price, is_price_outlier |

## importar no power bi desktop

`obter dados` → `texto/csv` → selecione os 5 arquivos acima (um por vez, ou
`pasta` apontando pra `powerbi/data/` + o arquivo em `data/processed/`
separadamente). não precisa de transformação no power query — os csvs já
saem prontos pro tipo de visual de cada página.

## roteiro por página

### página 1 — visão geral (descritivo)
serve de abertura, contextualiza os números antes de entrar nos achados.

- **cards (kpi)**: total de produtos (`COUNTROWS(powerbi_products)` = 44.830),
  preço médio (`AVERAGE(powerbi_products[price])` ≈ usd 27,76), preço máximo
  (usd 1.000 — já é o gancho pro achado 1).
- **gráfico de barras horizontal**: `category_counts` (top 10), eixo y =
  `product_type`, eixo x = `count`. ordene decrescente.
- **texto**: 1-2 linhas de contexto (dataset gymshark, kaggle, 44.831 produtos).

### página 2 — achado 1: outlier de preço
- **tabela**: `price_outliers` completa (12 linhas) — colunas handle,
  variant_title, sku, price. deixa visível que é sempre usd 1.000,00.
- **card**: "12 skus · 1 preço fixo · 2 produtos × 6 tamanhos".
- **gráfico de dispersão (scatter)** opcional: `powerbi_products`, eixo x =
  índice/handle, eixo y = price, destaque (`is_price_outlier` como legenda/cor)
  pra mostrar visualmente o quão isolados esses 12 pontos estão do resto.
- **caixa de texto (recomendação)**: "provável erro de cadastro — preço fixo
  independente de tamanho é atípico pra vestuário, e é ~36x a média do
  dataset. reportar ao catálogo de origem, não apenas filtrar como outlier
  de modelagem."

### página 3 — achado 2: funil de preenchimento de imagem
- **gráfico de funil** (visual nativo "funnel" do power bi): `image_fill_funnel`,
  categoria = `label` (já vem com prefixo numérico "1. mesmo handle" etc.
  pra manter a ordem certa — configure "sort by column" = `tier` se o power
  bi não respeitar a ordem alfabética automaticamente), valor = `products`.
- **card**: "121 de 128 imagens resolvidas (94,5%)" —
  `medida = DIVIDE(128 - CALCULATE(SUM(image_fill_funnel[products]), image_fill_funnel[tier]="unresolved"), 128)`.
- **caixa de texto (recomendação)**: "as 7 restantes são itens sob encomenda
  sem variante irmã (patch, gravação). não vale investir em mais uma camada
  de matching pra 0,02% dos produtos — resolver manualmente é mais barato."

### página 4 — achado 3: fragmentação de categoria
- **gráfico de barras agrupado**: `category_fragmentation`, eixo y = `norm`,
  eixo x = `count`, legenda/cor = `raw` — mostra os pares lado a lado
  (ex: "Mens T-Shirt" 4.430 vs "mens T-Shirt" 35).
- **card**: "91 valores brutos → 85 após normalizar" (`91 - 85 = 6 grupos
  duplicados`, contagem de linhas de `category_fragmentation` / 2).
- **caixa de texto (recomendação)**: "a mesma categoria conta como duas no
  relatório atual. correção pertence à entrada do dado (validação no
  cadastro/etl), não a mais uma regra de limpeza reativa."

## estilo

mantenha uma paleta só (2-3 cores), a mesma em todas as páginas — o tema
"gymshark" costuma usar preto/branco com um accent (a marca usa um verde
característico). destaque os achados no accent color e deixe o resto em
cinza neutro, pra guiar o olho pro que importa em cada página.
