# Laboratório 2

## Atividade 1
1. O estilo escolhido foi o de camadas, pois dessa forma seria possível concentrar todo acesso aos dados em um único componente, tendo um controle maior de leitura e escrita.
2. Os componentes são:
  * dictionary.py: Componente de acesso ao dicionário. Contém um dicionário, suas funções de acesso e de leitura e escrita em arquivo.
  * application.py: Componente de aplicação para comunicação com o dicionário. Esse componente é responsável por receber requisições e determinar qual ação deve ser tomada. Além disso, contém a função de deletar, somente disponível para administradores que possam acessar esse componente.
  * client_side.py: Componente de interaface para usuários do sistema. Lê uma ação do teclado e comunica a aplicação em caso de ação válida, para que a mesma possa retornar o que for pedido.

O client_side se comunica com application via sockets, enquanto application se comunica com dictionary através de um objeto simples.

## Atividade 2
1. No lado cliente ficará a interface de cada usuário, de responsabilidade de client_side.py
2. No lado servido ficará a interface do administrador, de responsabilidade de application.py. Os componentes de dicionário e requisições também estarão no servidor, mantendo assim uma cópia segura dos arquivos necessários.
3. O lado cliente pode mandar as mensagens: "GET\n[chave]" e "ADD\n[chave]\n[valor]". As respectivas respostas são: "[valor]" e "ADD-NEW"/"ADD-OLD" (A depender se a chave é nova ou não). O cliente que deverá mandar a mensagem e esperar uma resposta do servidor, não havendo nenhuma mensagem por fonte do servidor. Ao receber uma mensagem o servidor faz a ação respectiva, de acessar o valor da chave ou adicionar uma nova entrada ao dicionário.

## Atividade 3
O código se encontra no repositório. Algumas decisões tomadas foram:
* A interface do administrador faz parte do código que cuida das requisições pois dessa forma a verificação fica mais simples, não sendo necessário realizar um sistema de login pelos clientes.
* Foi decidida a concorrência através de threads ao contrário de multiprocessos pois a memória do segundo não é compartilhada. Para implementar seria então necessário criar uma interface de comunicação entre os processos, o que complicaria a aplicação mais do que o objetivo do trabalho.
* Os componentes de uma mensagem são separados com quebra de linha pois qualquer outro caractere poderia fazer parte de um idioma. Dessa forma é mais garantido que em uma aplicação com linguagens existentes é um dicionário válido. A opção de enviar mais de um pacote para cada componente da mensagem foi avaliada, mas não seguiu em frente.
* Da mesma forma, também não há mais de um pacote enviado em caso de mensagens que excedam o limite de caracteres do socket, mantendo a aplicação com um limite físico de tamanho máximo das palavras.
* A leitura também é bloqueada por lock pois em caso de concorrência foi priorizado a consistência do conteúdo, para não receber uma mensagem possível de estar desatualizada.
