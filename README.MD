# Documentação Técnica do Projeto: Te Dedico

## 1. Introdução e Visão Geral

**"Te Dedico"** é uma aplicação web desenvolvida utilizando o framework Django, projetada para permitir que usuários registrados criem e compartilhem "presentes" digitais altamente personalizáveis. O sistema visa oferecer uma plataforma intuitiva para a criação de mensagens interativas que podem incluir texto, imagens, vídeos, música ambiente e esquemas de cores customizados.

**Principais Funcionalidades e Casos de Uso:**

* **Criação Personalizada de Presentes:** Usuários podem compor presentes digitais com título, mensagem, upload de imagens, incorporação de vídeos (via URL), adição de música de fundo (via URL) e seleção de cores para o fundo e elementos de destaque.
* **Autenticação de Usuários:** Sistema completo de registro, login e logout para proteger o acesso e associar os presentes aos seus respectivos autores.
* **Dashboard do Usuário:** Após o login, os usuários têm acesso a um painel pessoal onde podem visualizar todos os presentes que criaram, com informações resumidas e acesso rápido.
* **Visualização Única de Presentes:** Cada presente possui uma URL única e um QR Code correspondente (gerado automaticamente) para fácil compartilhamento e visualização. A página de visualização aplica as personalizações de mídia e aparência definidas pelo autor.
* **API RESTful:** Uma API (Application Programming Interface) construída com Django REST Framework expõe endpoints para gerenciamento programático dos presentes.
* **Interface Administrativa:** O Django Admin é customizado para permitir o gerenciamento facilitado dos dados da aplicação por administradores.

O projeto utiliza uma arquitetura Model-View-Template (MVT), padrão do Django, e adota Tailwind CSS para a estilização do frontend, garantindo uma interface moderna e responsiva.

## 2. Arquitetura da Aplicação

O projeto "Te Dedico" adere à arquitetura MVT (Model-View-Template) do Django:

* **Modelos (`models.py`):** Representam a camada de dados da aplicação. Definem a estrutura das informações armazenadas no banco de dados, suas relações e validações. No "Te Dedico", o principal modelo é `Presente`.
* **Views (`views.py`):** Constituem a camada de lógica de negócios. As views processam as requisições HTTP recebidas, interagem com os modelos para buscar ou manipular dados, e selecionam o template apropriado para renderizar a resposta ao cliente. Inclui views baseadas em funções e classes (ViewSets para a API).
* **Templates (`templates/`):** Formam a camada de apresentação. São arquivos HTML (com a linguagem de template do Django) que definem a estrutura e a interface do usuário.
* **URLs (`urls.py`):** O sistema de roteamento do Django mapeia as URLs das requisições HTTP para as views correspondentes.
* **Django REST Framework (DRF):** Utilizado para construir a API RESTful, facilitando a serialização de dados e a criação de endpoints.
* **Frontend:** A interface do usuário é renderizada no servidor através dos templates Django e estilizada com Tailwind CSS. JavaScript é utilizado para interatividade no lado do cliente, como a pré-visualização dinâmica na criação de presentes.

## 3. Tecnologias Utilizadas

* **Backend:**
    * Python (Linguagem de Programação Principal)
    * Django 5.2.1 (Framework Web)
    * Django REST Framework (Toolkit para construção de Web APIs)
* **Frontend:**
    * HTML5 (Linguagem de Marcação)
    * Tailwind CSS (Framework CSS, via CDN)
    * JavaScript (Linguagem de Scripting para interatividade no cliente)
    * FontAwesome (Biblioteca de Ícones, via CDN)
* **Banco de Dados:**
    * SQLite 3 (Sistema de Gerenciamento de Banco de Dados padrão para desenvolvimento)
* **Geração de QR Code:**
    * `qrcode` (Biblioteca Python para geração de QR Codes)
* **Manipulação de Imagens (Implícito):**
    * Pillow (Biblioteca Python para processamento de imagens, dependência do `ImageField` do Django)

## 4. Estrutura de Diretórios Detalhada

A organização dos diretórios e arquivos do projeto "Te Dedico" segue as convenções padrão do Django, facilitando a navegação e a manutenção do código. Abaixo está uma representação da estrutura principal:

tededico_project/      # Diretório raiz do projeto Django

