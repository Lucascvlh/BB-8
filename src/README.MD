# Automação de Cadastro de Processos
Este script em Python utiliza a biblioteca Selenium para automatizar o processo de cadastro de processos em um sistema web. O objetivo é simplificar e agilizar o cadastro de processos em um sistema de gerenciamento.

## Requisitos
Para utilizar este script, você precisará das seguintes dependências:

Python: A linguagem de programação usada para escrever o script.
Selenium: Uma biblioteca para automação de navegadores da web.
python-dotenv: Uma biblioteca para carregar variáveis de ambiente a partir de um arquivo .env.
pyautogui: Uma biblioteca para automação de tarefas do sistema operacional.
ChromeDriver: O driver para o navegador Google Chrome.
Você também precisa configurar um arquivo .env com as seguintes variáveis de ambiente:

- **URL_BL**: A URL do sistema de gerenciamento BrainLaw.
- **LOGIN_BL**: Seu nome de usuário para o BrainLaw.
- **PASSWORD_BL**: Sua senha para o BrainLaw.
- **URL_BL_PESQUISA**: A URL específica para a pesquisa de processos no BrainLaw.
- **URL_PAINEL_CSC**: A URL do painel de cadastro no BrainLaw.
- **URL_PROJUDI**: A URL do sistema Projudi.
- **LOGIN_PROJUDI**: Seu nome de usuário para o Projudi.
- **PASSWORD_PROJUDI**: Sua senha para o Projudi.
- **URL_CITACOES_PROJUDI**: A URL específica para a página de citações no Projudi.
- **COUNT_DOWN**: O número de vezes que você deseja pressionar a tecla "down" (setas para baixo) durante o processo.
Uso
Para utilizar este script, siga estas etapas:

Instale todas as dependências necessárias, como o Selenium e o pyautogui, executando:

```pip install -r requirements.txt```.

**Configure o arquivo .env com as variáveis de ambiente necessárias.**

Execute o script Python, que automatizará o processo de cadastro de processos conforme descrito no código.

O script abrirá um navegador Chrome e automatizará as ações necessárias para o cadastro de processos no BrainLaw e Projudi.

O script também registrará as ações realizadas em um arquivo de log.

Ao final, o script exibirá um resumo do processo, incluindo o número de processos cadastrados e a porcentagem de aproveitamento.

Lembre-se de que este script é específico para um ambiente e sistema. Você pode precisar ajustá-lo para atender às necessidades do seu ambiente e sistema específicos.

### Nota: Este script é fornecido apenas como exemplo e pode ser necessário adaptá-lo para atender aos requisitos específicos do seu sistema e ambiente.
