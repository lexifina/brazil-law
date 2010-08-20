ANEXO ÚNICO
LEIAUTE DO ARQUIVO DA DECLARAÇÃO
Declaração de Serviços Médicos e Saúde - Dmed
1.Regra Geral.
2. Estrutura de Arquivo:
2.1. Exemplo de estrutura de declarante Pessoa Jurídica.
3. Leiaute:
3.1. Registro de informação da declaração (identificador Dmed);
3.2. Registro do responsável pelo preenchimento(identificador RESPO);
3.3. Registro de informação do declarante pessoa jurídica (identificador DECPJ);
3.4. Registro de informação da operadora de plano privado de assistência à saúde(identificador OPPAS);
3.5. Registro de informação do titular do plano (identificador TOP);
3.6. Registro de informação de reembolso do titular do plano (identificador RTOP);
3.7. Registro de informação de dependente do titular (identificador DTOP);
3.8. Registro de informação de reembolso do dependente (identificador RDTOP);
3.9. Registro de informação do prestador de serviço de saúde (identificador PSS);
3.10. Registro de informação do responsável pelo pagamento ao rpestador do serviço de saúde (identificador RPPSS); 3.11. Registro de informação de beneficiário do serviço pago (identificador BRPPSS);
3.12. Registro identificador do término da declaração (identificador FIMDmed).
4. Tabela de relação de dependência.
1 - Regra geral: Esta
Esta seção apresenta as regras que devem ser respeitadas em todos os arquivos gerados, quando não excepcionadas por regra específica referente a um dado registro e explicitada em suas observações.
Nº Regra de preenchimento Descrição 1 Formato dos campos Alfanumérico (C): representados por "C" - todos os caracteres, excetuados o caractere "|" (pipe ou barra vertical, caractere 124 da Tabela ASCII); Numérico (N): representados por "N" - pode conter apenas os valores de "0" a "9". 2 Campos numéricos (D) cujo conteúdo representa data Devem ser informados conforme o padrão ano, mês, dia (AAAAMMDD), excluindo-se quaisquer caracteres de separação (tais como "." (ponto), "/" (barra inclinada), "-" (hífen), etc.). 3 Campos numéricos (N) cujo conteúdo representa ano Devem ser informados conforme o padrão "ano"(AAAA). 4 Campos numéricos com número de inscrição Os campos numéricos com número de inscrição (CNPJ, CPF, CNES e ANS) deverão ser informados com todos os dígitos, inclusive os zeros (0) à esquerda; As máscaras (caracteres especiais de formatação, tais como "." (ponto), "/" (barra inclinada), "-" (hífen), etc.) não devem ser informadas. 5 Campos numéricos referentes a valores monetários Devem ser informados com até 9 posições, representando 7 posições inteiras e 2 decimais; Os zeros não significativos não devem ser informados; Os caracteres ' .' (ponto) e ' ,' (vírgula) não devem ser informados. 6 Campos alfanuméricos com números ou códigos de identificação Os campos com conteúdo alfanumérico nos quais se faz necessário registrar números ou códigos de identificação (Ex.: Cadastro Nacional de Estabelecimentos de Saúde - CNES) deverão seguir a regra de formação e tamanho definidos pelo respectivo órgão regulador; As máscaras (caracteres especiais de formatação, tais como "." (ponto), "/" (barra inclinada), "-" (hífen), etc.) não devem ser informadas. 7 Formação dos campos Ao final de cada campo (incluído o último de cada registro) deve ser inserido o caractere delimitador "|" (pipe ou barra vertical: caractere 124 da Tabela ASCII); O caractere delimitador "|" (pipe) não deve ser incluído como parte integrante do conteúdo de quaisquer campos numéricos, datas ou alfanuméricos; Na ausência de informação, o campo vazio (campo sem conteúdo; nulo e com valor zero) deverá ser iniciado com caractere "|" e imediatamente encerrado com o mesmo caractere "|" delimitador de campo. 8 Formação dos registros Cada registro deve necessariamente ocupar apenas uma linha no arquivo. 9 Preenchimento dos campos Preenchimento fixo: o campo deve ser preenchido com o tamanho exato; Preenchimento variável: o campo pode ter variação de tamanho de preenchimento.
[arquivo anexo: 16033a.htm]
2 - Estrutura de arquivo:
2.1. - Exemplo de estrutura de declarante Pessoa Jurídica:
Dmed - Declaração de serviços médicos e de saúde;
RESPO - Responsável pelo preenchimento;
DECPJ - Declarante pessoa jurídica;
OPPAS - Operadora de plano privado de assistência à saúde;
TOP - Titular do plano; RTOP - Reembolso do titular do plano;
DTOP - Dependente do titular; RDTOP - Reembolso do dependente;
PSS - Prestador de serviço de saúde; RPPSS - Responsável pelo pagamento ao prestador do serviço de saúde;
BRPPSS - Beneficiário do serviço pago;
FIMDmed - Término da declaração.
3 - Leiaute do arquivo:
3.1. Registro de informação da declaração (identificador Dmed):
Regras de validação do registro: - Registro obrigatório no arquivo; - Deve ser o 1º (primeiro) registro no arquivo; - Ocorre somente uma vez no arquivo. Ordem Campo Formato Preenchimento Tamanho Valores Válidos Obrigatório 1 Identificador de registro C Fixo 4 Dmed Sim 2 Ano-referência N Fixo 4 2011 Sim 3 Ano-calendário N Fixo 4 2010 ou 2011 Sim 4 Indicador de retificadora C Fixo 1 S - Retificadora N - Original Sim 5 Número do recibo N Fixo 12 - Não 6 Identificador de estrutura do leiaute C Fixo 6 L1101M Sim Observações: Ordem Campo Descrição 5 Número do recibo Se a declaração for original, não preencher; Se a declaração for retificadora, deverá ser preenchido com o número do recibo da última declaração entregue, se declarante não transmitir a declaração com assinatura digital.
[arquivo anexo: 16033b.htm]
3.2. - Registro do Responsável pelo preenchimento (identificador RESPO):
Regras de validação do registro: - Registro obrigatório no arquivo; - Deve ser o 2º (segundo) registro no arquivo; - Ocorre somente uma vez no arquivo. Ordem Campo Formato Preenchimento Tamanho Valores Válidos Obrigatório 1 Identificador de registro C Fixo 5 RESPO Sim 2 CPF N Fixo 11 - Sim 3 Nome C Variável 60 - Sim 4 DDD N Fixo 2 - Sim 5 Telefone N Fixo 8 - Sim 6 Ramal N Variável 6 - Não 7 Fax N Fixo 8 - Não 8 Correio eletrônico C Variável 50 - Não
[arquivo anexo: 16033c.htm]
3.3. Registro de informação do declarante pessoa jurídica (identificador DECPJ):
Regras de validação do registro: - Registro obrigatório no arquivo quando for declarante pessoa jurídica; - Deve ser o 3º (terceiro) registro no arquivo; - Ocorre somente uma vez no arquivo; Ordem Campo Formato Preenchimento Tamanho Valores Válidos Obrigatório 1 Identificador de registro C Fixo 5 DECPJ Sim 2 CNPJ N Fixo 14 - Sim 3 Nome empresarial C Variável 150 - Sim 4 Tipo do declarante N Fixo 1 1 - Prestador de serviço de saúde; 2 - Operadora de plano privado de assistência à saúde; 3 - Prestador de serviço de saúde e Operadora de plano privado de assistência a saúde. Sim 5 Registro ANS N Fixo 6 - Não 6 CNES N Fixo 7 - Não 7 CPF responsável perante o CNPJ N Fixo 11 - Sim 8 Indicador de situação da declaração C Fixo 1 S - Declaração de situação especial; N - Não é declaração de situação especial. Sim 9 Data do evento D Fixo 8 - Não Observações: Ordem Campo Descrição 5 REGISTRO ANS Agência Nacional de Saúde Suplementar - ANS; Preenchimento obrigatório se campo de ordem 4 - Tipo do declarante igual a "2" ou "3". 6 CNES Cadastro Nacional de Estabelecimentos de Saúde - CNES. 9 Data do evento Preenchimento obrigatório se campo de ordem 8 - Indicador de situação da declaração igual a "S".
[arquivo anexo: 16033d.htm]
3.4. Registro de informação da operadora de plano privado de assistência à saúde (identificador OPPAS):
Regras de validação do registro: - Ocorre caso o declarante seja operadora de plano privado de assistência à saúde. Ordem Campo Formato Preenchimento Tamanho Valores Válidos Obrigatório 1 Identificador de registro C Fixo 5 OPPAS Sim Observações: Ordem Campo Descrição 1 Identificador de registro Preenchimento obrigatório se o campo de ordem 4 - Tipo do Declarante, do registro DECPJ igual a "2"; Preenchimento opcional se o campo de ordem 4 - Tipo do Declarante, do registro DECPJ igual a "3", e o declarante não exerceu atividades de Operadora de Plano Privado de Assistência à Saúde no ano-calendário.
[arquivo anexo: 16033e.htm]
3.5. Registro de informação do titular do plano (identificador TOP):
Regras de validação do registro: - Deve estar classificado em ordem crescente por CPF do titular; - Deve estar associado ao registro do tipo OPPAS. Ordem Campo Formato Preenchimento Tamanho Valores Válidos Obrigatório 1 Identificador de registro C Fixo 3 TOP Sim 2 CPF do titular N Fixo 11 - Sim 3 Nome C Variável 60 - Sim 4 Valor pago no ano com o titular N Variável 9 > 0 Sim
[arquivo anexo: 16033f.htm]
3.6. Registro de informação de reembolso do titular do plano (identificador RTOP):
Regras de validação do registro: - Deve estar classificado em ordem crescente por CPF/CNPJ do prestador de serviço (primeiro os CPFs e depois os CNPJ); - Deve estar associado ao registro do tipo TOP; - Só deverá constar o registro se houver valor de reembolso do ano-calendário ou de anos-calendários anteriores. Ordem Campo Formato Preenchimento Tamanho Valores Válidos Obrigatório 1 Identificador de registro C Fixo 4 RTOP Sim 2 CPF/CNPJ do prestador de serviço N Variável 14 CPF com 11 dígitos; CNPJ com 14 dígitos. Sim 3 Nome/Nome empresarial do prestador de serviço C Variável 150 Nome da pessoa física até 60 posições. Nome empresarial da pessoa jurídica até 150 posições. Sim 4 Valor do reembolso do ano-calendário N Variável 9 - Não 5 Valor do reembolso de anos anteriores N Variável 9 - Não Observações: Ordem Campo Descrição 4 Valor do reembolso do ano-calendário Valores reembolsados no ano-calendário, referentes a pagamentos de serviços prestados no ano-calendário. 5 Valor do reembolso de anos anteriores Valores reembolsados no ano-calendário referentes a pagamentos de serviços prestados em anos anteriores.
[arquivo anexo: 16033g.htm]
3.7. Registro de informação de dependente do titular (identificador DTOP):
Regras de validação do registro: - Deve estar classificado em ordem crescente por CPF e Data de nascimento do dependente; - Deve estar associado ao registro do tipo TOP. Ordem Campo Formato Preenchimento Tamanho Valores Válidos Obrigatório 1 Identificador de registro C Fixo 4 DTOP Sim 2 CPF do dependente N Fixo 11 - Não 3 Data de Nascimento D Fixo 8 - Não 4 Nome C Variável 60 Sim 5 Relação de Dependência N Fixo 2 Conforme Tabela de Relação de Dependência Não 6 Valor pago no ano com o dependente N Variável 9 Maior que zero Sim Observações: Ordem Campo Descrição 2 CPF do dependente Preenchimento obrigatório para maiores de 18 anos até 31 de dezembro de 2010. 3 Data de nascimento Preenchimento obrigatório para menores de 18 anos até 31 de dezembro de 2010, que não tenham informado o CPF.
[arquivo anexo: 16033h.htm]
3.8. Registro de informação de reembolso do dependente (identificador RDTOP):
Regras de validação do registro: - Deve estar classificado em ordem crescente por CPF/CNPJ do prestador de serviço (primeiro os CPF e depois os CNPJ); - Deve estar associado ao registro do tipo DTOP; - Só deverá constar o registro se houver valor de reembolso do ano-calendário e de anos-calendários anteriores. Ordem Campo Formato Preenchimento Tamanho Valores Válidos Obrigatório 1 Identificador de registro C Fixo 5 RDTOP Sim 2 CPF/CNPJ do prestador de serviço N Variável 14 CPF com 11 dígitos; CNPJ com 14 dígitos. Sim 3 Nome/Nome Empresarial do prestador de serviço C Variável 150 Nome da pessoa física até 60 posições; Nome empresarial da pessoa jurídica até 150 posições. Sim 4 Valor do reembolso do ano-calendário N Variável 9 - Não 5 Valor do reembolso de anos anteriores N Variável 9 - Não Observações: Ordem Campo Descrição 4 Valor do reembolso do ano-calendário Valores reembolsados no ano-calendário, referentes a pagamentos de serviços prestados no ano-calendário. 5 Valor do reembolso de anos anteriores Valores reembolsados no ano-calendário referentes a pagamentos de serviços prestados em anos anteriores.
[arquivo anexo: 16033i.htm]
3.9. Registro de informação do prestador de serviço de saúde (identificador PSS):
Regras de validação do registro: - Ocorre caso o declarante seja prestador de serviço de saúde. Ordem Campo Formato Preenchimento Tamanho Valores Válidos Obrigatório 1 Identificador de registro C Fixo 3 PSS Sim Observações: Ordem Campo Descrição 1 Identificador de registro Preenchimento obrigatório se o campo de ordem 4 - Tipo do Declarante, do registro DECPJ igual a "1"; Preenchimento opcional se o campo de ordem 4 - Tipo do Declarante, do registro DECPJ igual a "3", e o declarante não exerceu atividades de Prestador de Serviços de Saúde no ano-calendário.
[arquivo anexo: 16033j.htm]
3.10. Registro de informação do responsável pelo pagamento ao prestador do serviço de saúde (identificador RPPSS):
Regras de validação do registro: - Deve estar classificado em ordem crescente por CPF do responsável pelo pagamento; - Deve estar associado ao registro do tipo PSS. Ordem Campo Formato Preenchimento Tamanho Valores Válidos Obrigatório 1 Identificador de registro C Fixo 5 RPPSS Sim 2 CPF do responsável pelo pagamento N Fixo 11 - Sim 3 Nome C Variável 60 - Sim 4 Valor pago no ano pelo responsável em benefício próprio N Variável 9 - Não
[arquivo anexo: 16033l.htm]
3.11. Registro de informação de beneficiário do serviço pago (identificador BRPPSS):
Regras de validação do registro: - Deve estar classificado em ordem crescente por CPF e Data de nascimento do beneficiário; - Deve estar associado ao registro do tipo RPPSS. Ordem Campo Formato Preenchimento Tamanho Valores Válidos Obrigatório 1 Identificador de registro C Fixo 6 BRPPSS Sim 2 CPF do beneficiário N Fixo 11 - Não 3 Data de nascimento D Fixo 8 - Não 4 Nome C Variável 60 - Sim 5 Valor pago no ano com o beneficiário N Variável 9 >0 Sim Observações: Ordem Campo Descrição 3 Data de nascimento Preenchimento obrigatório para o beneficiário do serviço de saúde que não informar o número do CPF quando da prestação do serviço.
[arquivo anexo: 16033m.htm]
3.12. Registro identificador do término da declaração (identificador FIMDmed):
Regras de validação do registro: - Registro obrigatório no arquivo; - Deve ser o último registro no arquivo; - Ocorre somente uma vez no arquivo. Ordem Campo Formato Preenchimento Tamanho Valores Válidos Obrigatório 1 Identificador de registro C Fixo 7 FIMDmed Sim
[arquivo anexo: 16033n.htm]
4 - Tabela de relação de dependência:
Código Descrição 03 cônjuge/companheiro 04 filho/filha 06 enteado/enteada 08 pai/mãe 10 agregado/outros
[arquivo anexo: 16033o.htm]