├── tededico_project/  # Aplicação de configuração do projeto (core)

│   ├── __init__.py

│   ├── asgi.py        # Ponto de entrada para servidores ASGI (Asynchronous Server Gateway Interface)

│   ├── settings.py    # Arquivo de configurações globais do projeto Django

│   ├── urls.py        # Configuração principal de URLs do projeto

│   └── wsgi.py        # Ponto de entrada para servidores WSGI (Web Server Gateway Interface)

├── app/               # Aplicação Django principal do "Te Dedico"

│   ├── __init__.py

│   ├── admin.py       # Configurações para a interface administrativa do Django

│   ├── api_urls.py    # Definições de URL específicas para a API REST

│   ├── apps.py        # Configuração da aplicação "app"

│   ├── migrations/    # Arquivos de migração do banco de dados gerados pelo Django

│   │   ├── 0001_initial.py

│   │   ├── 0002_alter_presente_options_presente_autor_and_more.py

│   │   ├── 0003_presente_cor_destaque_presente_cor_fundo_and_more.py

│   │   └── __init__.py

│   ├── models.py      # Definição dos modelos de dados da aplicação

│   ├── serializers.py # Serializers para converter modelos em formatos como JSON para a API

│   ├── templates/     # Diretório contendo os arquivos de template HTML

│   │   ├── base.html  # Template base com estrutura comum e sidebar

│   │   ├── criar.html # Template para a página de criação de presentes

│   │   ├── login.html # Template para a página de login

│   │   ├── register.html# Template para a página de registro

│   │   ├── ver.html   # Template para visualização de um presente específico

│   │   └── dashboard/ # Subdiretório para templates relacionados ao dashboard

│   │       └── dashboard.html # Template do painel do usuário

│   ├── tests.py       # Arquivo para testes automatizados da aplicação

│   ├── urls.py        # Definições de URL específicas para a aplicação "app"

│   └── views.py       # Lógica de processamento de requisições e respostas (views)

├── media/             # Diretório onde os arquivos de mídia enviados pelos usuários (imagens, QR Codes)

│                      # são armazenados (configurado em settings.py)

└── manage.py          # Utilitário de linha de comando do Django para tarefas administrativas

A estrutura de diretórios do projeto é organizada da seguinte forma:


## 5. Configuração do Projeto (`tededico_project/settings.py`)

O arquivo `settings.py` contém todas as configurações do projeto Django. As configurações mais relevantes incluem:

* **`SECRET_KEY`**: Chave criptográfica única para a instalação Django. **Crucial para segurança, deve ser mantida em segredo em produção.**
* **`DEBUG`**: Booleano que ativa/desativa o modo de depuração. Definido como `True` em desenvolvimento para exibir informações detalhadas de erro. **Deve ser `False` em produção.**
* **`ALLOWED_HOSTS`**: Lista de strings representando os nomes de host/domínio que esta aplicação Django pode servir. **Deve ser configurada explicitamente em produção.**
* **`INSTALLED_APPS`**: Enumera todas as aplicações Django que estão ativas neste projeto. Inclui apps padrão do Django, a aplicação `app` do projeto e `rest_framework`.
* **`MIDDLEWARE`**: Define a lista de middlewares utilizados pelo Django para processar requisições e respostas globalmente.
* **`ROOT_URLCONF`**: Especifica o módulo Python onde as configurações de URL raiz do projeto estão definidas (`'tededico_project.urls'`).
* **`TEMPLATES`**: Configura o sistema de templates do Django, incluindo backends, diretórios e processadores de contexto.
* **`DATABASES`**: Dicionário de configuração para os bancos de dados. Atualmente configurado para usar SQLite.
* **Autenticação e Autorização:**
    * `AUTH_PASSWORD_VALIDATORS`: Define validadores para fortalecer as senhas dos usuários.
    * `LOGIN_URL = '/login/'`: URL para redirecionamento de usuários não autenticados que tentam acessar recursos protegidos.
    * `LOGIN_REDIRECT_URL = '/'`: URL para redirecionamento após um login bem-sucedido.
    * `LOGOUT_REDIRECT_URL = '/login/'`: URL para redirecionamento após um logout bem-sucedido.
