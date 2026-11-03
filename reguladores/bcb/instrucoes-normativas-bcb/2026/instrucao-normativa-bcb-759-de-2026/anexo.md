ANEXO À INSTRUÇÃO NORMATIVA BCB Nº 759, DE 9 DE JULHO DE 2026
Manual de Escopo de Dados e Serviços do Open Finance Versão 8.0
Sumário das alterações
Data
Versão
Descrição das alterações
9/7/2026
8.0
Inclusão de dados e escopo referentes ao serviço de portabilidade de crédito (seção 8).
Termos de Uso
Este manual detalha os requisitos técnicos para a implementação dos elementos necessários à operacionalização do Open Finance, complementando a regulamentação vigente sobre o tema.
O manual será revisto e atualizado periodicamente a fim de assegurar a compatibilidade com a regulamentação, bem como para incorporar os aprimoramentos decorrentes da evolução do Open Finance e da tecnologia.
Informações mais detalhadas e exemplos da aplicação deste manual poderão ser encontradas nos guias e tutoriais disponíveis no Portal do Open Finance no Brasil, na Área do Desenvolvedor.
Sugestões, críticas ou pedidos de esclarecimento de dúvidas relativas ao conteúdo deste documento podem ser enviados ao Banco Central do Brasil por meio dos canais institucionais dessa autarquia.
Referências
As especificações constantes deste manual baseiam-se, referenciam e complementam, quando aplicável, os seguintes documentos e elementos:
I - Resolução Conjunta nº 1, de 4 de maio de 2020;
II - Circular nº 4.015, de 4 de maio de 2020;
III - Resolução BCB nº 32, de 29 de outubro de 2020;
IV - Resolução BCB nº 1, de 12 de agosto de 2020;
V - Documento 3040 (Dados de Risco de Crédito);
VI - Resolução CNSP nº 415, de 20 de julho de 2021;
VII - Circular Susep nº 635, de 20 de julho de 2021;
VIII - Lei nº 13.709, ​​de 14 de agosto de 2018 (Lei Geral de Proteção de Dados Pessoais - LGPD);
IX - ISO 3166;
X - ISO 4217; e
XI - Portal do Open Finance no Brasil.
Os atos normativos de competência do Conselho Monetário Nacional ou do Banco Central do Brasil podem ser acessados no sítio eletrônico do Banco Central do Brasil na internet (www.bcb.gov.br), por meio da opção de "Busca de normas".
1. Introdução
Os dados e serviços objeto de compartilhamento representam parte primordial do Open Finance, pois serão determinantes para o grau de utilidade e de interesse no Open Finance pela sociedade. Desse modo, garantir a qualidade, disponibilidade e integridade desses dados e serviços é fundamental para construir a confiança no Open Finance.
A Resolução Conjunta nº 1, de 4 de maio de 2020, estabelece a obrigatoriedade de compartilhamento de dados de produtos e serviços disponibilizados pelas instituições a seus clientes, enquanto a Circular nº 4.015, de 4 de maio de 2020, disciplina o escopo desses dados.
Este manual foi elaborado para especificar o detalhamento e a padronização mínimos necessários para o compartilhamento. Neste sentido, estão relacionados os campos nas tabelas a seguir com informações adicionais e descrição de atributos, quando pertinentes. Para a implementação das Application Programming Interface (APIs) nos termos requeridos pela regulamentação vigente, orientações detalhadas de caráter técnico deverão ser disponibilizadas no Portal do Open Finance no Brasil.
Os dados listados neste manual são de implementação obrigatória, de acordo com a Circular nº 4.015, de 2020, e são traduzidos para a especificação técnica conforme análise e deliberação da Estrutura de Governança do Open Finance, podendo ser consolidados ou expandidos para múltiplos campos. Quando determinados dados forem considerados como opcionais, de acordo com as especificações técnicas da Estrutura de Governança do Open Finance, as instituições participantes somente poderão deixar de encaminhar os dados para os quais houver impossibilidade devido à sua inexistência, não havendo discricionaridade nesse encaminhamento.
Cabe ressaltar que as instituições participantes do Open Finance possuem autonomia para decidir sobre o compartilhamento de dados adicionais aos relacionados neste manual, desde que respeitado o consentimento prévio do cliente em relação aos dados pessoais e observada a legislação e regulamentação vigentes. O consentimento prévio do cliente, para finalidades e prazos determinados, também é exigido para o compartilhamento dos dados cadastrais e transacionais de clientes previstos neste manual.
Este manual também especifica os dados mínimos necessários para o compartilhamento do serviço de iniciação de transação de pagamento, bem como detalha o escopo das modalidades de pagamento que devem ser implementados no Open Finance, conforme cronograma estabelecido pelo Banco Central do Brasil. Com relação aos dados, além das informações mínimas para a iniciação de transação de pagamento, devem ser informados, de forma geral, os dados dispostos nos regulamentos ou instrumentos que disciplinam o funcionamento do arranjo de pagamento referente à respectiva transação de pagamento e demais dados estabelecidos nas especificações disponíveis no Portal do Open Finance no Brasil.
Para os aspectos operacionais do Open Finance, é necessário consultar fontes complementares de informação, disponíveis no Portal do Open Finance no Brasil, no qual poderão ser encontradas as especificações relativas à visão de alto nível, o dicionário de dados, no caso o tipo, formato, tamanho e demais atributos pertinentes aos campos de dados, bem como os agrupamentos de dados e os códigos das APIs.
Finalmente, cabe destacar que o fomento à concorrência entre instituições financeiras, de pagamento e demais instituições autorizadas a funcionar pelo Banco Central do Brasil, por meio da comparabilidade das informações compartilhadas, é um dos objetivos que se pretende alcançar com o Open Finance. Assim, todas as informações constantes deste manual devem ser prestadas em conformidade com a padronização estabelecida na regulamentação vigente, quando houver.
2. Dados sobre Canais de Atendimento
Nos termos da regulamentação em vigor, os dados sobre canais de atendimento devem abranger, no mínimo, os campos listados nas tabelas a seguir.
2.1 Dependências próprias
Dado
Campo
Esclarecimentos adicionais
Identificação
Marca
Nome da marca reportada pelo participante do Open Finance.
O conceito a que se refere a marca é, em essência, uma promessa das instituições em fornecer uma série específica de atributos, benefícios e serviços uniformes aos clientes.
Nome da instituição
Nome da instituição responsável pela dependência.
CNPJ da instituição
Número completo do CNPJ da instituição responsável pela dependência.
Nome da dependência
CNPJ da dependência
Código identificador da dependência
Dígito verificador da dependência
Campo adicional para URL (CNPJs)
URL de link, para lista complementar, com os nomes e CNPJs agrupados no caso de instituições oferecerem produtos e serviços com as mesmas características.
Tipo de dependência
Tipo de dependência, segundo a classificação estabelecida pela regulamentação que dispõe sobre a instalação, no País, de dependências de instituições financeiras e demais instituições autorizadas a funcionar pelo Banco Central do Brasil.
Código da agência vinculada ao posto de atendimento
Data de abertura da dependência
Localização
Endereço completo
Complemento
Bairro
Município
Código IBGE do município
7 dígitos (o último é um código verificador).
Sigla da Unidade da Federação
CEP
País
Código do país
De acordo com o código "alpha3" do ISO-3166.
Latitude
Entre -90 e 90. Formato numérico, 2 casas antes da vírgula, 11 posições.
Longitude
Entre -180 e 180. Formato numérico, 3 casas antes da vírgula, 11 posições.
Forma de acesso
Horário de abertura
Horário de encerramento
Dias de funcionamento
Indicador de restrição de acesso
Tipo de telefone
Fixo ou celular.
DDI
DDD
Número de telefone
Serviços prestados
Nomes dos serviços prestados
Relação dos serviços efetivamente prestados, discriminados no Subitem 2.5.2 deste manual.
Códigos dos serviços prestados
Códigos dos serviços efetivamente prestados, discriminados no Subitem 2.5.2 deste manual.
2.2 Correspondentes no País
Dado
Campo
Esclarecimentos adicionais
Identificação
Marca
Nome da marca reportada pelo participante do Open Finance.
O conceito a que se refere a marca é, em essência, uma promessa das instituições em fornecer uma série específica de atributos, benefícios e serviços uniformes aos clientes.
Nome da instituição titular
Nome da instituição responsável pelo correspondente no País.
CNPJ da instituição titular
Número completo do CNPJ da instituição responsável pelo correspondente no País.
Nome do contratante
CNPJ do contratante
Nome do correspondente no País
Nome do conglomerado do correspondente no País
CNPJ do correspondente no País
Substabelecimento
1. não, 2. sim.
Localização
Endereço completo
Complemento
Bairro
Município
Código IBGE do município
7 dígitos (o último é um código verificador).
Sigla da Unidade da Federação
CEP
País
Código do país
De acordo com o código "alpha3" do ISO-3166.
Latitude
Entre -90 e 90. Formato numérico, 2 casas antes da vírgula, 11 posições.
Longitude
Entre -180 e 180. Formato numérico, 3 casas antes da vírgula, 11 posições.
Forma de acesso
Horário de abertura
Horário de encerramento
Dias de funcionamento
Indicador de restrição de acesso
Tipo de telefone
Fixo ou celular.
DDI
DDD
Número de telefone
Serviços prestados
Nomes dos serviços prestados
Relação dos serviços efetivamente prestados, discriminados no Subitem 2.5.3 deste manual.
Códigos dos serviços prestados
Códigos dos serviços efetivamente prestados, discriminados no Subitem 2.5.3 deste manual.
2.3 Canais eletrônicos
Dado
Campo
Esclarecimentos adicionais
Canal
Marca
Nome da marca reportada pelo participante do Open Finance.
O conceito a que se refere a marca é, em essência, uma promessa das instituições em fornecer uma série específica de atributos, benefícios e serviços uniformes aos clientes.
Nome da instituição
Nome da instituição responsável pelo canal eletrônico.
CNPJ da instituição
Campo adicional para URL (CNPJs)
URL de link, para lista complementar, com os nomes e CNPJs agrupados no caso de instituições oferecerem produtos e serviços com as mesmas características.
Tipo de canal
Internet banking, mobile banking ou chat.
Forma de acesso
Tipo de acesso
1. URL para acesso ao internet banking, 2. URL para aquisição do app, 3. URL para chat, 4. outros.
Serviços prestados
Nomes dos serviços prestados
Relação dos serviços efetivamente prestados, discriminados no Subitem 2.5.2 deste manual.
Códigos dos serviços prestados
Códigos dos serviços efetivamente prestados, discriminados na Subitem 2.5.2 deste manual.
2.4 Outros canais disponíveis
2.4.1 Canais telefônicos
Dado
Campo
Esclarecimentos adicionais
Canal
Marca
Nome da marca reportada pelo participante do Open Finance.
O conceito a que se refere a marca é, em essência, uma promessa das instituições em fornecer uma série específica de atributos, benefícios e serviços uniformes aos clientes.
Nome da instituição
Nome da instituição responsável pelo canal telefônico.
CNPJ da instituição
Campo adicional para URL (CNPJs)
URL de link, para lista complementar, com os nomes e CNPJs agrupados no caso de instituições oferecerem produtos e serviços com as mesmas características.
Tipo de canal
Central telefônica, SAC e ouvidoria.
Forma de acesso
DDI
DDD
Número de telefone
Tipo de acesso
1. central telefônica, 2. SAC, 3. ouvidoria, 4. outros.
Serviços prestados
Nomes dos serviços prestados
Relação dos serviços efetivamente prestados, discriminados no Subitem 2.5.2 deste manual.
Códigos dos serviços prestados
Códigos dos serviços efetivamente prestados, discriminados no Subitem 2.5.2 deste manual.
2.4.2 Terminais de autoatendimento compartilhados
No momento, é facultativa a implementação de endpoint para o compartilhamento dos dados relativos aos terminais de autoatendimento de terceiros compartilhados.
Dado
Campo
Esclarecimentos adicionais
Identificação
Marca
Nome da marca reportada pelo participante do Open Finance.
O conceito a que se refere a marca é, em essência, uma promessa das instituições em fornecer uma série específica de atributos, benefícios e serviços uniformes aos clientes.
Nome da instituição titular
Nome da instituição responsável pela dependência.
CNPJ da instituição titular
Número completo do CNPJ da instituição responsável pela dependência.
Campo adicional para URL (CNPJs)
URL de link, para lista complementar, com os nomes e CNPJs agrupados no caso de instituições oferecerem produtos e serviços com as mesmas características.
Nome do proprietário
Localização
Endereço completo
Complemento
Bairro
Município
Código IBGE do município
7 dígitos (o último é um código verificador).
Sigla da Unidade da Federação
CEP
País
Código do país
De acordo com o código "alpha3" do ISO-3166.
Latitude
Entre -90 e 90. Formato numérico, 2 casas antes da vírgula, 11 posições.
Longitude
Entre -180 e 180. Formato numérico, 3 casas antes da vírgula, 11 posições.
Forma de acesso
Horário de abertura
Horário de encerramento
Dias de funcionamento
Indicador de restrição de acesso
Serviços prestados
Nomes dos serviços prestados
Relação dos serviços efetivamente prestados, discriminados no Subitem 2.5.2 deste manual.
Códigos dos serviços prestados
Códigos dos serviços efetivamente prestados, discriminados no Subitem 2.5.2 deste manual.
2.5 Classificação de dependências e serviços prestados
2.5.1 Tipos de dependências
Os tipos de dependências das instituições autorizadas a funcionar pelo Banco Central do Brasil, conforme a regulamentação em vigor que dispõe sobre a instalação, no País, de dependências de instituições financeiras e demais instituições autorizadas a funcionar pelo Banco Central do Brasil, e que podem ser compartilhados no Open Finance, são os seguintes:
I - Agência;
II - Posto de Atendimento (PA);
III - Posto de Atendimento Eletrônico (PAE); e
IV - Unidade Administrativa Desmembrada (UAD).
2.5.2 Tipos de serviços prestados por agências ou postos de atendimento
A relação de serviços prestados por agências ou postos de atendimento deve estar em conformidade com a estabelecida pela regulamentação aplicável à sua divulgação na forma de dados abertos, discriminando, no mínimo, o seguinte:
I - abertura de contas de depósitos ou de pagamento pré-paga;
II - saque de moeda em espécie;
III - recebimentos, pagamentos de qualquer natureza;
IV - transferências eletrônicas visando à movimentação de contas de depósitos ou de pagamento de titularidade de clientes;
V - consulta a saldos e extratos de contas de depósitos e de contas de pagamento;
VI - aplicações e resgates de investimentos;
VII - execução ativa e passiva de ordens de pagamento por solicitação de clientes e usuários;
VIII - depósitos de moeda em espécie e de cheques;
IX - operações de crédito, bem como outros serviços prestados para o acompanhamento da operação;
X - cartão de crédito;
XI - seguros;
XII - operações de arrendamento mercantil;
XIII - abertura de conta de pagamento pós-paga;
XIV - compra e venda de moeda estrangeira em espécie;
XV - compra e venda de cheque ou cheque de viagem, bem como carga de moeda estrangeira em cartão pré-pago;
XVI - compra e venda de ouro; e
XVII - outros produtos ou serviços.
Os códigos correspondentes aos serviços relacionados deverão ser padronizados para observância comum por todas as instituições participantes.
2.5.3 Tipos de serviços prestados por correspondentes no País
As atividades de atendimento realizadas por correspondentes no País, conforme regulamentação vigente, são as seguintes:
I - recepção e encaminhamento de propostas de abertura de contas de depósitos e de pagamento mantidas pela instituição contratante;
II - realização de recebimentos, pagamentos e transferências eletrônicas visando à movimentação de contas de depósitos e de pagamento de titularidade de clientes mantidas pela instituição contratante;
III - recebimentos e pagamentos de qualquer natureza, e outras atividades decorrentes da execução de contratos e convênios de prestação de serviços mantidos pela instituição contratante com terceiros;
IV - execução ativa e passiva de ordens de pagamento cursadas por intermédio da instituição contratante por solicitação de clientes e usuários;
V - recepção e encaminhamento de propostas de operações de crédito e de arrendamento mercantil concedidas pela instituição contratante, bem como outros serviços prestados para o acompanhamento da operação;
VI - recebimentos e pagamentos relacionados a letras de câmbio de aceite da instituição contratante; e
VII - realização de operações de câmbio de responsabilidade da instituição contratante.
Os códigos correspondentes aos serviços relacionados deverão ser padronizados para observância comum por todas as instituições participantes.
3. Dados sobre produtos e serviços disponíveis à contratação
3.1 Contas de depósitos à vista, de poupança e de pagamento pré-pagas
Dado
Campo
Esclarecimentos adicionais
Identificação
Marca
Nome da marca reportada pelo participante do Open Finance.
O conceito a que se refere a marca é, em essência, uma promessa das instituições em fornecer uma série específica de atributos, benefícios e serviços uniformes aos clientes.
Nome da instituição
Nome da instituição responsável pela conta.
CNPJ da instituição
Campo adicional para URL (CNPJs)
URL de link, para lista complementar, com os nomes e CNPJs agrupados no caso de instituições oferecerem produtos e serviços com as mesmas características.
Tipo de conta
Conta de depósito à vista, conta de depósito de poupança ou conta de pagamentos pré-paga, nos termos na regulamentação vigente.
Tarifas cobradas por serviços avulsos
Denominação
Relação dos serviços objeto de cobrança de tarifas, conforme regulamentação vigente.
Siglas
Conforme regulamentação vigente.
Fatos geradores de cobrança
Conforme regulamentação vigente.
Moeda
De acordo com o ISO 4217.
Valor
Distribuição de frequência relativa dos valores sobre cobrança de tarifas pela prestação dos serviços prioritários, de serviços no âmbito do arranjo de pagamento Pix e do serviço de iniciação de transação de pagamento, informados nos termos da Resolução BCB nº 32, de 2020.
Pacotes de serviços
Denominação dos pacotes de serviços
Conforme regulamentação vigente.
Nome dos serviços incluídos
Conforme regulamentação vigente.
Fatos geradores de cobrança
Conforme regulamentação vigente.
Moeda
De acordo com o ISO 4217.
Eventos previstos no pacote de serviços
Quantidade mensal.
Moeda
De acordo com o ISO 4217.
Tarifa mensal
Distribuição de frequência relativa dos valores referentes à cobrança de tarifas, nos termos da Resolução BCB nº 32, de 2020.
Formas de movimentação
Formas de movimentação
1. movimentação eletrônica, 2. movimentação com cheque, 3. movimentação com cartão, 4. movimentação presencial.
Termos e condições contratuais
Saldo mínimo (moeda)
De acordo com o ISO 4217.
Saldo mínimo (valor)
Campo aberto.
Critérios de elegibilidade
Campo aberto.
Procedimentos de encerramento
Campo aberto (possibilidade de incluir URL).
Canais disponíveis para abertura e encerramento
Lista de canais
1. dependências próprias, 2. correspondentes no País, 3. internet banking, 4. mobile banking, 5. canais telefônicos, 6. chat, 7. outros.
Público-alvo
Lista de público-alvo
1. pessoa natural, 2. pessoa jurídica, 3. ambos.
Forma de remuneração e taxa de rendimento
Descrição da forma de remuneração
Informação conforme a regulamentação em vigor.
Percentual em favor do titular da conta de pagamento pré-paga
Campo aberto.
3.2 Contas de pagamento pós-pagas
Dado
Campo
Esclarecimentos adicionais
Identificação
Marca
Nome da marca reportada pelo participante do Open Finance.
O conceito a que se refere a marca é, em essência, uma promessa das instituições em fornecer uma série específica de atributos, benefícios e serviços uniformes aos clientes.
Nome da instituição
Nome da instituição responsável pela conta.
CNPJ da instituição
Campo adicional para URL (CNPJs)
URL de link, para lista complementar, com os nomes e CNPJs agrupados no caso de instituições oferecerem produtos e serviços com as mesmas características.
Denominação
Identificação do nome da conta de pagamento pós-paga (cartão).
Classificação
Categoria atribuída ao cartão de pagamento, sob uma certa denominação, que lhe agrega um conjunto de benefícios, diferenciando-o de acordo com o perfil do cliente.
Arranjo de pagamento
Instituidor do arranjo de pagamento.
Programa de benefícios e recompensas
Programa de benefícios ou recompensas
1. não, 2. sim.
Termos e condições do programa
Campo aberto (possibilidade de incluir URL).
Tarifas
Denominação
Conforme regulamentação vigente.
Siglas
Conforme regulamentação vigente.
Fatos geradores de cobrança
Conforme regulamentação vigente.
Moeda
De acordo com o ISO 4217.
Valor
Distribuição de frequência relativa dos valores referentes à cobrança de tarifas pela prestação de serviços prioritários relacionados à cartão de crédito, informados nos termos da Resolução BCB nº 32, de 2020.
Taxas de remuneração
Crédito rotativo (moeda)
De acordo com o ISO 4217.
Crédito rotativo (valor)
Distribuição de frequência relativa dos valores referentes ao crédito rotativo nos termos da Resolução BCB nº 32, de 2020.
Parcelamento de saldo devedor da fatura (moeda)
De acordo com o ISO 4217.
Parcelamento de saldo devedor da fatura
Distribuição de frequência relativa dos valores referentes ao crédito rotativo nos termos da Resolução BCB nº 32, de 2020.
Outras operações de crédito
1. saque na função crédito, 2. pagamento de contas, 3. outros.
Moeda
De acordo com o ISO 4217.
Público-alvo
Lista de público-alvo
1. pessoa natural, 2. pessoa jurídica, 3. ambos.
Termos e condições contratuais
Regra de pagamento mínimo de saldo devedor da fatura
Percentual do valor do saldo devedor da fatura.
Critérios de elegibilidade
Campo aberto (possibilidade de incluir URL).
Procedimentos de encerramento
Campo aberto (possibilidade de incluir URL).
3.3 Operações de crédito
3.3.1 Adiantamento a depositantes
Dado
Campo
Esclarecimentos adicionais
Identificação
Marca
Nome da marca reportada pelo participante do Open Finance.
O conceito a que se refere a marca é, em essência, uma promessa das instituições em fornecer uma série específica de atributos, benefícios e serviços uniformes aos clientes.
Nome da instituição
Nome da instituição concedente do adiantamento a depositantes.
CNPJ da instituição
Campo adicional para URL (CNPJs)
URL de link, para lista complementar, com os nomes e CNPJs agrupados no caso de instituições oferecerem produtos e serviços com as mesmas características.
Tarifas
Denominação
Conforme regulamentação vigente.
Siglas
Conforme regulamentação vigente.
Fatos geradores de cobrança
Conforme regulamentação vigente.
Moeda
De acordo com o ISO 4217.
Valor
Distribuição de frequência relativa dos valores referentes às tarifas cobradas pela prestação do serviço prioritário de concessão de adiantamento a depositante, nos termos da Resolução BCB nº 32, de 2020.
Taxas de juros remuneratórios
Referencial ou indexador
Tipos de taxas referenciais ou indexadores e percentuais adotados, conforme Anexo do Documento 3040.
Taxa nominal pré-fixada contratada
Distribuição de frequência relativa da parcela prefixada dos juros cobrados na situação de adimplência, em periodicidade mensal, de acordo com a Resolução BCB nº 32, de 2020.
Público-alvo
Lista de público-alvo
1. pessoa natural, 2. pessoa jurídica, 3. ambos.
Termos e condições contratuais
Termos e condições contratuais
Campo aberto (possibilidade de incluir URL).
3.3.2 Empréstimos
Dado
Campo
Esclarecimentos adicionais
Identificação
Marca
Nome da marca reportada pelo participante do Open Finance.
O conceito a que se refere a marca é, em essência, uma promessa das instituições em fornecer uma série específica de atributos, benefícios e serviços uniformes aos clientes.
Nome da instituição
Nome da instituição responsável pelos empréstimos.
CNPJ da instituição
Campo adicional para URL (CNPJs)
URL de link, para lista complementar, com os nomes e CNPJs agrupados no caso de instituições oferecerem produtos e serviços com as mesmas características.
Modalidades
Conforme Circular nº 4.015, de 2020, e Anexo do Documento 3040.
Tarifas
Denominação das tarifas
Conforme regulamentação vigente.
Siglas das tarifas
Conforme regulamentação vigente.
Fatos geradores de cobrança
Conforme regulamentação vigente.
Moeda
De acordo com o ISO 4217.
Valor
Distribuição de frequência relativa dos valores referentes às tarifas cobradas, nos termos da Resolução BCB nº 32, de 2020.
Taxas de juros remuneratórios
Referencial ou indexador
Tipos de taxas referenciais ou indexadores e percentuais adotados, conforme Anexo do Documento 3040.
Taxa nominal pré-fixada contratada
Distribuição de frequência relativa da parcela prefixada dos juros cobrados na situação de adimplência, em periodicidade mensal, de acordo com a Resolução BCB nº 32, de 2020.
Público-alvo
Lista de público-alvo
1. pessoa natural, 2. pessoa jurídica, 3. ambos.
Tipos de garantia exigíveis
Lista de tipos de garantias
Conforme Anexo do Documento 3040.
Termos e condições contratuais
Termos e condições contratuais
Campo aberto (possibilidade de incluir URL).
3.3.3 Direitos creditórios descontados
Dado
Campo
Esclarecimentos adicionais
Identificação
Marca
Nome da marca reportada pelo participante do Open Finance.
O conceito a que se refere a marca é, em essência, uma promessa das instituições em fornecer uma série específica de atributos, benefícios e serviços uniformes aos clientes.
Nome da instituição
Nome da instituição responsável pela operação de direitos creditórios descontados.
CNPJ da instituição
Campo adicional para URL (CNPJs)
URL de link, para lista complementar, com os nomes e CNPJs agrupados no caso de instituições oferecerem produtos e serviços com as mesmas características.
Modalidades
Conforme Circular nº 4.015, de 2020, e Anexo do Documento 3040.
Tarifas
Denominação
Conforme regulamentação vigente.
Siglas
Conforme regulamentação vigente.
Fatos geradores de cobrança
Conforme regulamentação vigente.
Moeda
De acordo com o ISO 4217.
Valor
Distribuição de frequência relativa dos valores referentes às tarifas cobradas, nos termos da Resolução BCB nº 32, de 2020.
Taxas de juros remuneratórios
Referencial ou indexador
Tipos de taxas referenciais ou indexadores e percentuais adotados, conforme Anexo do Documento 3040.
Taxa nominal pré-fixada contratada
Distribuição de frequência relativa da parcela prefixada dos juros cobrados na situação de adimplência, em periodicidade mensal, de acordo com a Resolução BCB nº 32, de 2020.
Público-alvo
Lista de público-alvo
1. pessoa natural, 2. pessoa jurídica, 3. ambos.
Tipos de garantia exigíveis
Lista de tipos de garantias
Conforme Anexo do Documento 3040.
Termos e condições contratuais
Termos e condições contratuais
Campo aberto (possibilidade de incluir URL).
3.3.4 Financiamentos
Dado
Campo
Esclarecimentos adicionais
Identificação
Marca
Nome da marca reportada pelo participante do Open Finance.
Nome da instituição
Nome da instituição responsável pelo financiamento.
CNPJ da instituição
Campo adicional para URL (CNPJs)
URL de link, para lista complementar, com os nomes e CNPJs agrupados no caso de instituições oferecerem produtos e serviços com as mesmas características.
Modalidades
Conforme Circular nº 4.015, de 2020 e Anexo do Documento 3040.
Tarifas
Denominação
Conforme regulamentação vigente.
Siglas
Conforme regulamentação vigente.
Fatos geradores de cobrança
Conforme regulamentação vigente.
Moeda
De acordo com o ISO 4217.
Valor
Distribuição de frequência relativa dos valores referentes às tarifas cobradas, nos termos da Resolução BCB nº 32, de 2020.
Taxas de juros remuneratórios
Referencial ou indexador
Tipos de taxas referenciais ou indexadores e percentuais adotados, conforme Anexo do Documento 3040.
Taxa nominal pré-fixada contratada
Distribuição de frequência relativa da parcela prefixada dos juros nominais cobrados na situação de adimplência, em periodicidade mensal, de acordo com a Resolução BCB nº 32, de 2020.
Público-alvo
Lista de público-alvo
1. pessoa natural, 2. pessoa jurídica, 3. ambos.
Tipos de garantia exigíveis
Lista de tipos de garantias
Conforme Anexo do Documento 3040.
Termos e condições contratuais
Termos e condições contratuais
Campo aberto (possibilidade de incluir URL).
3.4 Operações de câmbio
3.4.1 Valor efetivo total (VET) – Informações sobre os VETs praticados pela instituição nas operações de câmbio conforme previstas na regulamentação vigente.
Dado
Campo
Esclarecimentos adicionais
Identificação
Marca
Nome da marca reportada pelo participante do Open Finance.
Nome da instituição
Nome da instituição responsável pelas operações de câmbio.
CNPJ da instituição
VET
Tipo de operação de câmbio
Compra ou venda.
Moeda
Moeda estrangeira, de acordo com o modelo ISO 4217. Devem ser disponibilizadas, no mínimo, informações sobre as moedas USD e EUR.
Natureza-fato da operação
1. comércio exterior; 2. transportes; 3. seguros; 4. viagens internacionais; 5. transferências unilaterais; 6. serviços diversos; 7. rendas de capitais; 8. capitais brasileiros; 9. capitais estrangeiros; e 10. serviço de pagamento ou transferência internacional (eFX).
Forma de entrega da moeda estrangeira
1. espécie; 2. teletransmissão; 3. cartão pré-pago.
Faixa de valor da operação (equivalente em USD)
1. até US$200,00; 2. de US$200,01 a US$500,00; 3. de US$500,01 a US$1.000,00; 4. US$1.000,01 a US$3.000,00; 5. US$3.000,01 a US$10.000,00; 6. de US$10.000,01 a US$30.000,00; e 7. de US$30.000,01 a US$100.000,00.
Valor
VET calculado e expresso conforme regulamentação vigente.
Distribuição de frequência dos VETs, em periodicidade mensal, de acordo com a Resolução BCB nº 32, de 2020.
Público-alvo
Lista de público-alvo
1. pessoa natural; 2. pessoa jurídica.
3.4.2 Taxa de câmbio – Informações sobre as taxas de câmbio praticadas pela instituição no momento da consulta em operações com clientes para liquidação pronta, conforme regulamentação vigente.
Dado
Campo
Esclarecimentos adicionais
Identificação
Marca
Nome da marca reportada pelo participante do Open Finance.
Nome da instituição
Nome da instituição responsável pelas operações de câmbio.
CNPJ da instituição
Taxa de câmbio
Tipo de operação de câmbio
Compra ou venda.
Moeda
Moeda estrangeira, de acordo com o modelo ISO 4217. Devem ser disponibilizadas, no mínimo, informações sobre as moedas USD e EUR.
Natureza-fato da operação
1. comércio exterior; 2. transportes; 3. seguros; 4. viagens internacionais; 5. transferências unilaterais; 6. serviços diversos; 7. rendas de capitais; 8. capitais brasileiros; 9. capitais estrangeiros; e 10. serviço de pagamento ou transferência internacional (eFX).
Forma de entrega da moeda estrangeira
1. espécie; 2. teletransmissão; 3. cartão pré-pago.
Valor
Informação da taxa de câmbio praticada pela instituição no momento da consulta para uma operação de câmbio de US$500,00 (quinhentos dólares dos Estados Unidos) ou o seu equivalente em outras moedas.
Público-alvo
Lista de público-alvo
1. pessoa natural; 2. pessoa jurídica.
3.5 Serviços de credenciamento em arranjo de pagamento
Dado
Campo
Esclarecimentos adicionais
Taxas e tarifas por serviço
Denominação
Taxa de desconto.
Modalidade
Conta pós-paga (crédito), conta de depósitos (débito).
Fato gerador
Recebimento por meio de transação de arranjo de pagamento baseado em conta pós-paga (cartão de crédito), recebimento por meio de transação de arranjo de pagamento baseado em conta de depósitos (cartão de débito).
Valor
Distribuição de frequência relativa dos valores referentes às taxas de desconto cobradas, nos termos da Resolução BCB nº 32, de 2020.
Sigla identificadora
Sigla da tarifa cobrada sobre o serviço de credenciamento informado.
3.6 Contas de depósito a prazo e outros produtos com natureza de investimento
3.6.1 Produtos
Incluem-se no escopo mínimo desta subseção os produtos de investimento que permitam a contratação automática ou o regate automático em conta de livre movimentação de clientes.
3.6.1.1 Certificado de Depósito Bancário, Recibo de Depósito Bancário, Letra de Crédito Imobiliário e Letra de Crédito do Agronegócio
Dado
Campo
Esclarecimentos adicionais
Identificação
Marca
Nome da marca reportada pelo participante do Open Finance.
Nome da instituição
Razão social da instituição responsável pela distribuição do produto.
CNPJ da instituição
CNPJ da instituição responsável pela distribuição do produto.
Identificação e Características do produto
Nome da instituição
Razão social da instituição emissora do produto.
CNPJ da instituição
CNPJ da instituição emissora do produto.
Denominação do produto
Conforme regulamentação vigente.
Taxas, indicadores e característica de remuneração
Indexador
Índice utilizado como referência para a correção da rentabilidade ou rendimentos do ativo financeiro.
Taxa de remuneração na emissão
Taxa efetiva percebida no momento da emissão do título.
Condições de investimento e resgate
Data de vencimento
Data de vencimento do ativo financeiro.
Investimento inicial
Valor mínimo de investimento inicial.
Prazo de carência
Prazo a partir do qual passa a ser possível resgatar o investimento.
Liquidez
Capacidade de conversão do título em dinheiro (resgate ou recompra).
3.6.1.2 Cotas de fundo de investimento relativas a fundos de investimento classificados como cambial, multimercado, de renda fixa e de ações
Dado
Campo
Esclarecimentos adicionais
Identificação
Marca
Nome da marca reportada pelo participante do Open Finance.
Nome da instituição
Razão Social da instituição responsável pela distribuição do produto.
CNPJ da instituição
CNPJ da instituição responsável pela distribuição do produto.
Identificação do produto
Nome do fundo de investimento
Razão social do fundo de investimento.
CNPJ do fundo de investimento
Código ISIN
Código universal que identifica cada valor mobiliário ou instrumento financeiro, conforme Norma ISSO 6166.
Nome do administrador
Razão social da pessoa jurídica autorizada pela CVM para o exercício de administrador de carteiras de valores mobiliários e responsável pela administração do fundo de investimento.
CNPJ do administrador
Nome do gestor
Pessoa natural ou jurídica responsável pela gestão profissional dos ativos da carteira de valores mobiliários autorizado pela CVM.
CNPJ do gestor
Taxas
Taxa de administração
Taxa cobrada pelo administrador do fundo como remuneração pela prestação dos serviços de administração, gestão da carteira, e demais serviços necessários ao funcionamento do fundo.
Taxa de entrada
Taxa cobrada no momento da aplicação, que incide sobre o valor investido no fundo de investimento.
Taxa de saída
Taxa paga pelo cotista ao resgatar recursos de um fundo de investimento.
Taxa de performance
Taxa cobrada do fundo em função do resultado, conforme regras dispostas no regulamento do fundo de investimento.
Condições de investimento e resgate
Investimento inicial
Valor mínimo de investimento inicial.
Tipo de cota
Abertura ou fechamento.
Prazo de cotização da aplicação
Prazo em dias indicado no regulamento do fundo para a conversão das cotas em dinheiro.
Prazo de cotização para resgate
Prazo em dias indicada no regulamento do fundo para a conversão das cotas em dinheiro.
Prazo de pagamento do resgate
Prazo em dias do efetivo pagamento, pelo fundo, do valor líquido devido ao cotista que efetuou pedido de resgate.
Prazo de carência
Indica se o fundo estabelece um período em que o investidor não pode resgatar os recursos aplicados no fundo. Caso ocorra resgate antes do período, o investidor perderá a rentabilidade do período.
Tributação
Tipo de tributação
Indica se o tipo de tributação é de curto prazo, longo prazo ou variável.
3.6.2 Serviço de corretagem ou de agente de custódia
Conforme estabelecido pela Circular nº 4.015, de 2020, os campos relativos a esta subseção devem ser informados para os seguintes produtos: títulos públicos disponibilizados pelo Tesouro Direto; ações; cotas de fundos de índices listados em bolsa; debêntures; Certificados de Recebíveis Imobiliários; e Certificados de Recebíveis do Agronegócio.
Dado
Campo
Esclarecimentos adicionais
Identificação
Marca
Nome da marca reportada pelo participante do Open Finance.
Nome da instituição
Razão social da instituição responsável pela prestação do serviço.
CNPJ da instituição
Taxas ou tarifas de serviços de corretagem
Denominação
Especifica o tipo de ativo financeiro negociado.
Fato gerador
Descrição de forma clara e objetiva do serviço que justifica a cobrança de tarifa.
Valor
Distribuição de frequência relativa dos valores referentes às taxas ou tarifas cobradas, nos termos da Resolução BCB nº 32, de 2020.
Taxas ou tarifas de serviços de agente de custódia
Denominação
Especifica o tipo de ativo financeiro negociado.
Fato gerador
Indicação do fato ou serviço que dá origem à cobrança de tarifa.
Valor
Distribuição de frequência relativa dos valores referentes às taxas ou tarifas cobradas, nos termos da Resolução BCB nº 32, de 2020.
3.7 Seguros, previdência complementar aberta e capitalização
As instituições devem observar o disposto no Manual de Escopo de Dados e Serviços do Open Insurance, disponível na página do Open Insurance no endereço eletrônico da Superintendência de Seguros Privados (Susep) na internet.
4. Dados sobre o cadastro de clientes e de seus representantes
4.1 Pessoa natural
Dado
Campo
Esclarecimentos adicionais
Identificação
Nome completo
Número do CPF
Número completo do CPF da pessoa natural.
Número do documento de viagem
Número do documento de viagem, aplicável somente à pessoa natural residente no exterior desobrigada de inscrição no CPF.
Data de vigência do documento de viagem
Data de vigência do documento de viagem, conforme especificação RFC-3339.
País emissor do documento de viagem
País de emissão do documento de viagem, conforme o código "alpha3" do ISO-3166.
Endereço residencial
Complemento
Bairro
Município
Sigla da Unidade da Federação
CEP
País
DDI
DDD
Número de telefone
Ramal
E-mail(s)
Nome social
Tipo de filiação
Filiação
Nome civil completo das pessoas relativas à filiação.
Data de nascimento
Estado marital
1. solteiro, 2. casado, 3. viúvo, 4. separado judicialmente, 5. divorciado, 6. união estável, 7. outros.
Sexo
Tipo do(s) documento(s) de identificação
1. CNH, 2. RG, 3. NIF, 4. RNE, 5. outros, 6. sem outros documentos.
Número/código do(s) documento(s) de identificação
Data de validade do(s) documento(s) de identificação
Local de emissão
Nacionalidade brasileira
1. sim, 2. não.
Outras nacionalidades
De acordo com o código "alpha3" do ISO-3166.
Documento(s) estrangeiro(s) de identificação
Tipo do(s) documento(s) estrangeiro(s) de identificação
País do(s) documento(s) estrangeiro(s) de identificação
De acordo com o código "alpha3" do ISO-3166.
Data de validade do(s) documento(s) estrangeiro(s) de identificação
Qualificação
Frequência da renda informada
1. diária, 2. semanal, 3. quinzenal, 4. mensal, 5. bimestral, 6. trimestral, 7. semestral, 8. anual.
Moeda
BRL.
Valor da renda
Data de referência da renda
Conforme especificação RFC-3339.
Moeda
BRL.
Valor do patrimônio
Ano de referência do patrimônio
Ocupação
Código da ocupação
Tipo de código da ocupação
1. RFB, 2. CBO, 3. outros.
Relacionamento
Data de início de relacionamento da pessoa natural
Conforme especificação RFC-3339. Deve trazer o menor valor reportada ao Banco Central do Brasil por meio do DOC 3040 e do Cadastro de Clientes do Sistema Financeiro (CCS).
Tipos de produtos e serviços com contratos vigentes
1. conta de deposito à vista, 2. conta de pagamento pré-paga, 3. conta de poupança, 4. cartão de crédito, 5. operação de crédito,
6. seguro, 7. previdência, 8. investimento, 9. operações de câmbio, 10. conta salário, 11. credenciamento, 12. outros.
Natureza de conta
1. depósito à vista, 2. poupança, 3. pagamento pré-paga, 4. não se aplica.
Subtipo de conta
1. individual, 2. conjunta simples, 3. conjunta solidária, 4. não se aplica.
Número da(s) Conta(s)
Código(s) da(s) agência(s)
Natureza dos poderes vigentes de representante
1. representante legal, 2. procurador. 3. não se aplica.
CPF do representante
Nome civil completo do representante
Nome social do representante
Nome ou Razão social do empregador
Conforme registrado em comunicação da portabilidade de salário.
CPF/CNPJ do empregador
Conforme registrado em comunicação da portabilidade de salário.
CNPJ do Banco Detentor da Conta Salário
Conforme registrado em comunicação da portabilidade de salário.
ISPB do Banco Detentor da Conta Salário
Conforme registrado em comunicação da portabilidade de salário.
Data de Aprovação da Portabilidade
Conforme registrado em comunicação da portabilidade de salário.
Nome ou Razão social do empregador
Conforme registrado na abertura da conta salário.
CPF/CNPJ do empregador
Conforme registrado na abertura da conta salário.
CNPJ do Banco Detentor da Conta Salário
Conforme registrado na abertura da conta salário.
ISPB do Banco Detentor da Conta Salário
Conforme registrado na abertura da conta salário.
Data de Abertura da Conta Salário
Conforme registrado na abertura da conta salário.
4.2 Pessoa jurídica
Dado
Campo
Esclarecimentos adicionais
Identificação
Razão social
Nome fantasia
Data de constituição
Conforme especificação RFC-3339.
Número do CNPJ
Número completo do CNPJ da pessoa jurídica.
Número de registro no país de origem
Aplicável somente as pessoas jurídicas com domicílio ou sede no exterior desobrigadas de inscrição no CNPJ.
País de emissão do documento de registro
De acordo com o código "alpha3" do ISO-3166.
Data de vigência do documento de registro
Conforme especificação RFC-3339.
Endereço comercial
Complemento
Bairro
Município
Código IBGE do município
Sigla da Unidade da Federação
CEP
País
Código do país
De acordo com o código "alpha3" do ISO-3166.
Latitude
Entre -90 e 90. Formato numérico, 2 casas antes da vírgula, 11 posições.
Longitude
Entre -180 e 180. Formato numérico, 3 casas antes da vírgula, 11 posições.
DDI
DDD
Número de telefone
Ramal
E-mail(s)
Tipo de vínculo com a pessoa jurídica
1. sócio, 2. administrador.
Nome completo do sócio ou administrador
Nome social do sócio ou administrador
Data de início do vínculo
Conforme especificação RFC-3339.
Percentual da participação societária
Percentual de participação societária (informar com 2 casas decimais). Sócio só deve ser informado se sua participação societária for igual ou superior a 25%.
Tipo de documento de identificação do sócio ou administrador
Número/código do documento do sócio ou administrador
País emissor do documento do sócio ou administrador
De acordo com o código "alpha3" do ISO-3166.
Data de vigência do documento do sócio ou administrador
Data vigência do documento, conforme especificação RFC-3339.
Qualificação
Ramo de atuação principal
Código do ramo da atividade da empresa consultada, segundo padrão CNAE (Classificação Nacional de Atividades Econômicas).
Ramo de atuação secundária
Códigos relativos às demais atividades econômicas da empresa, segundo padrão CNAE (Classificação Nacional de Atividades Econômicas). Se disponível.
Frequência do faturamento informado
1. diária, 2. semanal, 3. quinzenal, 4. mensal, 5. bimestral, 6. trimestral, 7. semestral, 8. anual.
Moeda
BRL.
Valor de faturamento
Ano de referência do faturamento
Moeda
BRL.
Valor do patrimônio da empresa
Data do patrimônio informado
Conforme especificação RFC-3339.
Relacionamento
Data de início de relacionamento da pessoa jurídica
Conforme especificação RFC-3339. Deve trazer o menor valor reportada ao Banco Central do Brasil por meio do DOC 3040 e do Cadastro de Clientes do Sistema Financeiro (CCS).
Tipos de produtos e serviços com contratos vigentes
1. conta de deposito à vista, 2. conta de pagamento pré-paga, 3. conta de poupança, 4. cartão de crédito, 5. operação de crédito,
6. seguro, 7. previdência, 8. investimento, 9. operações de câmbio, 10. conta salário, 11. credenciamento, 12. outros.
Natureza de conta
1. depósito à vista, 2. poupança, 3. pagamento pré-paga, 4. não se aplica.
Número da(s) conta(s)
Código(s) da(s) agência(s)
Natureza dos poderes vigentes de representante
1. representante legal, 2. procurador, 3. não possui.
Nome ou razão social do representante
Nome social do representante
CPF ou CNPJ do representante
5. Dados transacionais
5.1 Contas de depósitos à vista ou de poupança e de pagamento pré-pagas
Dado
Campo
Esclarecimentos adicionais
Identificação
Natureza da conta
1. conta de depósitos à vista, 2. conta de depósitos de poupança, 3. conta de pagamento pré-paga.
Subtipo de conta
1. individual, 2. conjunta simples, 3. conjunta solidária.
Número da conta
Código da agência
Saldo Disponível
Moeda
BRL.
Saldo disponível
Moeda
BRL.
Saldo bloqueado
Moeda
BRL.
Saldo disponível com aplicação automática
Data de atualização do saldo
Data e hora da última captura do saldo para compartilhamento no Open Finance.
Transações da conta
Indicador da transação
1. Transação efetivada, 2. Lançamento futuro, 3. Transação processando.
Tipo de lançamento
1. crédito, 2. débito.
Tipo de transação
1. TED, 2. Pix, 3. transferência entre contas na mesma instituição, 4. pagamento de boleto, 5. pagamento de convênio ou de outros documentos de arrecadação, 6. pacote de serviços, 7. tarifa, 8. folha de pagamento,
9. depósito, 10. saque, 11. pagamento de cartão, 12. juros, multas e demais encargos financeiros, 13. rendimento de aplicação financeira, 14. portabilidade de salário, 15. resgate de aplicação financeira,
16. operações de crédito, 17. outros.
Identificação da transação
Literal usada pela instituição detentora de contas para identificar a transação, conforme visualização apresentada ao cliente nos canais eletrônicos da instituição (extrato).
Como regra geral deve ser compartilhada a informação conforme consta no histórico de transações apresentado na tela do aplicativo ou do navegador.
O Banco Central pode determinar o formato de compartilhamento a ser adotado por uma instituição participante específica.
Identificador único da transação
Código ou identificador único prestado pela instituição que mantém a conta para representar a transação individual.
Moeda
BRL.
Valor
Data da transação
Data e hora da transação disponível para os clientes nos canais digitais da instituição. Obrigatório preencher com dados reais com precisão de pelo menos data, hora, minuto e segundo.
Tipo de pagador/recebedor envolvido na transação
Identificação do tipo de pessoa envolvida na transação:
Pessoa Natural - Informar "PESSOA_NATURAL" no campo "PartiePersonType"; ou
Pessoa Jurídica - Informar "PESSOA_JURIDICA" no campo "PartiePersonType".
Identificação do pagador/recebedor de transação
Nome ou razão social e CPF ou CNPJ do pagador/recebedor de transação.
Identificação da instituição do pagador/recebedor
Código identificador da instituição do pagador/recebedor atribuído pelo Banco Central do Brasil às instituições participantes do STR (Sistema de Transferência de reservas).
Limites contratados
Moeda
BRL.
Valor do limite de cheque especial
Valor do limite de cheque especial contratado pelo cliente.
Moeda
BRL.
Valor utilizado do limite de cheque especial
Valor utilizado total do limite do cheque especial e o adiantamento a depositante.
Moeda
BRL.
Valor de operação de adiantamento a depositantes contratada
Valor de operação contratada em caráter emergencial para cobertura de saldo devedor em conta de depósitos à vista e de excesso sobre o limite pactuado de cheque especial.
5.2 Conta de pagamento pós-paga
Dado
Campo
Esclarecimentos adicionais
Tipos de conta
Denominação
Denominação da conta de pagamento pós-paga.
Produto
Instituidor do arranjo de pagamento pós-pago
Identificador do instrumento de pagamento pós-pago (cartão de crédito)
Funcionalidade de cartão múltiplo
1. sim, 2. não.
Limite de crédito total associado ao cartão de crédito
Indicador de consolidação
1. consolidado, 2. individual.
Moeda
BRL.
Valor total do limite de crédito
Justificativa de limite zerado
Justificativa para caso em que o limite é igual a zero.
Moeda
BRL.
Valor utilizado do limite de crédito
Moeda
BRL.
Valor disponível não utilizado do limite de crédito
Limites por modalidade de operação associada ao cartão de crédito
Modalidade de operação
1. crédito à vista, 2. crédito parcelado, 3. saque a crédito no Brasil, 4. saque a crédito no exterior, 5. empréstimo cartão consignado, 6. outros.
Indicador de consolidação
1. consolidado, 2. individual.
Moeda
BRL.
Valor total por modalidade
Moeda
BRL.
Valor utilizado
Moeda
BRL.
Valor disponível não utilizado dos limites por modalidade
Transações realizadas
Tipo de transação
1. pagamento, 2. tarifa, 3. operações de crédito contratadas no cartão, 4. estorno, 5. cashback, 6. outros.
Identificação da transação
Literal usada na instituição financeira para identificar a transação. A informação apresentada precisa ser a mesma utilizada nos canais eletrônicos da instituição (extrato).
Identificador único da transação
Código ou identificador único prestado pela instituição que mantém a conta para representar a transação individual.
Identificação da fatura
Informação que identifica a fatura onde consta a transação informada, não devendo ser informada para faturas abertas.
Indicador da operação
1. crédito, 2. débito.
Tipo de pagamento
1. à vista, 2. a prazo.
Tipo de tarifa
Observar a padronização estabelecida na regulamentação vigente.
Tipo de operação de crédito contratada no cartão
1. crédito rotativo, 2. parcelamento de fatura, 3. empréstimo. 4. outros.
Identificador da parcela
Quantidade de parcelas
Moeda
BRL.
Valor
Data da transação
Data e hora da transação disponível para os clientes nos canais digitais da instituição. Obrigatório preencher com dados reais com precisão de data, hora e minuto.
Tipo de pagador/recebedor envolvido na transação
Identificação do tipo de pessoa envolvida na transação:
Pessoa Natural - Informar "PESSOA_NATURAL" no campo "PartiePersonType"; ou
Pessoa Jurídica - Informar "PESSOA_JURIDICA" no campo "PartiePersonType".
Identificação do pagador/recebedor
Nome ou razão social e CPF ou CNPJ do pagador/recebedor de transação.
Pagamento da fatura
Identificação da fatura
Informação que identifica a fatura.
Pagamento da fatura
Data do vencimento
Conforme especificação RFC-3339.
Data do pagamento efetivo
Moeda
BRL.
Valor total da fatura
Moeda
BRL.
Valor de pagamento mínimo
Moeda
BRL.
Valor de pagamento da fatura
Parcelamento
1. sim, 2. não.
Forma de pagamento
Tipo de encargo
Moeda
BRL.
Valor do encargo
5.3 Operações de Crédito
Dado
Campo
Esclarecimentos adicionais
Identificação do contrato
Denominação
Denominação da operação de crédito definida pela instituição contratante.
Modalidade de crédito contratada
1. adiantamento a depositantes, 2. empréstimos, 3. direitos creditórios descontados, 4. financiamentos, 5. financiamentos Rurais, 6. financiamentos imobiliários. Conforme Documento 3040.
Subtipo da modalidade de crédito contratada
Número do contrato dado pela instituição contratante
Número padronizado do contrato
Identificação Padronizada da Operação de Crédito (IPOC).
Data de contratação da operação
Conforme especificação RFC-3339.
Data da liberação de recursos
Conforme especificação RFC-3339.
Data de liquidação da operação
Conforme especificação RFC-3339.
Moeda
BRL.
Valor contratado
Data de vencimento final da operação
Conforme especificação RFC-3339.
Periodicidade
1. sem periodicidade regular, 2. semanal, 3. quinzenal, 4. mensal, 5. bimestral, 6. trimestral, 7. semestral, 8. anual, 9. outros.
Data de vencimento da primeira prestação
Conforme especificação RFC-3339.
Custo Efetivo Total (CET)
Expresso na forma de taxa percentual anual, com observância da regulamentação vigente.
Seguro contratado
Identificação se existe seguro contratado para a operação de crédito.
Sistema de amortização
CNPJ do ente consignante
Taxa de juros remuneratórios
Tipo de taxa
1. nominal, 2. efetiva.
Tipo de juros
1. simples, 2. composto.
Periodicidade da taxa
1. a.m., 2. a.a.
Base de cálculo
1. 21/252, 2. 30/360, 3. 30/365.
Referencial ou indexador
Tipos de taxas referenciais ou indexadores e percentuais adotados, conforme Documento 3040.
Taxa pré-fixada contratada
Tarifas
Denominação da tarifa
Conforme a regulamentação vigente, no caso de tarifas cobradas de pessoas naturais.
Sigla identificadora da tarifa
Conforme a regulamentação vigente, no caso de tarifas cobradas de pessoas naturais.
Moeda
BRL.
Valor
Data de pagamento
Conforme especificação RFC-3339.
Encargos
Tipo de encargo
Observado os tipos de encargos cuja cobrança é admitida pela legislação e pela regulamentação vigente.
Moeda
BRL.
Valor
Data de pagamento
Conforme especificação RFC-3339.
Garantias
Tipo da garantia
De acordo com o Anexo 12 do Documento 3040.
Subtipo da garantia
De acordo com o Anexo 12 do Documento 3040.
Moeda
BRL.
Valor original
Pagamentos
Moeda
BRL.
Saldo devedor
Valor do saldo devedor remanescente.
Data de pagamento das prestações
Relação das datas dos pagamentos realizados no período. Conforme especificação RFC-3339.
Moeda
BRL.
Valor do pagamento
Relação dos valores dos pagamentos realizados no período.
Identificador único do pagamento
Código ou identificador único prestado pela instituição para representar o pagamento individual.
Prazo do contrato
Prazo total do contrato
Em meses.
Prazo remanescente do contrato
Em meses.
Quantidade de prestações pagas
Considerar somente as parcelas quitadas no valor integral.
Quantidade de prestações a vencer
Quantidade de prestações vencidas
Data de vencimento das prestações não regulares
Relação das datas de vencimento das prestações não regulares a pagar.
Moeda
BRL
Valor da prestação não regular a pagar
Relação dos valores dos pagamentos a realizar no período.
5.4 Investimentos
Os dados de investimentos aqui demandados contemplam aqueles referentes aos mercados primário e secundário, à exceção de títulos públicos federais transacionados no mercado secundário (custódia SELIC).
5.4.1 Certificado de Depósito Bancário, Recibo de Depósito Bancário, Letra de Crédito Imobiliário e Letra de Crédito do Agronegócio
Dado
Campo
Esclarecimentos adicionais
Identificação da instituição
CNPJ da instituição responsável pela distribuição do produto.
Identificação da instituição emissora
CNPJ da instituição emissora do produto.
Identificação do instrumento financeiro
Código ISIN.
Denominação do produto
Conforme regulamentação vigente.
Identificador único do investimento
Identifica de forma única o relacionamento do cliente com o produto.
Código na clearing
Código de registro do ativo na clearing.
Data de emissão do título
​
Data de vencimento
Data de vencimento do ativo financeiro.
Preço
Valor monetário do preço unitário.
Data da compra pelo cliente
Data de aquisição pelo cliente.
Data de fim da carência
Data até a qual o cliente não poderá resgatar antecipadamente seu investimento.
Remuneração
Tipo de remuneração
1. pré-fixado, 2. pós-fixado ou 3. híbrida.
Taxa de remuneração na emissão
Taxa de remuneração na emissão (pré-fixado).
Percentual do indexador na emissão
Percentual do indexador na emissão (pós fixado).
Tipo de taxa
Tipo de taxa de remuneração.
Periodicidade da taxa
Periodicidade da taxa de remuneração.
Base de cálculo
Periodicidade da base de cálculo.
Índice de referência
Índice de referência para a correção da rentabilidade e/ou rendimentos do ativo.
Informações adicionais sobre o índice de referência
Valor do preço unitário
Valor do preço unitário na emissão.
Moeda
BRL.
Saldos de Investimentos
Data de referência
Data e hora da última posição consolidada disponível a que se referem os dados transacionais do cliente disponíveis nos canais eletrônicos.
Quantidade de títulos detidos
Quantidade de títulos detidos na data da posição do cliente.
Valor atualizado do preço unitário
Valor bruto unitário atualizado na data de referência.
Valor bruto
Valor do investimento que se refere a quantidade x PU atualizado na data de referência.
Valor líquido
Valor do investimento atualizado na data de referência, posterior a dedução de impostos (IOF e IR).
IR provisionado
Valor do imposto de renda provisionado considerando a alíquota vigente na data de referência.
IOF provisionado
Valor do imposto (IOF) provisionado considerando a alíquota vigente na data de referência.
Saldo bloqueado
Valor não disponível para movimentação naquele momento por qualquer motivo (bloqueio judicial, bloqueio em garantia, entre outros). Prazo de carência não é considerado como bloqueio.
Valor unitário na data da compra
Valor unitário negociado com o cliente na data de aquisição.
Moeda
BRL.
Transações
Tipo de movimentação
Tipo de movimentação na visão de investimento: entrada ou saída
Tipo de transação
Aplicação, resgate, cancelamento, vencimento etc.
Informação adicional sobre o tipo de movimentação
Data da movimentação
PU bruto
Preço unitário bruto na data da transação.
Quantidade transacionada
Quantidade de títulos envolvidos na transação.
Valor bruto da transação
Valor bruto da transação (Preço unitário da movimentação x Quantidade).
Imposto de renda
Valor do imposto de renda recolhido na transação.
Imposto IOF
Valor do IOF recolhido na transação.
Valor líquido da transação
Taxa de remuneração da transação
Percentual do indexador
Percentual máximo do indexador acordado com o cliente na contratação.
Identificador único
Código ou identificador único prestado pela instituição que mantém a representação individual do movimento.
Moeda
BRL.
5.4.2 Debêntures, Certificados de Recebíveis Imobiliários (CRI) e Certificados de Recebíveis do Agronegócio (CRA)
Dado
Campo
Esclarecimentos adicionais
Identificação
Identificação da instituição
CNPJ da instituição.
Identificação da instituição emissora
CNPJ da instituição emissora.
Identificação do instrumento financeiro
Código ISIN.
Tipo de investimento
Especificação do ativo (Debêntures, CRI ou CRA).
CNPJ do devedor
Nome do devedor
Indicador de produto isento
Indicar se o produto é incentivado mediante isenção de imposto sobre ganhos.
Informações de remuneração
Indicar se há pagamento de cupom, periodicidade e informações adicionais.
Indexador
Índice utilizado como referência para a correção da rentabilidade ou rendimentos do ativo.
Informações adicionais do indexador
Identificador único do investimento
Identifica de forma única o relacionamento do cliente com o produto.
CNPJ do devedor
Quando se tratar de CRI e CRA.
Nome do devedor
Quando se tratar de CRI e CRA.
Código na clearing
Código de registro do ativo na clearing.
Data de emissão do título
Data de vencimento do título
Preço
Valor monetário do preço unitário.
Data da compra pelo cliente
Data de aquisição pelo cliente.
Data de fim da carência
Data até a qual o cliente não poderá resgatar antecipadamente seu investimento.
Remuneração
Tipo de remuneração
Taxa de remuneração na emissão
Taxa de remuneração na emissão (pré-fixado).
Percentual do indexador na emissão
Percentual do indexador na emissão (pós fixado).
Tipo de taxa
Tipo de taxa de remuneração.
Periodicidade da taxa
Periodicidade da taxa de remuneração.
Base de cálculo
Periodicidade da base de cálculo.
Índice de referência
Índice de referência para a correção da rentabilidade e/ou rendimentos do ativo.
Informações adicionais sobre o índice de referência
Valor do preço unitário
Valor do preço unitário na emissão.
Moeda
BRL.
Data de referência
Data e hora da última posição consolidada disponível a que se referem os dados transacionais do cliente disponíveis nos canais eletrônicos.
Quantidade de títulos detidos
Quantidade de títulos detidos na data da posição do cliente.
Valor atualizado do preço unitário
Valor bruto unitário atualizado na data de referência.
Valor bruto
Valor do investimento que se refere a quantidade x PU atualizado na data de referência.
Valor líquido
Valor do investimento atualizado na data de referência, posterior a dedução de impostos (IOF e IR).
Imposto de renda provisionado
Valor do imposto de renda provisionado considerando a alíquota vigente na data de referência.
IOF provisionado
Valor do imposto (IOF) provisionado considerando a alíquota vigente na data de referência.
Saldo bloqueado
Valor não disponível para movimentação naquele momento por qualquer motivo (bloqueio judicial, bloqueio em garantia, entre outros). Prazo de carência não é considerado como bloqueio.
Valor unitário na data da compra
Valor unitário negociado com o cliente na data de aquisição.
Moeda
BRL.
Transações
Tipo de movimentação
Tipo de movimentação na visão de investimento: entrada ou saída
Tipo de transação
Aplicação, resgate, cancelamento, vencimento etc.
Informação adicional sobre o tipo de movimentação
Data da movimentação
PU bruto
Preço unitário bruto na data da transação.
Quantidade transacionada
Quantidade de títulos envolvidos na transação.
Valor bruto da transação
Valor bruto da transação (Preço unitário da movimentação x Quantidade).
IR recolhido
Valor do imposto de renda recolhido na transação.
IOF recolhido
Valor do IOF recolhido na transação.
Valor líquido da transação
Taxa de remuneração da transação
Percentual do indexador
Percentual máximo do indexador acordado com o cliente na contratação.
Identificador único
Código ou identificador único prestado pela instituição que mantém a representação individual do movimento.
Moeda
BRL.
5.4.3 Renda Variável
Dado
Campo
Esclarecimentos adicionais
Identificação
Identificação da instituição
CNPJ da instituição.
Identificação da instituição emissora
CNPJ da instituição emissora.
Identificador único do investimento
Identifica de forma única o relacionamento do cliente com o produto, mantendo as regras de imutabilidade dentro da instituição transmissora.
Identificação do instrumento financeiro
Código ISIN.
Ticker
Código de negociação para identificação de ativos negociados em bolsa.
Posição
Data de referência
Posição fechada para o ativo na data do dia anterior.
Fator de preço
Fator que indica o número de ações utilizadas para a formação do preço.
Saldo bruto
Valor do investimento anterior à dedução de impostos, taxas e tarifas (se houver), atualizado na data de referência.
Saldo bloqueado
Valor não disponível para movimentação naquele momento por qualquer motivo (bloqueio judicial, bloqueio em garantia, entre outros).
Quantidade
Quantidade total do ativo na data de referência.
Preço da data de referência
Preço de fechamento da data de referência.
Moeda
BRL
Movimentações
Tipo de movimentação
Tipo de movimentação na visão de investimento: entrada ou saída
Motivo da movimentação
O campo deve classificar a movimentação em um dos tipos descritos: 1. compra, 2. venda, 3. dividendos, 4. JCP, 5. aluguéis, 6. transferência de custódia, 7. transferência de titularidade e 8. outros.
Informação adicional sobre o motivo da movimentação
Data da movimentação
Fator de preço
Fator que indica o número de ações utilizadas para a formação do preço.
PU da movimentação
Preço unitário da movimentação: valor da unidade do produto na movimentação do investimento.
Quantidade
Quantidade de ativos movimentados.
Valor da movimentação
Valor da transação realizada pelo cliente.
Identificador único da movimentação
Código ou identificador único prestado pela instituição que mantém a representação individual do movimento.
Identificador da nota de negociação
Identificador da nota de negociação.
Moeda
BRL.
Detalhes da nota de negociação
Número da nota de negociação
Identificador da nota de negociação.
Valor bruto da nota de negociação
Valor da nota de negociação, que é o somatório das operações realizadas.
Valor monetário da taxa de corretagem
Pode ser cobrada como um valor fixo por operação, ou um como um percentual sobre o valor negociado, ou ainda de forma mista, conforme guia CVM do investidor.
Valor monetário da taxa de liquidação
Valor cobrado para liquidação na custódia.
Valor monetário da taxa de registro
Valor cobrado para registro na custódia.
Valor monetário da taxa Aviso de Negociações de Ativos (A.N.A .)
Valor cobrado pela bolsa pelo aviso de negociação de ativo.
Emolumentos
Valor cobrado pela bolsa para remunerar os serviços de registro prestados.
Valor monetário da taxa de custódia
Taxa cobrada pela IF para custódia.
Impostos
Impostos cobrados na operação, exceto imposto de renda.
Imposto de renda recolhido na fonte
Imposto de renda retido na fonte.
Valor líquido da nota de negociação
Valor bruto da negociação após despesas com taxa de corretagem, taxa de liquidação, taxa de registro, taxa A.N.A., emolumentos, taxa de custódia, impostos e IRRF.
Moeda
BRL.
5.4.4 Tesouro Direto
Dado
Campo
Esclarecimentos adicionais
Identificação
Identificação da instituição
CNPJ da instituição responsável pelo cadastro.
Identificação do instrumento financeiro
Código ISIN.
Identificador único do investimento
Identifica de forma única o relacionamento do cliente com o produto, mantendo as regras de imutabilidade dentro da instituição transmissora.
Nome do produto
Descrição do ativo em questão.
Remuneração
Indexador
Índice utilizado como referência para a correção da rentabilidade e/ou rendimentos do ativo (CDI, DI , TR, IPCA, IGP_M, IGP_DI, INPC, BCP, TLC, SELIC, PRE_FIXADO e OUTROS).
Informações adicionais do indexador
Taxa de remuneração da aquisição (pré-fixada)
Valor da taxa da aquisição do contrato.
Percentual do indexador da aquisição (pós-fixado)
Percentual do indexador da aquisição do contrato.
Periodicidade da taxa de remuneração
Periodicidade da taxa de remuneração (mensal, anual, diário e semestral).
Base da taxa de remuneração
Base de cálculo (dias úteis ou dias corridos).
Data de vencimento
Data de vencimento do título.
Data de aquisição
Data de aquisição do cliente.
Pagamento de cupom
Indicativo se há pagamento de cupom (sim ou não).
Periodicidade de pagamento do cupom
Em caso de haver pagamento de cupom, descrever a periodicidade (mensal, trimestral, semestral, anual, irregular e outros).
Informações adicionais da periodicidade de pagamento de cupom
Posição
Data de referência da posição
Data da última posição consolidada disponível a que se referem os dados transacionais do cliente disponíveis nos canais eletrônicos.
PU atualizado
Valor bruto unitário atualizado (a mercado) na data de referência.
Saldo bruto
Valor do investimento anterior à dedução de impostos, taxas e tarifas (se houver), atualizado (a mercado) na data de referência.
Saldo líquido
Valor do investimento posterior a dedução de impostos, taxas e tarifas (se houver), atualizado (a mercado) na data de referência.
Imposto de renda provisionado
Valor do imposto provisionado considerando a alíquota vigente na data de referência.
IOF provisionado
IOF provisionado.
Saldo bloqueado
Valor não disponível para movimentação naquele momento por qualquer motivo (bloqueio judicial, bloqueio em garantia, entre outros).
PU de aquisição
Valor unitário negociado com o cliente na data de aquisição.
Quantidade
Quantidade de títulos detidos na data da posição do cliente.
Moeda
BRL.
Movimentações
Tipo de movimentação
Tipo de movimentação na visão de investimento: entrada ou saída
Motivo da movimentação
1. compra, 2. venda, 3. cancelamento, 4. vencimento, 5. pagamento de juros, 6. amortização, 7. transferência de titularidade, 8. transferência de custódia e 9. outros.
Data da movimentação
PU unitário da movimentação
Preço unitário bruto negociado na transação.
Quantidade
Quantidade de títulos movimentados.
Valor bruto da movimentação
Valor da transação realizada pelo cliente.
Imposto de renda recolhido na fonte
Valor do imposto de renda retido na fonte.
IOF recolhido na fonte
Valor do IOF recolhido na fonte.
Valor líquido da movimentação
Valor líquido da transação.
Taxa de remuneração
Taxa de remuneração da movimentação.
Identificador único da movimentação
Código ou identificador único prestado pela instituição para individualizar o movimento.
5.4.5 Cotas de fundo de investimento relativas a fundos de investimento classificados como cambial, multimercado, de renda fixa e de ações
Dado
Campo
Esclarecimentos adicionais
Identificação
Identificação da instituição
CNPJ da instituição responsável pelo cadastro.
Classificação ANBIMA
Classe
Subclasse
Identificador único do investimento
Identifica de forma única o relacionamento do cliente com o fundo, mantendo as regras de imutabilidade dentro da instituição transmissora.
Nome do fundo de investimento
Nome oficial do fundo de investimento conforme exibido para os clientes nos canais eletrônicos.
CNPJ do fundo de investimento
CNPJ do fundo de investimento.
Identificação do instrumento financeiro
Código ISIN.
Classificação ANBIMA
Classe
Subclasse
Posição
Data de referência
Data da última posição consolidada disponível a que se referem os dados transacionais do cliente disponíveis nos canais eletrônicos.
Saldo bruto
Valor do investimento que se refere a quantidade da cota x valor da cota, atualizado na data de referência.
Saldo líquido
Valor do investimento atualizado na data de referência, após a dedução de impostos (IOF e IR) e taxa de saída.
Imposto de renda provisionado
Valor do imposto provisionado considerando a alíquota vigente na data de referência.
IOF provisionado
IOF provisionado.
Saldo bloqueado
Valor não disponível para movimentação naquele momento por qualquer motivo (bloqueio judicial, bloqueio em garantia, entre outros).
Quantidade de cotas
Quantidade de títulos detidos na data da posição do cliente.
Valor bruto da cota
Valor bruto da cota atualizado na data de referência.
Moeda
BRL.
Movimentações
Identificador da movimentação
Código ou identificador único prestado pela instituição que mantém a representação individual do movimento na posição do fundo.
Tipo de movimentação
Tipo de movimentação na visão de investimento: entrada ou saída
Motivo da movimentação
Classificar a transação de movimentação de investimento em um dos tipos descritos (amortização, transferência de cotas, aplicação, resgate ou come-cotas).
Informação adicional do motivo da movimentação
Data da conversão da movimentação
Data da conversão da transação de movimentação do fundo de investimento.
Valor da cota da movimentação
Valor da cota utilizada na conversão para a realização da
movimentação do cliente no fundo, conforme a regra prevista em regulamento.
Quantidade de cotas movimentadas
Número de cotas convertidas na data da movimentação.
Valor da movimentação
Valor solicitado pelo cliente.
Valor bruto da movimentação
Valor da movimentação que se refere a quantidade da cota x valor da cota da movimentação.
Imposto de renda retido na fonte
Valor do imposto de renda retido na fonte considerando a alíquota vigente na data da movimentação.
IOF retido na fonte
Valor do IOF retido na fonte considerando a alíquota vigente na data da movimentação.
Valor da taxa de saída
Valor da taxa de saída considerado na movimentação.
Valor líquido da movimentação
Valor após a dedução de impostos e taxa de saída.
Moeda
BRL.
5.5 Câmbio
Dado
Campo
Esclarecimentos adicionais
Identificação
Marca
Nome da marca reportada pelo participante do Open Finance.
Identificação da instituição
CNPJ da instituição responsável pelo cadastro.
Identificador único do investimento
Identifica de forma única o relacionamento do cliente com o produto, mantendo as regras de imutabilidade dentro da instituição transmissora.
Identificação do Produto
Identificação da instituição autorizada
CNPJ da instituição autorizada a operar no mercado de câmbio.
Nome da instituição autorizada
Nome da instituição autorizada a operar no mercado de câmbio.
Identificação da instituição intermediadora
CNPJ da instituição intermediadora autorizada a operar no mercado de câmbio.
Nome da instituição intermediadora
Nome da instituição intermediadora autorizada a operar no mercado de câmbio
Número da operação
Número do registro da operação no Banco Central do Brasil.
Operação
Tipo de operação
Tipo de operação (compra ou venda).
Data da operação
Data do fechamento do contrato de câmbio.
Data de liquidação
Data em que a operação (compra ou venda) está prevista para ser liquidada.
Imposto sobre a operação
Imposto sobre a operação.
Valor da operação
Valor negociado na operação.
Valor da operação em moeda estrangeira
Valor a liquidar
Valor do saldo da operação a liquidar em moeda estrangeira.
Valor do VET
Custo da operação de câmbio em reais por moeda estrangeira, englobando a taxa de câmbio, as tarifas e tributos incidentes.
Percentual adiantado
Percentual do valor em moeda nacional concedido ao cliente antecipadamente.
Forma de entrega
Forma de entrega da moeda estrangeira.
Código da operação
Código da natureza fato do fechamento da operação.
Código de relação pagador/recebedor
Código de Relação de vínculo entre o Cliente e o Pagador/Recebedor no Exterior.
Nome da contraparte
Nome do pagador ou recebedor no exterior.
País da contraparte
País do pagador ou recebedor.
Moeda
Moeda em que o valor do campo a que se refere é denominado.
Eventos
Número de registro do evento
Informações da movimentação do fundo de investimento.
Tipo de evento
1. contratação no mercado primário, 2. alteração de operação cambial no mercado primário, 3. cancelamento de operação cambial no mercado primário, 4. liquidação de operação cambial no mercado primário,
5. baixa de valor a liquidar de operação cambial no mercado primário, 6. restabelecimento de baixa de valor a liquidar de operação cambial no mercado primário.
Data do evento
Data de evento relacionado com a operação.
Data de liquidação
Data em que a operação (compra ou venda), após evento, está prevista para ser liquidada.
Imposto sobre a operação
Imposto sobre a operação.
Valor da operação
Valor negociado na operação.
Valor da operação em moeda estrangeira
Valor a liquidar
Valor do saldo da operação a liquidar em moeda estrangeira.
Valor do VET
Valor da operação de câmbio em reais por moeda estrangeira, englobando a taxa de câmbio, as tarifas e tributos incidentes.
Percentual adiantado
Percentual do valor em moeda nacional concedido ao cliente antecipadamente.
Forma de entrega
Forma de entrega da moeda estrangeira.
Código da operação
Código da natureza fato do fechamento da operação.
Código de relação pagador/recebedor
Código de Relação de vínculo entre o cliente e o pagador/recebedor no exterior.
Nome da contraparte
Nome do pagador ou recebedor no exterior.
País da contraparte
País do pagador ou recebedor.
Moeda
Moeda em que o valor do campo a que se refere é denominado.
6. Dados e escopo referentes ao serviço de iniciação de transação de pagamento
Com relação aos dados necessários para o compartilhamento do serviço de iniciação de transação de pagamento, as tabelas da subseção 6.1 deste manual apresentam os dados mínimos que devem estar abrangidos para a iniciação da transação de pagamento. Além desses dados, devem ser observados, de forma geral, os dados dispostos nos regulamentos que disciplinem o funcionamento do arranjo de pagamento referente à respectiva transação de pagamento e demais dados estabelecidos nas especificações disponíveis no Portal do Open Finance no Brasil.
6.1 Dados mínimos para o serviço de iniciação de transação de pagamento
6.1.1 Dados mínimos para consentimento e solicitação do compartilhamento do serviço de iniciação de transação de pagamento, no caso de pagamentos únicos
Pagamentos únicos são pagamentos que ocorrerão apenas uma vez, sejam imediatos ou agendados para uma data futura.
Campo
Esclarecimentos adicionais
Dados mínimos
Informações do cliente pagador
Identificação do cliente pagador.
Conta do pagador a ser debitada
Informações sobre a conta a ser debitada, caso informado pelo cliente à instituição iniciadora de transação de pagamento, incluindo ISPB, tipo e número da conta e agência.
Informações do recebedor
Identificação do recebedor/beneficiário, incluindo nome relacionado à identificação e número do CPF ou CNPJ.
Forma de pagamento
Conforme serviços de pagamento de que trata o art. 6º da Circular nº 4.015, de 2020.
Valor
Valor a ser pago.
Moeda
BRL.
Data do pagamento
Data do pagamento.
6.1.2 Dados mínimos para consentimento e solicitação do compartilhamento do serviço de iniciação de transação de pagamento, no caso de pagamentos sucessivos
A Resolução Conjunta nº 1, de 2020, estabelece a possibilidade de transações de pagamentos sucessivas. Essas podem ser consideradas:
I - Agendamentos Recorrentes: representam mais de um pagamento agendado utilizando o mesmo consentimento;
II - Transferências Inteligentes: permitem a transferência automática de fundos entre contas pertencentes a um mesmo cliente, geralmente em diferentes instituições financeiras, utilizando o mesmo consentimento; ou
III - Pix Automático: definido nos termos da Resolução BCB nº 1, de 12 de agosto de 2020.
Campo
Esclarecimentos adicionais
Dados mínimos
Informações do cliente pagador
Identificação do cliente pagador.
Conta do pagador a ser debitada
Informações sobre a conta a ser debitada, caso informado pelo cliente à instituição iniciadora de transação de pagamento, incluindo ISPB, tipo e número da conta e agência, se aplicável.
Informações do recebedor
Identificação do recebedor/beneficiário, incluindo nome relacionado à identificação e número do CPF ou CNPJ.
Forma de pagamento
Conforme serviços de pagamento de que trata o art. 6º da Circular nº 4.015, de 2020.
Valor
Facultativo nos casos de transações de pagamento sucessivas cujo valor pactuado seja variável.
Moeda
BRL.
Data do pagamento
Com a inclusão da periodicidade, prazo, número de recorrências ou data inicial de pagamento.
Limite
Quando aplicável.
6.1.3 Dados mínimos para consentimento e solicitação do compartilhamento do serviço de iniciação de transação de pagamento sem redirecionamento
A resolução BCB nº 406, de 2 de agosto de 2024, define que o compartilhamento do serviço de iniciação de transação de pagamento sem redirecionamento compreende as etapas de vinculação de conta e transação de pagamento.
Para a etapa de vinculação de conta, os dados devem abranger, no mínimo, os campos listados na tabela a seguir:
Campo
Esclarecimentos adicionais
Dados mínimos
Informações do cliente pagador
Identificação do cliente pagador.
Identificação da instituição iniciadora
Identificação da instituição iniciadora.
Conta do pagador a ser debitada
Informações sobre a conta a ser debitada, caso informado pelo cliente à instituição iniciadora de transação de pagamento, incluindo ISPB, tipo e número da conta e agência.
Forma de pagamento
Conforme serviços de pagamento de que trata o art. 6º da Circular nº 4.015, de 2020.
Valor máximo por transação
Quando aplicável.
Valor máximo diário
Quando aplicável.
Prazo de validade do consentimento
Prazo de cinco anos que o cliente deve poder aumentar ou reduzir.
Para a etapa de transação de pagamento, os dados mínimos são os mesmos correspondentes a consentimento e solicitação do compartilhamento do serviço de iniciação de transação de pagamento, no caso de pagamentos únicos ou de pagamentos sucessivos, conforme subseções 6.1.1 e 6.1.2, respectivamente.
6.2 Serviço de iniciação de transação de pagamento de Pix
O Pix é um arranjo de pagamentos instantâneos instituído pelo Banco Central do Brasil, disciplinado nos termos da Resolução BCB nº 1, de 12 de agosto de 2020, e demais regulamentos correspondentes.
Para o compartilhamento do serviço de iniciação de transação de pagamento de Pix, os requisitos técnicos, o escopo, as formas de iniciação e demais procedimentos operacionais necessários devem ser implementados pelas instituições participantes conforme os limites estabelecidos pela regulamentação vigente.
Os dados e demais requisitos para o compartilhamento do serviço de iniciação de transação de pagamento na modalidade Pix devem ser consultados nos regulamentos, documentos, manuais técnicos e demais instruções desse arranjo de pagamento. Demais dados e informações detalhados de caráter técnico necessários para o referido compartilhamento deverão ainda ser disponibilizadas no Portal do Open Finance no Brasil.
7. Dados e escopo referentes ao serviço otimizado de iniciação de transação de pagamento com compartilhamento de dados (jornada otimizada)
É facultado às instituições que atuam como instituições receptoras de dados e como instituições iniciadoras de transação de pagamento o oferecimento do serviço otimizado de iniciação de transação de pagamento com compartilhamento de dados (jornada otimizada), que permite que o cliente, em uma mesma jornada, dê consentimento para:
I - o compartilhamento do serviço de iniciação de transação de pagamento; e
II - o compartilhamento de dados.
É permitida a jornada otimizada para o compartilhamento de dados selecionados durante os seguintes compartilhamentos de serviço de iniciação de transação de pagamento:
I - Transferências Inteligentes: durante o consentimento, o cliente deve poder selecionar compartilhamento de saldo disponível e limites contratados referenciados na tabela disposta na subseção 5.1 deste manual; ou
II - compartilhamento do serviço de iniciação de transação de pagamento sem redirecionamento: durante a etapa de vinculação de conta, o cliente deve poder selecionar compartilhamento de saldo disponível e limites contratados referenciados na tabela disposta na subseção 5.1 deste manual.
Os dados abrangidos pela jornada otimizada são os seguintes:
I - em relação ao compartilhamento do serviço de iniciação de transação de pagamento, aqueles dispostos nas tabelas da subseção 6.1.2 e da subseção 6.1.3 deste manual; e
II - em relação ao compartilhamento de dados, os dados de saldo disponível e de limites contratados dispostos na subseção 5.1 deste manual.
Além desses dados, devem ser observados, de forma geral, os dados dispostos nos regulamentos que disciplinem o funcionamento do arranjo de pagamento referente à respectiva transação de pagamento e demais dados estabelecidos nas especificações disponíveis no Portal do Open Finance no Brasil.
Considerando que, na jornada otimizada, o cliente poderá dar dois consentimentos, destaca-se que o consentimento para compartilhamento do serviço de iniciação de transação de pagamento deve ser considerado como primário e que o consentimento para compartilhamento de dados deve ser considerado como secundário.
Dessa forma, a finalidade e o ciclo de vida do consentimento secundário devem ser atrelados à finalidade e ao ciclo de vida do consentimento primário. Por consequência, caso o consentimento primário seja encerrado, o consentimento secundário se encerra automaticamente.
8. Dados e escopo referentes ao serviço de portabilidade de crédito
O serviço de portabilidade de crédito no Open Finance é definido como a transferência de operação de crédito da instituição credora original para a instituição proponente, por solicitação do cliente, que se dá por meio de recebimento de proposta de operação de crédito feita pela instituição proponente em condições mais vantajosas do que a operação de crédito contratada pelo cliente com a instituição credora original.
A prestação desse serviço pressupõe o prévio consentimento pelo cliente do compartilhamento de dados da instituição credora original para a instituição proponente, nos termos da regulamentação do Banco Central do Brasil.
Em relação ao escopo de dados desse serviço, os dados devem abranger, no mínimo, os campos listados na tabela a seguir, observada a documentação da Estrutura de Governança do Open Finance:
Dados
Campo
Esclarecimentos adicionais
Dados mínimos
Informações do cliente
Identificação do cliente.
Informações da instituição proponente
Identificação da instituição proponente.
Informações da instituição credora original
Identificação da instituição credora original.
Informações da operação de crédito a ser portada
Identificação do contrato.
Informações da proposta de operação de crédito
Características e informações de data e hora de criação da proposta de operação de crédito.
O serviço de portabilidade de crédito no Open Finance será implementado de forma gradual no que se refere a modalidades de operação de crédito elegíveis.
8.1 Crédito Pessoal
A modalidade de operação de empréstimo descrita como "crédito pessoal - sem consignação em folha de pagamento", conforme Anexo do Documento 3040, é elegível para o serviço de portabilidade de crédito no Open Finance.
Mediante prévio consentimento do cliente, as instituições credoras originais devem disponibilizar informações de quaisquer contratos enquadrados nessa modalidade, independentemente de suas características, para que as instituições proponentes possam apresentar suas propostas, conforme estabelecido na regulamentação do Banco Central do Brasil e na documentação da Estrutura de Governança do Open Finance.
Brasília, ........... de julho de 2026.
NOTA 599/2026-BCB/DENOR, DE 9 de JULHO de 2026
Fundamenta proposta de edição de instrução normativa que estabelece a versão 8.0 do Manual de Escopo de Dados e Serviços do Open Finance.
Senhores Chefes do Denor, do Desuc, do Desup e do Deinf,
1. A presente Nota fundamenta proposta de edição de instrução normativa pelo Departamento de Regulação do Sistema Financeiro (Denor), pelo Departamento de Supervisão de Cooperativas e de Instituições Não Bancárias (Desuc), pelo Departamento de Supervisão Bancária (Desup) e pelo Departamento de Tecnologia da Informação (Deinf), no uso da atribuição que lhes confere o art. 23, inciso I, alínea "a", do Regimento Interno do Banco Central do Brasil, anexo à Resolução BCB nº 340, de 21 de setembro de 2023, com base no art. 3º, inciso I, da Resolução BCB nº 32, de 29 de outubro de 2020.
2. A proposta de instrução normativa divulga a versão 8.0 do Manual de Escopo de Dados e Serviços do Open Finance. A alteração se refere à inclusão de dados e escopo referentes ao serviço de portabilidade de crédito.
3. Cumpre ressaltar que, por força do art. 5º da Lei nº 13.874, de 20 de setembro de 2019, as propostas de edição e de alteração de atos normativos de interesse geral de agentes econômicos ou de usuários dos serviços prestados, editadas por órgão ou entidade da administração pública federal, incluídas as autarquias e as fundações públicas, serão precedidas da realização de análise de impacto regulatório (AIR), que conterá informações e dados sobre os possíveis efeitos do ato normativo para verificar a razoabilidade do seu impacto econômico.
4. Por sua vez, o Decreto nº 10.411, de 30 de junho de 2020, que regulamenta essa Lei, em seu art. 4º, inciso II, estabelece que a AIR poderá ser dispensada, desde que haja decisão fundamentada do órgão ou da entidade competente, nas hipóteses de ato normativo destinado a disciplinar direitos ou obrigações definidos em norma hierarquicamente superior que não permita, técnica ou juridicamente, diferentes alternativas regulatórias.
5. Desse modo, como a proposta em comento trata da inclusão da portabilidade de crédito, serviço regulamentado em resolução do Conselho Monetário Nacional, que poderá ser prestado também por meio do Open Finance, em consonância com as especificações técnicas desenvolvidas no âmbito da Estrutura de Governança do Open Finance e já implementadas pelas instituições participantes do Open Finance, consideramos que as alterações e esclarecimentos propostos enquadram-se na possibilidade de dispensa desse dispositivo, uma vez que a instrução normativa ora proposta visa a disciplinar direitos ou obrigações definidos em norma hierarquicamente superior.
À consideração de V.Sas.
JANAÍNA PIMENTA ATTIE IVENS ARUA NEVES DE MIRANDA
Consultora do Denor Chefe Adjunto do Desuc
​ MARCO GUIMARÃES VERRONE ANDRE BOKEL DA COSTA
Chefe Adjunto do Desup Chefe Adjunto do Deinf
De acordo.
MARDILSON FERNANDES QUEIROZ MARCELO COLLI INGLEZ
Chefe do Denor Chefe do Desuc, substituto
GEORGE OHARA ANDRE BOKEL DA COSTA
Chefe do Desup, substituto Chefe do Deinf, substituto
