### Passo a Passo
```markdown
### Passo 1: Instalar o Virtualenv

Se você ainda não tem o `virtualenv` instalado, instale-o usando o seguinte comando:

```bash
pip install virtualenv
```

### Passo 2: Criar um Ambiente Virtual

1. Navegue até o diretório onde você deseja criar o projeto:

   ```bash
   cd C:\Users\talit\OneDrive\Documentos\API_usuarios
   ```

2. Crie um novo diretório para o seu projeto (opcional):

   ```bash
   mkdir CRUD_API_Usuarios
   cd CRUD_API_Usuarios
   ```

3. Crie um ambiente virtual:

   ```bash
   virtualenv env
   ```

### Passo 3: Ativar o Ambiente Virtual

Ative o ambiente virtual que você acabou de criar:

- **No Windows**:

   ```bash
   env\Scripts\activate
   ```

- **No macOS/Linux**:

   ```bash
   source env/bin/activate
   ```

### Passo 4: Instalar o Django e Django REST Framework

Com o ambiente virtual ativado, instale o Django e o Django REST Framework:

```bash
pip install django djangorestframework djangorestframework-simplejwt
```

### Passo 5: Criar um Novo Projeto Django

1. Crie um novo projeto Django:

   ```bash
   django-admin startproject projeto
   ```

2. Navegue para o diretório do projeto:

   ```bash
   cd projeto
   ```

### Passo 6: Criar um Novo Aplicativo

1. Crie um novo aplicativo:

   ```bash
   python manage.py startapp projeto_APIusuarios
   ```

### Passo 7: Configurar o Projeto

1. Adicione o aplicativo e as dependências ao `settings.py`:

   Abra o arquivo `projeto/settings.py` e adicione `'rest_framework'`, `'rest_framework_simplejwt'` e `'projeto_APIusuarios'` à lista de `INSTALLED_APPS`:

   ```python
   INSTALLED_APPS = [
       ...
       'rest_framework',
       'rest_framework_simplejwt',
       'projeto_APIusuarios',
   ]
   ```

### Passo 8: Criar o Modelo de Usuário

No arquivo `projeto_APIusuarios/models.py`, crie o modelo de usuário:

```python
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    biography = models.TextField(blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    education = models.CharField(max_length=100, blank=True)
    pets_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username
```

### Passo 9: Criar o Serializer

No arquivo `projeto_APIusuarios/serializers.py`, crie o serializer para o modelo de usuário:

```python
from rest_framework import serializers
from .models import UserProfile
from django.contrib.auth.models import User

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'biography', 'age', 'phone', 'address', 'education', 'pets_count']
        read_only_fields = ['user']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
```

### Passo 10: Criar as Views

No arquivo `projeto_APIusuarios/views.py`, crie as views para o CRUD:

```python
from rest_framework import viewsets, permissions
from .models import UserProfile
from .serializers import UserProfileSerializer
from rest_framework.permissions import IsAuthenticated

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
```

### Passo 11: Configurar URLs

### Passo 11: Configurar URLs (continuação)

No arquivo `projeto_APIusuarios/urls.py`, configure as URLs para as views:

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet

router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

```
### Passo 12: Configurar as URLs do Projeto

```
Agora, você precisa incluir as URLs do aplicativo projeto_APIusuarios no arquivo de URLs principal do projeto. Abra o arquivo projeto/urls.py e adicione as seguintes linhas:

python

from django.contrib import admin

from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [

    path('admin/', admin.site.urls),

    path('api/', include('projeto_APIusuarios.urls')),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]

### Passo 13: Migrar o Banco de Dados

Agora que você configurou o modelo, as views e as URLs, é hora de criar as migrações e aplicar as alterações no banco de dados.

    Crie as migrações:

    bash

python manage.py makemigrations

Aplique as migrações:

bash

    python manage.py migrate
```

### Passo 14: Criar um Superusuário

```

Para acessar o painel de administração e criar usuários, você precisará de um superusuário. Execute o seguinte comando:

bash

python manage.py createsuperuser

Siga as instruções para criar um superusuário.
```
### Passo 15: Iniciar o Servidor

```

Agora você pode iniciar o servidor de desenvolvimento do Django:

bash

python manage.py runserver
```

### Passo 16: Testar a API

```

Acesse a API: Abra seu navegador ou uma ferramenta como Postman e acesse a URL:

http://127.0.0.1:8000/api/

Obter um token de autenticação: Para realizar operações de CRUD, você precisa de um token JWT. Para obtê-lo, faça uma requisição POST para a URL de autenticação:

POST http://127.0.0.1:8000/api/token/

Corpo da requisição (JSON):

json

{

    "username": "seu_usuario",

    "password": "sua_senha"

}

Se as credenciais estiverem corretas, você receberá uma resposta com o token:

json

{

    "refresh": "refresh_token",

    "access": "access_token"

}

Criar um novo perfil de usuário: Para criar um novo perfil, faça uma requisição POST para a URL:

POST http://127.0.0.1:8000/api/profiles/

Cabeçalhos:

Authorization: Bearer seu_token_de_acesso

Corpo da requisição (JSON):

json

{

    "biography": "Sou um amante de animais.",

    "age": 30,

    "phone": "123456789",

    "address": "Rua Exemplo, 123",

    "education": "Ensino Superior",

    "pets_count": 2

}

Listar perfis de usuários: Para listar todos os perfis de usuários, faça uma requisição GET para a URL:

GET http://127.0.0.1:8000/api/profiles/

Cabeçalhos:

Authorization: Bearer seu_token_de_acesso

Atualizar um perfil de usuário: Para atualizar um perfil existente, faça uma requisição PUT para a URL:

PUT http://127.0.0.1:8000/api/profiles/{id}/

Cabeçalhos:

Authorization: Bearer seu_token_de_acesso

Corpo da requisição (JSON):

json

{

    "biography": "Atualizei minha biografia.",

    "age": 31,

    "phone": "987654321",

    "address": "Rua Atualizada, 456",

    "education
    "education": "Mestrado",

   "pets_count": 3

   }

Excluir um perfil de usuário: Para excluir um perfil, faça uma requisição DELETE para a URL:

DELETE http://127.0.0.1:8000/api/profiles/{id}/

Cabeçalhos:

    Authorization: Bearer seu_token_de_acesso

```
### Passo 17: Encerrando o Ambiente Virtual
```
Quando você terminar de trabalhar no seu projeto, você pode desativar o ambiente virtual com o seguinte comando:

bash

deactivate

Considerações Finais

    Segurança: Certifique-se de que sua aplicação esteja segura, especialmente ao lidar com senhas e tokens. Use HTTPS em produção.
    Documentação: Considere usar ferramentas como Swagger ou Postman para documentar sua API.
    Testes: Implemente testes para garantir que sua API funcione conforme o esperado.

Conclusão

Você agora tem um projeto Django completo com uma API RESTful que permite criar, ler, atualizar e excluir perfis de usuários, com autenticação JWT. Se você tiver mais perguntas ou precisar de mais ajuda, fique à vontade para perguntar!

```
### Resumo do README

```


-O README acima fornece um guia completo para a criação de uma API CRUD de usuários usando Django e Django REST Framework. Ele inclui instruções sobre como configurar o ambiente, criar o projeto e o aplicativo, configurar modelos, serializers, views e URLs, além de testar a API e encerrar o ambiente virtual.


-Se precisar de mais alguma coisa ou de ajustes no README, é só avisar!