* **Internacionalização (i18n) e Localização (l10n):**
    * `LANGUAGE_CODE = 'en-us'`
    * `TIME_ZONE = 'UTC'`
    * `USE_I18N = True`, `USE_TZ = True`
* **Arquivos Estáticos e de Mídia:**
    * `SITE_URL_BASE = 'http://127.0.0.1:8000'`: URL base utilizada para gerar URLs absolutas, como na criação de QR Codes.
    * `STATIC_URL = 'static/'`: URL prefixo para arquivos estáticos (CSS, JavaScript, imagens do tema).
    * `MEDIA_URL = '/media/'`: URL prefixo para arquivos de mídia enviados pelos usuários.
    * `MEDIA_ROOT = BASE_DIR / 'media'`: Caminho absoluto no sistema de arquivos onde os arquivos de mídia são armazenados.
* **Outras Configurações:**
    * `DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'`: Define o tipo de campo padrão para chaves primárias automáticas.

## 6. Componentes Detalhados da Aplicação `app`

### 6.1. Modelos (`app/models.py`)

O principal modelo da aplicação é `Presente`.

**`Presente(models.Model)`**

Define a estrutura de um "presente digital".

* **Campos:**
    * `autor`: `ForeignKey(User, on_delete=models.CASCADE, related_name="presentes", verbose_name="Autor")` - Referência ao usuário criador. A exclusão de um usuário acarreta na exclusão de seus presentes.
    * `titulo`: `CharField(max_length=255, verbose_name="Título")` - Título textual do presente.
    * `mensagem`: `TextField(verbose_name="Mensagem")` - Conteúdo principal da mensagem do presente.
    * `imagem`: `ImageField(upload_to='imagens/', blank=True, null=True, verbose_name="Imagem")` - Campo opcional para upload de uma imagem, armazenada no subdiretório `imagens/` dentro de `MEDIA_ROOT`.
    * `video_url`: `URLField(blank=True, null=True, verbose_name="URL do Vídeo")` - Campo opcional para a URL de um vídeo externo.
    * `criado_em`: `DateTimeField(auto_now_add=True, verbose_name="Criado em")` - Registra automaticamente a data e hora da criação do objeto.
    * `qr_code`: `ImageField(upload_to='qrcodes/', blank=True, null=True, verbose_name="QR Code")` - Campo opcional para armazenar a imagem do QR Code gerado, salvo em `qrcodes/`.
    * `cor_fundo`: `CharField(max_length=7, blank=True, null=True, verbose_name="Cor de Fundo", help_text="Ex: #FFFFFF...")` - Código hexadecimal opcional para a cor de fundo.
    * `cor_destaque`: `CharField(max_length=7, blank=True, null=True, verbose_name="Cor de Destaque", help_text="Ex: #FF69B4...")` - Código hexadecimal opcional para a cor de destaque.
    * `musica_url`: `URLField(blank=True, null=True, verbose_name="URL da Música de Fundo", help_text="Link direto...")` - URL opcional para uma trilha sonora.

* **Métodos:**
    * `__str__(self)`: Retorna `self.titulo` para representação textual do objeto.
    * `get_absolute_url(self)`: Retorna a URL canônica para visualizar o objeto `Presente` específico, utilizando `reverse('ver_presente', kwargs={'id': self.id})`.
    * `save(self, *args, **kwargs)`: Sobrescrito para realizar duas ações principais antes de salvar:
        1.  **Validação de Cores:** Verifica se `cor_fundo` e `cor_destaque` iniciam com `#`. Caso contrário, define-os como `None` (validação básica).
        2.  **Geração de QR Code:** Se o objeto é novo (`is_new`) ou não possui um `qr_code` associado, um QR Code é gerado a partir da URL absoluta do presente (obtida via `get_absolute_url()` e `settings.SITE_URL_BASE`). A imagem do QR Code é salva em um `BytesIO buffer` e, em seguida, no campo `qr_code` do modelo. O método lida com `update_fields` para otimizar o salvamento quando apenas o QR Code precisa ser atualizado.

* **Classe `Meta`:**
    * `verbose_name = "Presente"` e `verbose_name_plural = "Presentes"`: Nomes amigáveis para o modelo no Django Admin.
    * `ordering = ['-criado_em']`: Define a ordem padrão de consulta para os objetos `Presente` como decrescente pela data de criação.

