ANEXO À INSTRUÇÃO NORMATIVA BCB Nº 706, DE 29 DE JANEIRO DE 2026
Manual de Monitoramento do Open Finance Versão 3.0
Sumário de alterações
Data
Versão
Descrição das alterações
.../1/2026
3.0
Subseção 2.4: alteração das regras para envio de reportes à Plataforma de Coleta de Métricas (PCM).
Subseção 2.6.2: alteração da fórmula de cálculo da taxa de conversão mínima.
Subseção 3.2.1: inclusão de análise de completude do relatório de situações de desconformidade.
Subseção 3.2.2: estabelecimento de novas regras para entrada em execução de planos de adequação.
Subseção 3.2.3: alteração do prazo de apresentação do diagnóstico sobre a taxa de conversão de dias corridos para dias úteis.
Subseção 3.3: atualização do item VI com novos papéis referentes à portabilidade de crédito.
Subseção 3.4.1: inclusão de explicação sobre segunda ocorrência reiterada.
Termos de Uso
Este manual define os princípios básicos do monitoramento do Open Finance, complementando a regulamentação vigente sobre o tema.
O manual será revisto e atualizado periodicamente a fim de preservar a compatibilidade com a regulamentação, bem como incorporar os aprimoramentos decorrentes da evolução do Open Finance.
Informações mais detalhadas e exemplos da aplicação deste manual poderão ser encontradas no Portal do Open Finance no Brasil (https://openfinancebrasil.org.br/), mantido pela Estrutura de Governança do Open Finance.
Sugestões, críticas ou pedidos de esclarecimento de dúvidas relativas ao conteúdo deste documento podem ser enviados ao Banco Central do Brasil por meio dos canais institucionais dessa autarquia.
Referências
Estas especificações têm como base, referenciam e complementam, quando aplicável, os seguintes documentos:
Referência
Origem
Resolução Conjunta nº 1, de 2020
https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolu%C3%A7%C3%A3o%20Conjunta&numero=1
Resolução BCB nº 32, de 2020
https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolu%C3%A7%C3%A3o%20BCB&numero=32
Lei nº 13.709, de 2018, Lei Geral de Proteção de Dados Pessoais (LGPD)
http://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/L13709.htm
1. Introdução
Este manual foi elaborado com o objetivo de garantir que o monitoramento do Open Finance, a ser realizado pela Estrutura de Governança do Open Finance, seja capaz de verificar se as instituições participantes estão em conformidade com as obrigações previstas na regulamentação do Banco Central do Brasil e em documentos elaborados pela Estrutura de Governança do Open Finance, conforme definido pela regulamentação vigente.
Convém destacar que as determinações referentes ao monitoramento de serviços de tecnologia estabelecidas neste manual são complementares e não excludentes em relação ao determinado pelo Manual de Serviços Prestados pela Estrutura de Governança do Open Finance.
Este manual de monitoramento não se limita a questões de tecnologia, uma vez que o adequado monitoramento da infraestrutura do Open Finance envolve diferentes aspectos, sendo condição para que o sistema continue evoluindo de forma ágil, eficiente e segura.
Entre esses aspectos, destacam-se os seguintes itens:
I - performance de application programming interfaces (APIs) e requisitos não funcionais;
II - especificações, cadastros, certificação e publicação de APIs;
III - metas de prazo máximo para atendimento de tickets;
IV - reporte de informações;
V - qualidade de dados; e
VI - experiência do cliente.
É importante destacar que a Estrutura de Governança do Open Finance deve realizar o monitoramento dos diversos itens mencionados acima por meio de avaliação de todas as ocorrências, sendo permitido o monitoramento por amostragem apenas em situações específicas expressamente autorizadas pelo Banco Central do Brasil.
A Estrutura de Governança do Open Finance deve armazenar e dar publicidade a dados estatísticos e indicadores referentes aos diversos itens monitorados. Além disso, as instituições participantes devem fornecer dados de qualidade e com detalhamento suficiente que permitam que a Estrutura de Governança do Open Finance implemente o processo de monitoramento de que trata este manual.
Adicionalmente, ressalta-se que o processo de monitoramento do Open Finance deve ser documentado por meio de uma política de monitoramento, que deve compreender os itens monitorados pelo sistema, o fluxo de gestão do monitoramento, os papéis e as responsabilidades dos integrantes desse fluxo e as medidas aplicáveis em situações de desconformidade.
Toda a documentação relativa ao processo de monitoramento é de responsabilidade da Estrutura de Governança do Open Finance e deve ser mantida à disposição do Banco Central do Brasil por cinco anos.
2. Itens monitorados
Esta seção descreve os itens que devem ser monitorados pela Estrutura de Governança do Open Finance. Tais itens e o detalhamento de cada um deles representam o mínimo exigido, cabendo à Estrutura de Governança do Open Finance, independentemente de alteração normativa, garantir que os itens monitorados sejam expandidos sempre que houver necessidade, com vistas ao objetivo final do processo de monitoramento, que é o bom funcionamento do Open Finance para todas as partes interessadas: instituições participantes, clientes e sociedade.
Adicionalmente, considerando que as ferramentas e processos de monitoramento do Open Finance estão em constante processo de desenvolvimento, este manual se restringirá a aspectos em que já é possível obter métricas para monitoramento, sendo que as demais métricas e indicadores serão posteriormente incorporados à medida que estiverem disponíveis para acompanhamento.
Nesse sentido, a obtenção dos itens monitorados deve ser realizada, prioritariamente, por meio de ferramentas da Estrutura de Governança do Open Finance. Na ausência dessas ferramentas ou em caso de ferramentas que consigam obter apenas parcialmente os itens monitorados, as instituições participantes devem reportar as informações necessárias para que a Estrutura de Governança do Open Finance consiga cumprir todas as etapas de monitoramento descritas neste manual ou em sua documentação.
2.1 Performance de APIs e requisitos não funcionais
A Estrutura de Governança do Open Finance deve monitorar diversas questões relacionadas à performance de APIs e requisitos não funcionais, entre as quais, deverão ser priorizados, no mínimo, para fins do processo de monitoramento, os seguintes itens:
I - tempo de resposta das APIs das instituições participantes;
II - disponibilidade das APIs das instituições participantes; e
III - volume de requisições com status code HTTP 529.
Para fins do processo de monitoramento, admite-se que sejam utilizados tickets abertos automaticamente por ferramentas da Estrutura de Governança do Open Finance ou tickets específicos, e que a aplicação do fluxo de monitoramento ocorra de forma mensal, cabendo ressaltar, contudo, que as instituições participantes devem corrigir as desconformidades de forma tempestiva, assim que receberem os tickets.
O Service Level Agreement (SLA) e os métodos de cálculo referentes ao tempo de resposta e à disponibilidade de APIs das instituições participantes, bem como do volume de requisições com status code HTTP 529, constam no Manual de APIs do Open Finance.
2.2 Especificações, cadastros, certificação e publicação de APIs
Esta subseção abordará os itens monitorados referentes a especificações das APIs; cadastros no Diretório de Participantes, certificação e publicação dessas APIs. Destaca-se que os itens desta subseção precisam ser cumpridos na sua totalidade, de modo que qualquer desvio em relação ao padrão estabelecido ensejará a aplicação de medidas à instituição participante em desconformidade.
A ocorrência de desconformidades em relação aos itens tratados nesta subseção ensejará a abertura de tickets à instituição participante em desconformidade, cujos prazos máximos de atendimento constam no Manual de Serviços Prestados pela Estrutura de Governança do Open Finance.
A Estrutura de Governança do Open Finance deve monitorar, no mínimo, os seguintes itens referentes a especificações, cadastros, certificação e publicação de APIs das instituições participantes:
I - acompanhamento da implementação de versões iniciais e de novas versões de APIs: a Estrutura de Governança do Open Finance deve:
a) monitorar e exigir o cumprimento dos marcos intermediários do processo de certificação e publicação em produção de versões iniciais e de novas versões de APIs, sejam eles definidos em regulamentação ou pela própria Estrutura de Governança do Open Finance; e
b) verificar e exigir a devida publicação das APIs das instituições participantes no Diretório de Participantes e em ambiente produtivo;
II - acompanhamento de versões implementadas de APIs e artefatos associados: a Estrutura de Governança do Open Finance deve:
a) verificar e exigir que as APIs e artefatos associados das instituições participantes em ambiente produtivo estejam aderentes às especificações funcionais e de segurança em vigor; e
b) verificar e exigir que as informações relativas às APIs, incluindo as adequadas certificações, estejam corretamente atualizadas nas ferramentas e nos sistemas associados aos serviços prestados pela Estrutura de Governança do Open Finance;
III - acompanhamento das modalidades de participação: a Estrutura de Governança do Open Finance deve verificar se as modalidades de participação cadastradas pelas instituições participantes estão em conformidade com o estabelecido na regulamentação, quando houver informações disponíveis para tal verificação, e adotar as providências necessárias para a regularização; e
IV - acompanhamento do processo de retirada das versões antigas das APIs de ambiente produtivo e do cadastro no Diretório de Participantes: a Estrutura de Governança do Open Finance deve verificar se existem versões antigas das APIs em ambiente produtivo ou cadastradas no Diretório de Participantes, de acordo com o cronograma definido pela regulamentação ou pela Estrutura de Governança do Open Finance. No caso de versões major, retirar as versões retired do Diretório de Participantes ao final do período de convivência e exigir que as instituições participantes deixem de chamá-las e as retirem do ambiente produtivo.
A Estrutura de Governança do Open Finance deve realizar a gestão do processo de obtenção de maturidade dos motores de certificação funcional e de segurança, com vistas a possibilitar que as instituições participantes consigam cumprir as obrigações do inciso I desta subseção.
Destaca-se que as desconformidades em relação aos itens de que trata esta subseção devem ser apuradas assim que forem detectadas.
Para fins do processo de monitoramento, admite-se que sejam utilizados tickets abertos automaticamente por ferramentas da Estrutura de Governança do Open Finance ou tickets específicos, e que a aplicação do fluxo de monitoramento ocorra de forma mensal, cabendo ressaltar, contudo, que as instituições participantes devem corrigir as desconformidades de forma tempestiva, assim que receberem os tickets.
Em relação aos itens desta subseção, com exceção do inciso I, alínea "b", caso as instituições participantes consigam corrigir as desconformidades dentro do prazo máximo permitido, de acordo com o Manual de Serviços Prestados pela Estrutura de Governança do Open Finance, tais situações de desconformidade devem ser registradas nas informações disponibilizadas às instituições participantes para realização da gestão de situações de desconformidade, conforme seção 5 deste Manual, mas não devem ser consideradas para fins de aplicação de medidas.
2.3 Metas de prazo máximo para atendimento de tickets
A Estrutura de Governança do Open Finance deve monitorar, no mínimo, o prazo para atendimento de:
I - tickets relativos a demandas de resolução de incidentes, abertos bilateralmente entre instituições participantes no Service Desk; e
II - tickets abertos pela Estrutura de Governança do Open Finance: a Estrutura de Governança do Open Finance deve acompanhar os prazos de cada ticket aberto por ela para atendimento por parte das instituições participantes. Os tickets abertos pela Estrutura de Governança do Open Finance compreendem aqueles abertos por órgãos da Estrutura de Governança do Open Finance, fornecedores e ferramentas, tal como a Ferramenta de Validação em Produção (FVP).
A Estrutura de Governança do Open Finance deve acompanhar, monitorar e demandar solução para cada ticket, bilateral ou aberto por ela, caso não tenha sido resolvido dentro do prazo máximo para seu atendimento, e gerar estatísticas sobre o prazo de atendimento de cada ticket, bilateral ou aberto por ela, que estiver encerrado ou que estiver com o prazo vencido.
As instituições participantes devem respeitar os prazos máximos de atendimento de tickets estabelecidos no Manual de Serviços Prestados pela Estrutura de Governança do Open Finance. Admite-se, para fins de avaliação sobre a conformidade do item monitorado de que trata esta subseção, que as instituições participantes atendam ao prazo máximo para 80% de seus tickets, desde que não apresentem tickets com atraso superior ao dobro do prazo máximo estabelecido no referido Manual.
Para fins do processo de monitoramento, o período de apuração referente ao item de que trata esta subseção é mensal.
2.4 Reporte de informações
As instituições participantes devem disponibilizar, nos prazos definidos pela Estrutura de Governança do Open Finance, dados com qualidade adequada e com detalhamento suficiente, de forma a permitir que a Estrutura de Governança do Open Finance implemente as funcionalidades dispostas neste manual.
A Estrutura de Governança do Open Finance deve estabelecer, para cada caso, os dados que precisam ser enviados pelas instituições participantes, bem como sua forma de envio, periodicidade, entre outros itens cabíveis.
Em relação à Plataforma de Coleta de Métricas (PCM), as instituições participantes devem enviar pelo menos 95% dos reportes de um determinado dia até 8h00 do próximo dia e pelo menos 99% dos reportes em até sete dias a partir da data e horário das transações.
Admite-se que uma instituição não atenda à meta diária de envio de reportes em até três dias de determinado mês, desde que ela tenha enviado pelo menos 99% dos reportes desses dias em até sete dias a partir da data e horário das transações.
Para atendimento da meta de envio de pelo menos 95% dos reportes até 8h00 do próximo dia a partir da data e horário das transações, reportes com status "UNPAIRED" não podem exceder 5% do volume de chamadas da instituição para cada API.
Para atendimento da meta de envio de pelo menos 99% dos reportes em até sete dias a partir da data e horário das transações, reportes com status "UNPAIRED" ou "PAIRED INCONSISTENT" não podem exceder 1% do volume de chamadas da instituição para cada API.
Caso a instituição não consiga enviar os reportes devido a falhas da PCM ou a falhas em processos associados de responsabilidade da Estrutura de Governança do Open Finance, a meta de envio dos reportes até 8h00 do próximo dia não precisa ser atendida, mas a instituição continua obrigada a enviá-los em até sete dias a partir da data e horário das transações.
Todos os reportes, com exceção dos reportes descartados, devem estar em conformidade com as especificações da API de integração com a PCM em relação a aspectos de completude dos reportes e de completude e validade dos dados, inclusive quanto ao campo "additionalInfo".
Para fins do processo de monitoramento, o período de apuração referente aos itens de que trata esta subseção é mensal e deve haver controle diário do envio e da conformidade dos reportes. Caso seja detectado que uma instituição participante não está atendendo alguma das metas estabelecidas, ela deve ser notificada e retornar à normalidade tempestivamente. Destaca-se que eventuais falhas no processo de geração de notificações ao longo do mês não devem impactar a aplicação do fluxo de monitoramento mensal.
2.5 Qualidade de dados
As instituições participantes do Open Finance devem garantir a qualidade dos dados informados por meio de suas APIs, com observância, no mínimo, dos seguintes itens:
I - completude: preenchimento de todos os campos obrigatórios dos endpoints de suas APIs e, quando aplicável, dos campos opcionais e condicionais;
II - consistência: ausência de divergências entre os dados informados por meio de suas APIs e os dados divulgados nos canais eletrônicos disponibilizados aos seus clientes, no caso de informações divulgadas em tais canais;
III - conformidade: aderência dos dados informados por meio de suas APIs aos padrões e às regras de negócios especificados no Open Finance;
IV - validade: representação dos dados informados nos diversos campos dos endpoints de suas APIs de acordo com sua definição, em termos de formato, tipo, valores permitidos, entre outros atributos;
V - atualidade: relevância dos dados informados por meio de suas APIs no tempo; e
VI - unicidade: unicidade dos dados informados por meio de suas APIs, ou seja, ausência de duplicidade de informações.
Visando à manutenção da qualidade de dados do Open Finance, as instituições participantes que tiverem aderido, obrigatória ou voluntariamente, ao compartilhamento de dados devem implementar o motor de qualidade de dados, conforme parâmetros definidos pela Estrutura de Governança do Open Finance, e utilizá-lo na sua atuação como transmissora de dados.
O reporte de informações referentes à utilização do motor de qualidade de dados deve ser realizado por cada instituição participante, não sendo válido o reporte de forma consolidada pelo conglomerado. Admite-se que as cooperativas de crédito reportem suas informações de forma consolidada por meio dos sistemas cooperativos.
Com base nos relatórios gerados a partir da análise de tickets relativos à qualidade de dados e de estatísticas provenientes do uso do motor de qualidade de dados pelas instituições participantes, a Estrutura de Governança do Open Finance deve manter índice de qualidade de dados que demonstre o desempenho individual de cada instituição. Esse índice deve estar em constante atualização de acordo com a evolução do Open Finance.
As instituições participantes do Open Finance devem manter SLA no índice de qualidade de dados igual ou superior a 95%. Instituições participantes com desempenho inferior a esse valor serão consideradas em desconformidade.
No caso de versões de APIs em que haja período de piloto em produção, o cálculo do índice de qualidade de dados não deve contemplá-las, com vistas a permitir que essas APIs atinjam maior maturidade, devendo, contudo, estarem contempladas no cálculo do referido índice a partir da data de go-live.
Durante o período do piloto em produção, os tickets gerados devem respeitar os prazos máximos estabelecidos no Manual de Serviços Prestados pela Estrutura de Governança do Open Finance e, por consequência, serem monitorados de acordo com a subseção 2.3 deste Manual, a fim de que a qualidade de dados seja também aprimorada na fase de piloto em produção.
Para fins do processo de monitoramento, o período de apuração referente aos itens de que trata esta subseção é mensal.
2.6 Experiência do cliente
2.6.1 Jornada do cliente
A Estrutura de Governança do Open Finance deve monitorar as jornadas dos clientes, de acordo com as diferentes modalidades de:
I - fluxos existentes, considerando os diferentes canais, dispositivos e ambientes em que a jornada Open Finance é disponibilizada, tais como aplicativo para aplicativo, aplicativo para navegador e vice-versa no mesmo dispositivo; aplicativo para navegador e vice-versa entre dispositivos diferentes; e navegador para navegador;
II - público-alvo, pessoa natural ou pessoa jurídica;
III - alçadas, simples ou múltiplas; e
IV - compartilhamento de dados ou de serviços, contemplando cada um de seus produtos.
A Estrutura de Governança do Open Finance deve gerar as próprias evidências das jornadas dos clientes ou contratar fornecedores independentes para tal, cabendo a ressalva de que não será admitida a geração de evidências das jornadas por meio do envio de jornadas pela própria instituição participante. Admite-se a geração de evidências pela própria instituição participante para fins de comprovação de correção das desconformidades, a serem avaliadas pela Estrutura de Governança do Open Finance para encerramento de tickets.
Para fins do processo de monitoramento, o período de apuração do monitoramento da jornada do cliente será definido pela Estrutura de Governança do Open Finance e dar-se-á na mesma periodicidade das rodadas de avaliação a serem executadas com as instituições participantes selecionadas.
A Estrutura de Governança do Open Finance definirá os escopos de avaliação de cada rodada e, com exceção de marcas ou instituições que não atuem nos escopos definidos para uma determinada rodada de avaliação, devem estar presentes, obrigatoriamente, em todas as rodadas, as marcas consideradas prioritárias das instituições participantes de maior relevância, conforme definição do Banco Central do Brasil.
Caso a instituição participante corrija a desconformidade dentro do seu prazo máximo para atendimento, aquela situação de desconformidade deve ser registrada nas informações disponibilizadas às instituições participantes para realização da gestão de situações de desconformidade, conforme seção 5 deste Manual, mas não deve ser considerada para fins de aplicação de medidas.
Para fins da análise quanto à verificação da correção da desconformidade, a instituição participante deve enviar evidências à Estrutura de Governança do Open Finance assim que a correção for efetuada e a Estrutura de Governança do Open Finance deve avaliar tais evidências tempestivamente. Caso a instituição participante não seja capaz de gerar evidências em relação a determinado escopo ou público-alvo, a geração das evidências para a análise quanto à verificação da correção da desconformidade deve ser realizada pela Estrutura de Governança do Open Finance, diretamente ou por meio de fornecedores independentes contratados. A desconformidade somente será considerada como corrigida após a análise de tais evidências.
2.6.2 Taxa de conversão
A Estrutura de Governança do Open Finance deve monitorar a taxa de conversão de jornadas de compartilhamento de dados e de jornadas de iniciação de pagamentos.
As taxas mínimas de conversão referentes a jornadas de compartilhamento de dados e a jornadas de iniciação de pagamentos são:
I - compartilhamento de dados: 80% da média ponderada por consentimentos solicitados das três maiores taxas de conversão de instituições transmissoras de dados nos últimos três meses, incluindo o mês de referência;
II - iniciação de transação de pagamento: 80% da média ponderada por consentimentos solicitados das três maiores taxas de conversão de instituições detentoras de conta nos últimos três meses, incluindo o mês de referência; e
III - vínculo: 80% da média ponderada por vínculos solicitados das três maiores taxas de conversão de instituições detentoras de conta nos últimos três meses, incluindo o mês de referência.
Para a apuração das três maiores taxas de conversão, deve-se considerar as seguintes instituições:
I - para compartilhamento de dados, as instituições transmissoras de dados pertencentes a conglomerados ou a sistemas cooperativos que representem 99% do estoque total de consentimentos ativos no período de apuração;
II - para iniciação de transação de pagamento, as instituições detentoras de conta pertencentes a conglomerados ou a sistemas cooperativos nos quais forem gerados 99% dos consentimentos no período de apuração; e
III - para vínculo, as instituições detentoras de conta pertencentes a conglomerados ou a sistemas cooperativos nos quais forem gerados 99% dos vínculos no período de apuração.
Há um limite de tolerância de três pontos percentuais para as taxas mínimas de conversão, de que trata esta subseção.
As taxas de conversão de que trata esta subseção devem ser calculadas da seguinte forma:
I - compartilhamento de dados: quantidade de consentimentos cujos "access tokens" foram gerados com sucesso em relação à quantidade de "consentIds" gerados para clientes redirecionados para a instituição transmissora de dados; e
II - iniciação de transação de pagamento: quantidade de consentimentos cujos "access tokens" foram gerados com sucesso em relação à quantidade de "consentIds" gerados para clientes titulares de conta redirecionados para a instituição detentora de conta; e
III - vínculo: quantidade de vínculos autorizados em relação às solicitações de criação de vínculo por clientes titulares de conta redirecionados para a instituição detentora de conta.
Considera-se como "cliente" nas fórmulas acima o CPF/CNPJ que possui credencial autenticadora para prosseguir no fluxo monitorado.
O período de apuração das taxas de conversão é mensal e devem ser consideradas, para cada mês, todas as semanas cujas sextas-feiras ocorreram no mês.
Para fins do processo de monitoramento, o período de apuração referente ao item de que trata esta subseção é mensal.
3. Processo de monitoramento
O processo de monitoramento do Open Finance, realizado pela Estrutura de Governança do Open Finance, em conjunto com as instituições participantes, deve ser pautado pelos princípios de transparência, melhoria contínua, eficiência e assertividade, e ter por objetivo assegurar que as instituições participantes estejam em consonância com as obrigações previstas em documentos elaborados no âmbito da Estrutura de Governança do Open Finance e na regulamentação do Banco Central do Brasil.
A Estrutura de Governança do Open Finance deve definir e documentar o processo de monitoramento por meio de uma política específica (Política de Monitoramento), que deve compreender, no mínimo, o fluxo de monitoramento e de aplicação de medidas, os papéis e as responsabilidades dos integrantes desse fluxo e as medidas aplicáveis em caso de descumprimento da performance desejada.
Outros aspectos referentes ao processo de monitoramento, tais como os itens monitorados, também devem ser documentados, mas, considerando necessidade de atualização mais frequente, poderão constar de documento auxiliar à Política de Monitoramento ou diretamente no portal do desenvolvedor.
Caso seja detectado que uma instituição participante não esteja em conformidade com um item monitorado, o caso deve ser acompanhado por um ticket do Service Desk, podendo ser utilizado um ticket que já tinha sido aberto referente ao caso ou ser aberto novo ticket, específico ou que consolide diversas situações de desconformidade.
3.1 Fluxo de monitoramento e de aplicação de medidas
A Política de Monitoramento deve descrever o fluxo de monitoramento e de aplicação de medidas discriminadas por cada integrante do fluxo, contemplando, no mínimo, as seguintes etapas integrantes desse processo:
I - verificação dos SLAs, taxas mínimas de conversão e prazos máximos de atendimento de tickets do Service Desk;
II - identificação de situações de desconformidade;
III - acompanhamento das situações de desconformidade por meio de tickets do Service Desk;
IV - avaliação da resposta das instituições participantes em desconformidade em relação às situações de desconformidade;
V - envio do caso para análise e ação de eventuais instâncias superiores, em caso de continuidade da situação de desconformidade ou do impacto da situação no bom funcionamento do Open Finance; e
VI - aplicação de medidas às instituições participantes em desconformidade.
3.2 Medidas aplicáveis
Em caso de situações de desconformidade, a Política de Monitoramento deve prever a aplicação das seguintes medidas:
I - entrega de relatório de situações de desconformidade;
II - apresentação de plano de adequação; e
III - apresentação de avaliação específica sobre taxa de conversão.
Esta subseção contempla disposições mínimas sobre medidas aplicáveis a situações de desconformidade em relação aos itens monitorados que constam na seção 2 deste manual.
3.2.1 Relatório de situações de desconformidade
O relatório de situações de desconformidade, mencionado no inciso I da subseção 3.2, deve:
I - ser apresentado pela instituição participante em desconformidade;
II - conter descrição do ocorrido e solução adotada para correção;
III - ser acompanhado de ciência do diretor responsável pelo compartilhamento de dados e serviços no âmbito do Open Finance, conforme fluxos internos de cada instituição participante do Open Finance;
IV - ser apresentado por meio de canais oficiais da instituição participante em até cinco dias úteis após solicitação da Estrutura de Governança do Open Finance;
V - ser avaliado em relação ao cumprimento dos incisos I a IV desta subseção pela Estrutura de Governança do Open Finance; e
VI - estar disponível ao Banco Central do Brasil.
Em caso de ausência do diretor responsável, admite-se a ciência de outro diretor estatutário.
Instituições que, quando demandadas, não apresentem o relatório de que trata esta subseção no prazo definido devem apresentar o plano de adequação de que trata a subseção 3.2.2.
3.2.2 Plano de adequação
O plano de adequação, mencionado no inciso II da subseção 3.2, deve:
I - ser apresentado pela instituição participante em desconformidade;
II - conter cronograma detalhado para que a situação de desconformidade seja solucionada e elementos mitigadores para prevenção de novas ocorrências;
III - ser assinado pelo diretor responsável pelo compartilhamento de dados e serviços no âmbito do Open Finance;
IV - ser apresentado por meio de canais oficiais da instituição participante em até dez dias úteis após solicitação da Estrutura de Governança do Open Finance; e
V - ser avaliado e aprovado pela Estrutura de Governança do Open Finance.
Em caso de ausência do diretor responsável, admite-se a assinatura de outro diretor estatutário.
O plano de adequação deve entrar em execução assim que for apresentado, conforme o item IV desta subseção. A Estrutura de Governança do Open Finance deve avaliar o plano de acordo com o item V desta subseção e, caso esteja satisfatório, aprová-lo e acompanhar a sua execução. Caso haja eventual necessidade de ajustes, a depender da avaliação da Estrutura de Governança do Open Finance, a instituição participante deve efetuar as alterações solicitadas no plano em execução e reapresentá-lo à Estrutura de Governança do Open Finance em até cinco dias úteis. A Estrutura de Governança do Open Finance deve avaliar novas versões dos planos de adequação e aprová-lo somente após considerá-lo satisfatório.
Não devem ser consideradas as desconformidades identificadas em itens monitorados constantes de plano de adequação que esteja em implementação e sendo cumprido conforme aprovado pela Estrutura de Governança do Open Finance e, quando for o caso, pelo Banco Central do Brasil, enquanto estiverem sendo observadas melhorias condizentes com o esperado.
Caso o plano de adequação em execução por instituição participante em desconformidade não apresente resultados condizentes com o esperado, a Estrutura de Governança do Open Finance deve comunicar o Banco Central do Brasil a respeito do caso com as informações de que trata a subseção 3.4.1.
Os planos de adequação que incluam itens monitorados constantes da subseção 2.3 devem contemplar os ajustes nos processos internos, de modo que as equipes de atendimento das instituições participantes passem a cumprir os prazos estabelecidos, e conter cronograma detalhado para solução de cada ticket que ainda esteja em aberto.
A Estrutura de Governança do Open Finance deve dar ciência ao Banco Central do Brasil sobre a eventual não apresentação de plano de adequação dentro do prazo regulamentar.
Os planos de adequação devem estar disponíveis ao Banco Central do Brasil, que poderá neles requerer ajustes.
3.2.3 Avaliação específica sobre taxa de conversão
A avaliação específica sobre taxa de conversão, mencionada no inciso III da subseção 3.2, deve:
I - ser apresentada pela instituição participante em desconformidade que apresentar taxa de conversão inferior ao patamar de que trata a subseção 3.4.2.1;
II - conter diagnóstico sobre sua taxa de conversão;
III - ser apresentada em até dez dias úteis após a detecção da desconformidade; e
IV - ter seus resultados submetidos à Estrutura de Governança do Open Finance e ao Banco Central do Brasil.
Após análise da Estrutura de Governança do Open Finance, nos casos em que a maior parte dos erros que ocasionaram a taxa de conversão inferior ao referido patamar for referente a aspectos de implementação, tanto no que se refere a questões técnicas ou relacionadas à jornada do cliente, a instituição participante em desconformidade deverá contratar empresa especializada independente para realizar um diagnóstico mais completo sobre a taxa de conversão da instituição participante em desconformidade.
O referido diagnóstico deve ser apresentado em até 65 dias úteis após solicitação pela Estrutura de Governança do Open Finance e tem validade por doze meses.
3.3 Ocorrências reiteradas
A apresentação de situação de desconformidade em relação a um mesmo item monitorado por uma instituição participante pode configurar uma ocorrência reiterada.
A seguir, apresenta-se as regras, por item monitorado, para que determinado caso seja configurado como uma ocorrência reiterada:
I - performance de APIs e requisitos não funcionais: apresentação de situação de desconformidade no decurso de três períodos de apuração após detecção da desconformidade inicial. Considera-se cada um dos incisos da subseção correspondente de forma separada. Mesmo que a situação de desconformidade tenha ocorrido em endpoint distinto da desconformidade inicial, considera-se ocorrência reiterada. O período de apuração para fins de detecção de ocorrência reiterada é mensal;
II - especificações, cadastros, certificação e publicação das APIs: apresentação de situação de desconformidade no decurso de três períodos de apuração após detecção da desconformidade inicial. Considera-se cada um dos incisos da subseção correspondente de forma separada. Mesmo que a situação de desconformidade tenha ocorrido em API distinta da desconformidade inicial, considera-se ocorrência reiterada. O período de apuração para fins de detecção de ocorrência reiterada é mensal;
III - metas de prazo máximo para atendimento de tickets: apresentação de situação de desconformidade no decurso de três períodos de apuração após detecção da desconformidade inicial. O período de apuração para fins de detecção de ocorrência reiterada é mensal;
IV - reporte de informações: apresentação de situação de desconformidade no decurso de três períodos de apuração após detecção da desconformidade inicial. O período de apuração para fins de detecção de ocorrência reiterada é mensal;
V - qualidade de dados: apresentação de situação de desconformidade no decurso de três períodos de apuração após detecção da desconformidade inicial. O período de apuração para fins de detecção de ocorrência reiterada é mensal;
VI - experiência do cliente - jornada do cliente: apresentação de situação de desconformidade no decurso de quatro ciclos de monitoramento após detecção da desconformidade inicial para o mesmo papel (detentor de conta, iniciador de transação de pagamento, transmissor de dados, receptor de dados, credora original ou proponente), para o mesmo público-alvo (pessoa natural ou pessoa jurídica) e para a mesma marca. O período de apuração para fins de detecção de ocorrência reiterada será no início do mês seguinte após o término do prazo máximo para resolução das desconformidades identificadas pelo monitoramento da jornada do cliente; e
VII - experiência do cliente - taxa de conversão: apresentação de situação de desconformidade no decurso de três períodos de apuração após detecção da desconformidade inicial. Considera-se cada um dos incisos da subseção correspondente de forma separada. O período de apuração para fins de detecção de ocorrência reiterada é mensal.
3.4 Regra de aplicação de medidas
3.4.1 Regra geral
Na hipótese de detecção de situações de desconformidade em relação a um item monitorado, a instituição participante em desconformidade deve apresentar à Estrutura de Governança do Open Finance o relatório de que trata a subseção 3.2.1.
Caso a instituição participante apresente situação de desconformidade em relação a um mesmo item monitorado de forma reiterada, conforme a subseção 3.3, ela deve apresentar o plano de adequação de que trata a subseção 3.2.2.
Em caso de segunda ocorrência reiterada, que se configura pela apresentação de desconformidade em relação aos prazos de que trata a subseção 3.3, de acordo com cada item monitorado, contados a partir do fim da execução de plano de adequação, o órgão de direção superior da Estrutura de Governança do Open Finance, conforme regulamentação do Banco Central do Brasil, deve comunicar ao Banco Central do Brasil a respeito do caso com, no mínimo, as seguintes informações:
I - dispositivo descumprido de ato normativo do Conselho Monetário Nacional ou do Banco Central do Brasil ou da documentação técnica da Estrutura de Governança do Open Finance;
II - relato descritivo do caso;
III - histórico de todas as informações disponíveis; e
IV - documentação comprobatória.
A Estrutura de Governança do Open Finance deve informar à instituição participante em desconformidade a respeito da comunicação ao Banco Central do Brasil.
Após a comunicação ao Banco Central do Brasil, a Estrutura de Governança do Open Finance deve continuar acompanhando a instituição participante em desconformidade, que deve apresentar novos planos de adequação até que a desconformidade seja cessada. Assim que a desconformidade for cessada, a Estrutura de Governança do Open Finance deve dar ciência ao Banco Central do Brasil.
3.4.2 Regras específicas
As medidas aplicáveis de que trata esta subseção são complementares às medidas dispostas na subseção 3.4.1.
3.4.2.1 Experiência do Cliente - Taxa de conversão
Na hipótese de a taxa de conversão ficar inferior a 60% das taxas mínimas de conversão de que trata a subseção 2.6.2, a instituição participante em desconformidade deve apresentar a avaliação de que trata a subseção 3.2.3.
3.5 Comunicação do processo de monitoramento
A comunicação do processo de monitoramento é aspecto fundamental para que as instituições participantes tenham amplo conhecimento acerca dos itens que estão sendo monitorados, da performance desejada, de como se dá o fluxo de monitoramento e de aplicação de medidas, quais os papéis e responsabilidades de cada integrante desse fluxo e quais são as medidas aplicáveis.
3.5.1 Comunicação ampla às instituições participantes
A Estrutura de Governança do Open Finance deve comunicar, de forma ampla, às instituições participantes como se dá o processo de monitoramento no Open Finance, abordando, no mínimo, os itens monitorados, os SLAs, as taxas mínimas de conversão e os prazos máximos de atendimento de tickets, o fluxo de monitoramento e de aplicação de medidas, os papéis e responsabilidades e as medidas aplicáveis.
A estratégia de comunicação deve considerar que alguns desses itens podem sofrer alterações frequentes e, assim, atualizações tempestivas são necessárias, para que as instituições participantes estejam sempre bem-informadas em relação ao processo de monitoramento.
3.5.2 Comunicação específica às instituições participantes
A Estrutura de Governança do Open Finance deve disponibilizar informações sobre a performance de cada instituição participante em relação aos itens monitorados, com vistas ao acompanhamento por parte dessas instituições em relação à sua performance, com maior destaque para os itens que estiverem em situação de desconformidade com a performance desejada.
Essas informações devem ser prestadas em nível de detalhe suficiente para que a instituição participante possa verificar a fidedignidade dos dados analisados no fluxo de monitoramento e de aplicação de medidas em relação aos seus dados internos.
4. Dados estatísticos e indicadores sobre a atuação das instituições participantes no Open Finance
A Estrutura de Governança do Open Finance deve prover os meios para armazenamento e compilação de dados estatísticos referentes à atuação das instituições participantes no Open Finance e à sua performance em relação aos itens monitorados, bem como produzir e disponibilizar indicadores com base nesses dados.
Visando a garantir o bom funcionamento do sistema, a Estrutura de Governança do Open Finance pode coletar e armazenar outras métricas relevantes não mencionadas explicitamente neste manual, ressaltando-se que estão vedados a coleta e o armazenamento de dados dos clientes, ainda que anonimizados ou pseudonimizados.
4.1 Divulgação de dados estatísticos e de indicadores sobre a atuação das instituições participantes
Os dados estatísticos referentes à atuação das instituições participantes devem abranger, no mínimo, informações acerca:
I - da quantidade de chamadas por API e por endpoint, contemplando seu histórico;
II - da disponibilidade de APIs por endpoint, contemplando seu histórico;
III - do percentual de sucesso das chamadas, bem como de seus erros, por status code;
IV - da quantidade de consentimentos ativos total e por clientes únicos, pessoas natural e jurídica, incluindo visões por transmissor ou detentor (conforme o caso) e por receptor ou iniciador (conforme o caso), contemplando seu histórico; e
V - das taxas de conversão do consentimento com detalhamento de cada etapa de sua geração, incluindo visões por transmissor ou detentor e por receptor ou iniciador.
Os dados informados pelas instituições participantes são de responsabilidade de cada instituição, representada pelo diretor responsável pelo compartilhamento de dados e serviços no âmbito do Open Finance, e devem ser informados com frequência mínima que permita aferir o atendimento dos acordos de nível de serviço:
I - das APIs das instituições participantes; e
II - dos elementos da infraestrutura compartilhada.
A Estrutura de Governança do Open Finance, com base nos indicadores de nível de serviço apurados das instituições participantes, deve construir um índice de performance no Open Finance, calculá-lo de forma individual para cada instituição participante e divulgá-lo mensalmente.
Esses dados estatísticos devem ser também disponibilizados, em área pública do Portal do Open Finance no Brasil na forma de um painel de indicadores de fácil visualização, de forma individualizada e nominal em relação às instituições participantes, que permita a verificação desse desempenho pelo público em geral de maneira rápida e clara.
O painel de indicadores deve propiciar a visualização dos dados em, no mínimo, dois níveis diferentes:
I - visão consolidada: com as médias dos indicadores mais importantes, prevendo destaque para os melhores e piores desempenhos do mês; e
II - visão customizada/comparativa: com a possibilidade de ordenação por valor (crescente e decrescente), busca e seleção de múltiplos parâmetros pelo usuário, como nome da instituição participante, endpoint, período, entre outros.
Em ambas as visualizações, deve constar no painel de indicadores recurso visual, como gráficos, ícones ou símbolos, que permita aferir o desempenho do indicador em relação ao mínimo regulatório exigido. As visualizações devem permitir ao público geral identificar nominalmente o desempenho de cada uma das instituições participantes.
Dada a amplitude do escopo de participantes do Open Finance, eventuais gráficos que listem todas as instituições participantes devem dispor de ferramenta de busca que auxilie o usuário a localizar no gráfico uma instituição específica, caso desejado.
O painel de indicadores deve ainda conter recursos para pesquisa customizada, de forma a possibilitar a seleção de campos, inclusive de dados individualizados e não agregados. Os resultados devem ser passíveis de download para diferentes formatos, respeitando a seleção de campos ou segregação de dados realizada.
As métricas, as unidades de medida e as definições utilizadas devem ficar claras para o usuário, bem como eventuais limitações, exclusões ou alterações referentes à base de cálculo.
4.2 Divulgação de dados estatísticos e de indicadores sobre os itens monitorados
A Estrutura de Governança do Open Finance deve compilar os dados estatísticos sobre os itens monitorados, gerar indicadores e índices em relação a eles e divulgá-los, com vistas a dar transparência em relação ao processo de monitoramento e criar incentivos para que as instituições participantes busquem contínua evolução de sua atuação.
Tal divulgação deve contemplar os dados estatísticos, indicadores e índices de cada instituição participante, de forma individual e nominal, considerando seu histórico, bem como as eventuais situações de desconformidade, referentes a cada item monitorado e a outras situações de desconformidade identificadas que ainda não estejam no escopo dos itens monitorados.
Os dados estatísticos, indicadores e índices devem ser documentados para fins de controle interno da Estrutura de Governança do Open Finance e estar à disposição do Banco Central do Brasil.
5. Acompanhamento das situações de desconformidade
A Estrutura de Governança do Open Finance deve disponibilizar as seguintes informações para que as instituições participantes possam fazer a gestão das situações de desconformidade:
I - a listagem de todos os casos abertos e o histórico dos casos que já estão encerrados;
II - o status de cada caso aberto a depender da fase em que se encontra no fluxo de monitoramento e de aplicação de medidas; e
III - o detalhamento de cada caso, com informações específicas sobre a situação de desconformidade, a data de entrada do caso no fluxo de monitoramento e de aplicação de medidas e o prazo restante para sua resolução, conforme regulamentação do Banco Central do Brasil e documentação da Estrutura de Governança do Open Finance.
As informações de acompanhamento das situações de desconformidade mencionadas nesta seção devem estar acessíveis para o Banco Central do Brasil.
Brasília, 29 de janeiro de 2026.
NOTA 51/2026-BCB/DENOR, DE 27 de JANEIRO de 2026.
Fundamenta proposta de edição de instrução normativa que estabelece a versão 3.0 do Manual de Monitoramento do Open Finance.
Senhores Chefes do Denor, do Desuc, do Desup e do Deinf,
1. A presente Nota fundamenta proposta de edição de instrução normativa pelo Departamento de Regulação do Sistema Financeiro (Denor), pelo Departamento de Supervisão de Cooperativas e de Instituições Não Bancárias (Desuc), pelo Departamento de Supervisão Bancária (Desup) e pelo Departamento de Tecnologia da Informação (Deinf), no uso das atribuições que lhes confere o art. 23, inciso I, alínea "a", do Regimento Interno do Banco Central do Brasil, anexo à Resolução BCB nº 340, de 21 de setembro de 2023, com base no art. 3º, inciso VI, da Resolução BCB nº 32, de 29 de outubro de 2020.
2. A respeito, a proposta trata de edição de instrução normativa que estabelece a versão 3.0 do Manual de Monitoramento do Open Finance, revogando a Instrução Normativa BCB nº 575, de 20 de dezembro de 2024, que divulgou a versão 2.0 do Manual de Monitoramento do Open Finance.
3. A principal novidade dessa versão é uma mudança na fórmula de cálculo da taxa mínima de conversão, que passa a considerar apenas as instituições mais relevantes do Open Finance. Outras alterações realizadas nessa nova versão se referem às regras de reporte de informação à Plataforma de Coleta de Métricas, visando maior qualidade das informações reportadas; inclusão de análise de completude do relatório de situações de desconformidade; estabelecimento de regras para entrada em execução de planos de adequação; e alteração do prazo para apresentação de diagnóstico sobre taxa de conversão de dias corridos para dias úteis.
4. Convém ressaltar que, por força do art. 5º da Lei nº 13.874, de 20 de setembro de 2019, as propostas de edição e de alteração de atos normativos de interesse geral de agentes econômicos ou de usuários dos serviços prestados, editadas por órgão ou entidade da administração pública federal, incluídas as autarquias e as fundações públicas, devem ser precedidas da realização de análise de impacto regulatório (AIR), que conterá informações e dados sobre os possíveis efeitos do ato normativo para verificar a razoabilidade do seu impacto econômico.
5. Por sua vez, o Decreto nº 10.411, de 30 de junho de 2020, que regulamenta essa Lei, em seu art. 4º, inciso V, alíneas "b" e "c", estabelece que poderá ser dispensada a AIR, na hipótese de ato normativo que visa à preservação da higidez dos mercados financeiros e dos sistemas de pagamentos, aplicável a essas medidas, que buscam aumentar a qualidade de dados disponíveis para o Open Finance, e aprimorar o regramento relacionado ao monitoramento desse sistema.
6​. ​Dessa forma, considerando o exposto acima, entendemos que a instrução normativa ora proposta está dispensada de AIR.
À consideração de V.Sas.
JANAÍNA PIMENTA ATTIE IVENS ARUA NEVES DE MIRANDA
Consultora do Denor Chefe Adjunto do Desuc
RICARDO SIVIERI ZENI VERUSKA ROCHA ARAGÃO
Chefe Adjunto do Desup Chefe Adjunta do Deinf
De acordo.
MARDILSON FERNANDES QUEIROZ ADALBERTO FELINTO DA CRUZ JUNIOR
Chefe do Denor Chefe do Desuc
RICARDO SIVIERI ZENI CAIO MOREIRA FERNANDES
Chefe do Desup, substituto Chefe do Deinf
