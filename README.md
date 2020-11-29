# sped
Script simples que corrige alguns lançamentos de notas no SPED.

## Descrição

Esse script foi criado para corrigir algumas milhares de notas que foram
lançadas em uma classificação tributária errada.
A necessida era que, a partir do arquivo do SPED exportado, as notas na
classificação errada seriam corrigidas ao trocar o código que determina
o tipo lançado, gerando um novo arquivo a ser importado. Esse novo arquivo
era então importado no sistema, que corriga os totalizadores necessário.

Esse script também serviu de exemplo para ensinar um pouco de Python à
contadora que precisava fazer a correção (o que explica algumas varáveis
estarem em português).

## Como Usar

### Dependências

* Python 3

### Executando o script

```
python3 sped.py <SPED de entrada> <Nome do arquivo de saída>
```