### 6.2. Views (`app/views.py`)

As views são responsáveis por processar requisições e retornar respostas.

* **`PresenteViewSet(viewsets.ModelViewSet)`**:
    * Endpoint da API REST para o modelo `Presente`.
    * Fornece automaticamente as ações `list`, `create`, `retrieve`, `update`, `partial_update`, e `destroy`.
    * `queryset = Presente.objects.all()`: Define o conjunto de dados base.
    * `serializer_class = PresenteSerializer`: Especifica o serializer a ser usado.
* **`criar_presente(request)`**:
    * Decorador: `@login_required` - Acesso restrito a usuários autenticados.
    * Método `GET`: Renderiza o template `criar.html` para exibição do formulário de criação.
    * Método `POST`: Coleta os dados do formulário (`request.POST`, `request.FILES`). Valida (de forma simples) os campos de cor. Cria uma nova instância de `Presente`, associando o `request.user` ao campo `autor`. Salva o objeto e redireciona para `ver_presente` com o ID do novo presente.
* **`ver_presente(request, id)`**:
    * Recupera uma instância de `Presente` pelo `id` fornecido na URL usando `get_object_or_404`.
    * Renderiza o template `ver.html`, passando o objeto `presente` para o contexto.
* **`login_view(request)`**:
    * Método `GET`: Renderiza `login.html`.
    * Método `POST`: Extrai `username` e `password`. Autentica o usuário com `authenticate()`. Se válido, realiza o login com `login(request, user)` e redireciona para `LOGIN_REDIRECT_URL` (`'/'`). Caso contrário, renderiza `login.html` com uma mensagem de erro.
* **`logout_view(request)`**:
    * Realiza o logout do usuário (`logout(request)`) e redireciona para `LOGOUT_REDIRECT_URL` (`'/login/'`).
* **`register_view(request)`**:
    * Método `GET`: Renderiza `register.html`.
    * Método `POST`: Extrai `username` e `password`. Verifica se o usuário já existe. Se não, cria o usuário com `User.objects.create_user()`, faz o login e redireciona para `'/'`. Caso contrário, renderiza `register.html` com uma mensagem de erro.
* **`dashboard_view(request)`**:
    * Decorador: `@login_required`.
    * Busca os presentes (`Presente.objects.filter(autor=request.user).order_by('-criado_em')`) do usuário logado.
    * Implementa paginação usando `django.core.paginator.Paginator` (5 itens por página).
    * Renderiza `dashboard/dashboard.html` com a página atual de presentes (`page_obj`) e o total de presentes.

### 6.3. URLs (`app/urls.py` e `app/api_urls.py`)

* **`tededico_project/urls.py`**:
    * `admin/`: Inclui as URLs do Django Admin.
    * `api/`: Delega para `app.api_urls` para todas as rotas da API.
    * `''`: Delega para `app.urls` para as rotas da aplicação principal.
    * Adiciona o padrão `static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)` para servir arquivos de mídia em desenvolvimento.
* **`app/urls.py`**:
    * Define as rotas para as views baseadas em função:
        * `''` (raiz) -> `dashboard_view` (nome: `dashboard`)
        * `criar/` -> `criar_presente` (nome: `criar_presente`)
        * `presente/<int:id>/` -> `ver_presente` (nome: `ver_presente`)
        * `login/` -> `login_view` (nome: `login`)
        * `logout/` -> `logout_view` (nome: `logout`)
        * `register/` -> `register_view` (nome: `register`)
* **`app/api_urls.py`**:
    * Utiliza `DefaultRouter` do DRF para registrar automaticamente as rotas para o `PresenteViewSet` sob o prefixo `presentes`.
    * Isso gera URLs como `/api/presentes/` (para `GET` listar e `POST` criar) e `/api/presentes/<id>/` (para `GET` detalhe, `PUT`/`PATCH` atualizar, `DELETE` excluir).

### 6.4. Templates

Os templates definem a interface do usuário. Todos herdam de `base.html`.

