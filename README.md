# DataTrib Prospector API

Esta API coleta dados públicos das empresas brasileiras através da [API de dados abertos do governo federal](https://dadosabertos.rfb.gov.br/), os seleciona através de filtros pré-configurados, os transforma para modelagem de dados definida para o projeto e os disponibiliza via endpoints.

Mais informações sobre o projeto podem ser encontradas [aqui](https://violet-wax-9da.notion.site/DataTrib-1fb210a39c4346778d4701213dd46bdc).

### Endpoints Disponíveis

-   [Empresas](https://github.com/vitormlps/prospector-api/blob/dev/src/app/routers/routes/empresas.py)
-   [Estabelecimentos](https://github.com/vitormlps/prospector-api/blob/dev/src/app/routers/routes/estabelecimentos.py)
-   [Sócios](https://github.com/vitormlps/prospector-api/blob/dev/src/app/routers/routes/socios.py)
-   [Simples Nacional](https://github.com/vitormlps/prospector-api/blob/dev/src/app/routers/routes/simples_nacional.py)
-   [CNAEs](https://github.com/vitormlps/prospector-api/blob/dev/src/app/routers/routes/cnaes.py)
-   [Naturezas Jurídicas](https://github.com/vitormlps/prospector-api/blob/dev/src/app/routers/routes/naturezas_juridicas.py)
-   [Situações Cadastrais](https://github.com/vitormlps/prospector-api/blob/dev/src/app/routers/routes/situacoes_cadastrais.py)
-   [Motivos de Situações](https://github.com/vitormlps/prospector-api/blob/dev/src/app/routers/routes/motivos.py)
-   [Representantes Legais](https://github.com/vitormlps/prospector-api/blob/dev/src/app/routers/routes/representantes_legais.py)
-   [Qualificações](https://github.com/vitormlps/prospector-api/blob/dev/src/app/routers/routes/qualificacoes.py)
-   [Logradouros](https://github.com/vitormlps/prospector-api/blob/dev/src/app/routers/routes/logradouros.py)
-   [Contatos](https://github.com/vitormlps/prospector-api/blob/dev/src/app/routers/routes/contatos.py)
-   [Municipios](https://github.com/vitormlps/prospector-api/blob/dev/src/app/routers/routes/municipios.py)
-   [Paises](https://github.com/vitormlps/prospector-api/blob/dev/src/app/routers/routes/paises.py)
-   [Portes Empresas](https://github.com/vitormlps/prospector-api/blob/dev/src/app/routers/routes/portes_empresas.py)
-   [Matrizes/Filiais](https://github.com/vitormlps/prospector-api/blob/dev/src/app/routers/routes/matrizes_filiais.py)
-   [Faixas Etarias](https://github.com/vitormlps/prospector-api/blob/dev/src/app/routers/routes/faixas_etarias.py)

### Exemplo de dado retornado

Endpoint: /empresas (GET)

```json
[
	{
		"id": "3f39ecc3-d30f-4c47-8aee-a788873c3762",
		"cnpj": "00000000/3688-90",
		"razao_social": "BANCO DO BRASIL SA",
		"nome_fantasia": "CAVALHADA - PORTO ALEGRE (RS)",
		"capital_social": 120000000000,
		"natureza_juridica": "Sociedade de Economia Mista",
		"cnae": "Bancos múltiplos, com carteira comercial",
		"cnaes_secundarios": "6499999",
		"porte_empresa": "Demais",
		"situacao_cadastral": "Ativa",
		"motivo": "SEM MOTIVO",
		"qualificacao": "Diretor",
		"cep": "91910180",
		"municipio": "PORTO ALEGRE/RS",
		"opcao_simples": false,
		"data_opcao_simples": "2007-07-01T00:00:00",
		"data_exclusao_simples": "2007-07-01T00:00:00"
	}
]
```