* **`base.html`**:
    * Estrutura principal da página, incluindo `<head>` (com CDN do Tailwind CSS e FontAwesome) e `<body>`.
    * Define variáveis CSS (`--casal-bg`, `--casal-accent`) para o tema.
    * Implementa uma **sidebar de navegação lateral** para usuários autenticados, com links para Dashboard, Criar Novo e Logout. A sidebar é responsiva e controlada por JavaScript.
    * Contém um **header mobile** com o logo e um botão "hamburger" para exibir/ocultar a sidebar em telas menores.
    * Utiliza blocos de template Django (`{% block title %}`, `{% block head_extra %}`, `{% block body_class %}`, `{% block content %}`) para permitir que templates filhos substituam ou adicionem conteúdo.
    * Inclui um footer padrão.
* **`dashboard/dashboard.html`**:
    * Exibe a lista de presentes criados pelo usuário logado.
    * Apresenta cada presente em um card com imagem, título, data e um trecho da mensagem.
    * Oferece links para "Ver Detalhes" e "Ver QR Code" de cada presente.
    * Implementa navegação por paginação se o número de presentes exceder o limite por página.
    * Mostra uma mensagem de incentivo para criar um presente se a lista estiver vazia.
* **`criar.html`**:
    * Contém o formulário para criação de novos presentes. Campos incluem: título, mensagem, upload de imagem, URL de vídeo, URL de música e seletores de cor de fundo/destaque.
    * Apresenta uma seção de "Sugestões de Temas" de cores que, ao serem clicadas, preenchem os campos de cor.
    * Implementa uma **pré-visualização dinâmica** em uma coluna adjacente. Esta pré-visualização é atualizada em tempo real via JavaScript à medida que o usuário preenche os campos do formulário, refletindo título, mensagem, imagem, vídeo, música e as cores selecionadas.
* **`ver.html`**:
    * Página de visualização de um presente individual.
    * Renderiza o título, mensagem, imagem, vídeo (incorporado) e áudio (com controles) do presente.
    * Aplica dinamicamente as cores de fundo e destaque personalizadas, se definidas no modelo `Presente`, sobrescrevendo os padrões do `base.html` através de variáveis CSS injetadas no bloco `head_extra`.
* **`login.html`** e **`register.html`**:
    * Templates simples para os formulários de autenticação e registro, respectivamente.
    * Exibem mensagens de erro, se aplicável.

### 6.5. Serializers (`app/serializers.py`)

* **`PresenteSerializer(serializers.ModelSerializer)`**:
    * Converte instâncias do modelo `Presente` para formatos de dados como JSON (para respostas da API) e vice-versa (para processar dados de requisições da API).
    * `class Meta`:
        * `model = Presente`: Especifica o modelo a ser serializado.
        * `fields = '__all__'`: Indica que todos os campos do modelo `Presente` devem ser incluídos na representação serializada.

### 6.6. Admin (`app/admin.py`)

A configuração do Django Admin para o modelo `Presente` é customizada para melhorar a usabilidade.

* **`@admin.register(Presente)`**: Registra o modelo `Presente` com a classe de administração customizada `PresenteAdmin`.
* **`PresenteAdmin(admin.ModelAdmin)`**:
    * `list_display`: Define as colunas exibidas na visualização em lista de presentes no admin (`titulo`, `autor`, `criado_em`, `imagem_preview`, `video_url`).
    * `list_filter`: Adiciona filtros laterais para `autor` e `criado_em`.
    * `search_fields`: Habilita a busca por `titulo`, `mensagem` e `autor__username`.
    * `readonly_fields`: Torna os campos `qr_code_preview` e `criado_em` somente leitura nos formulários de edição/criação do admin.
    * `fieldsets`: Organiza os campos do formulário em seções lógicas (Informações Principais, Mídia, QR Code).
    * `imagem_preview(self, obj)`: Método customizado para exibir uma miniatura da imagem do presente na `list_display` e no formulário.
    * `qr_code_preview(self, obj)`: Método customizado para exibir a imagem do QR Code no formulário.

### 6.7. Lógica Frontend (JavaScript em `criar.html`)

O template `criar.html` contém um script JavaScript significativo para a funcionalidade de pré-visualização dinâmica.

* **Atualização em Tempo Real:**
    * Listeners de eventos (`input`, `change`) são anexados aos campos do formulário (título, mensagem, upload de imagem, URL do vídeo, URL da música, seletores de cor).
    * Quando um valor é alterado, a função `updatePreview()` é chamada.
* **`updatePreview(themeTextColor = null)`:**
    * Atualiza o conteúdo textual da pré-visualização (título, mensagem).
    * Lê os valores dos seletores de cor ou dos campos de texto hexadecimais e aplica as cores de fundo e destaque ao container da pré-visualização e aos elementos de texto relevantes.
    * Se uma imagem é selecionada, usa `FileReader` para lê-la como Data URL e exibi-la na pré-visualização.
    * Processa a URL do vídeo:
        * Chama `getEmbedUrl()` para converter URLs de visualização do YouTube/Vimeo em URLs de incorporação (embed).
        * Atualiza o `src` do `<iframe>` de vídeo na pré-visualização.
    * Atualiza o `src` do elemento `<audio>` para a URL da música e tenta carregar o áudio.
    * Aplica a cor de texto `themeTextColor` à mensagem se um tema específico for aplicado.
* **`getEmbedUrl(videoUrl)`:**
    * Converte URLs de vídeo do YouTube (`watch?v=` para `embed/`) e Vimeo (`vimeo.com/ID` para `player.vimeo.com/video/ID`) para formatos adequados para incorporação em `<iframe>`.
* **Sugestões de Tema:**
    * `predefinedThemes`: Array de objetos JavaScript definindo temas (nome, cor de fundo, cor de destaque, cor do texto).
    * `displayThemeSuggestions()`: Cria dinamicamente pequenas "amostras" de temas clicáveis.
    * `applyTheme(theme)`: Ao clicar em uma sugestão de tema, esta função atualiza os valores dos campos de cor do formulário e chama `updatePreview()` para refletir o tema selecionado.

## 7. API REST (Interface `app/api_urls.py`)

A aplicação expõe uma API RESTful para o recurso "Presente" através do Django REST Framework.

* **Endpoint Base:** `/api/presentes/`
* **Serializers Utilizados:** `PresenteSerializer`
* **Operações Suportadas (via `PresenteViewSet`):**
    * **`GET /api/presentes/`**: Lista todos os presentes.
    * **`POST /api/presentes/`**: Cria um novo presente.
        * Corpo da requisição: JSON com os dados do presente.
    * **`GET /api/presentes/<id>/`**: Recupera os detalhes de um presente específico.
    * **`PUT /api/presentes/<id>/`**: Atualiza completamente um presente existente.
        * Corpo da requisição: JSON com todos os dados do presente.
    * **`PATCH /api/presentes/<id>/`**: Atualiza parcialmente um presente existente.
        * Corpo da requisição: JSON com os campos a serem atualizados.
    * **`DELETE /api/presentes/<id>/`**: Exclui um presente existente.

    *Autenticação e permissões para a API não estão explicitamente detalhadas no `PresenteViewSet`, assumindo-se as configurações padrão do DRF (geralmente, acesso não autenticado para leitura e autenticado para escrita, a menos que configurado de outra forma).*

## 8. Configuração do Ambiente de Desenvolvimento e Execução

1.  **Pré-requisitos:**
    * Python 3.x
    * pip (Gerenciador de pacotes Python)
    * Git (Opcional, para controle de versão)
2.  **Clonagem do Repositório (se aplicável):**
    ```bash
    git clone <url_do_repositorio>
    cd tededico_project
    ```
3.  **Criação e Ativação do Ambiente Virtual:**
    É altamente recomendável usar um ambiente virtual para isolar as dependências do projeto.
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```
4.  **Instalação das Dependências:**
    Crie um arquivo `requirements.txt` com o seguinte conteúdo:
    ```
    Django==5.2.1
    djangorestframework
    qrcode
    Pillow
    ```
    Então, instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
5.  **Configuração Inicial do Banco de Dados:**
    Aplique as migrações para criar as tabelas no banco de dados (SQLite por padrão).
    ```bash
    python manage.py migrate
    ```
6.  **Criação de um Superusuário:**
    Para acessar a interface administrativa do Django (`/admin/`).
    ```bash
    python manage.py createsuperuser
    ```
    Siga as instruções para definir nome de usuário, email (opcional)和 senha.
7.  **Execução do Servidor de Desenvolvimento:**
    ```bash
    python manage.py runserver
    ```
    A aplicação estará acessível em `http://127.0.0.1:8000/` por padrão.
    A interface administrativa estará em `http://127.0.0.1:8000/admin/`.

## 9. Instruções de Deploy (Considerações Gerais)

Para implantar esta aplicação em um ambiente de produção, as seguintes etapas e considerações são tipicamente necessárias (esta não é uma lista exaustiva):

* **Servidor WSGI/ASGI:**
    * Utilizar um servidor de aplicação Python como Gunicorn (para WSGI) ou Daphne/Uvicorn (para ASGI) em vez do servidor de desenvolvimento do Django.
* **Servidor Web (Reverse Proxy):**
    * Configurar um servidor web como Nginx ou Apache na frente do servidor de aplicação para servir arquivos estáticos, gerenciar conexões HTTPS e atuar como um reverse proxy.
* **Configurações de Produção (`settings.py`):**
    * `DEBUG = False`
    * `SECRET_KEY` deve ser uma chave forte e carregada de uma variável de ambiente ou arquivo secreto, não hardcoded.
    * `ALLOWED_HOSTS` deve ser configurado com o(s) domínio(s) da aplicação.
    * Usar um banco de dados mais robusto (PostgreSQL, MySQL) em vez de SQLite.
* **Arquivos Estáticos:**
    * Executar `python manage.py collectstatic` para reunir todos os arquivos estáticos em um único diretório (`STATIC_ROOT`) que será servido pelo Nginx/Apache.
* **Arquivos de Mídia:**
    * Garantir que o `MEDIA_ROOT` seja um local persistente e que o servidor web tenha permissão para servir arquivos de `MEDIA_URL`.
* **Segurança:**
    * Configurar HTTPS.
    * Revisar e aplicar outras configurações de segurança do Django (CSRF, XSS, Clickjacking).
* **Variáveis de Ambiente:**
    * Gerenciar configurações sensíveis (chaves de API, credenciais de banco de dados, `SECRET_KEY`) através de variáveis de ambiente.

## 10. Roadmap e Melhorias Futuras

Esta seção descreve potenciais melhorias e funcionalidades futuras para o projeto:

* **Testes Automatizados:**
    * Desenvolver uma suíte de testes unitários e de integração robusta para os modelos, views e APIs, utilizando o framework de testes do Django (`app/tests.py` atualmente está vazio).
* **Validação de Formulários Aprimorada:**
    * Implementar Django Forms ou ModelForms para uma validação de dados mais completa e segura no backend (views `criar_presente`, `register_view`, `login_view`), em vez de manipulação direta de `request.POST`.
* **Funcionalidades de Usuário:**
    * **Edição e Exclusão de Presentes:** Permitir que usuários autenticados editem ou excluam seus próprios presentes a partir do dashboard.
    * **Pré-visualização de Presentes no Dashboard:** Adicionar uma opção de pré-visualização rápida diretamente no dashboard.
    * **Compartilhamento Social:** Integrar botões de compartilhamento para redes sociais nas páginas de visualização de presentes.
* **Melhorias na API:**
    * **Autenticação e Permissões:** Implementar um sistema de autenticação mais granular para a API (ex: TokenAuthentication, OAuth2) e definir permissões de acesso aos endpoints.
    * **Documentação da API:** Gerar documentação interativa da API usando ferramentas como Swagger/OpenAPI (ex: `drf-yasg` ou `drf-spectacular`).
    * **Versionamento da API:** Introduzir versionamento para futuras atualizações da API.
* **UX/UI:**
    * **Internacionalização (i18n) e Localização (l10n):** Adaptar a aplicação para múltiplos idiomas e formatos regionais.
    * **Acessibilidade (a11y):** Realizar auditorias e melhorias para garantir a conformidade com as diretrizes de acessibilidade web.
    * **Feedback ao Usuário:** Melhorar o feedback visual para ações como uploads de arquivos, salvamento de formulários e erros.
* **Performance e Otimização:**
    * **Otimização de Imagens:** Implementar otimização de imagens no upload (compressão, redimensionamento) para reduzir o tempo de carregamento e o uso de armazenamento.
    * **Caching:** Aplicar estratégias de caching para otimizar o desempenho de consultas frequentes e renderização de páginas.
* **Segurança Avançada:**
    * Implementar Two-Factor Authentication (2FA).
    * Realizar auditorias de segurança regulares.