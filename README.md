# 🚗 Sistema de Rotas por Ruas — Botucatu

Sistema web desenvolvido em **Python + Flask + Leaflet + OpenStreetMap + OSRM** para calcular e visualizar rotas entre dois pontos diretamente no mapa.

O usuário pode clicar em **qualquer local do mapa** para definir a origem e depois clicar em outro local para definir o destino. O sistema então consulta o serviço de roteamento e desenha a rota seguindo as **ruas reais**, em vez de traçar uma linha reta entre os pontos.

---

## ✨ Funcionalidades

* 🗺️ Mapa interativo com Leaflet
* 📍 Origem definida livremente pelo usuário
* 📍 Destino definido livremente pelo usuário
* 🚗 Rota seguindo as ruas reais
* 📏 Cálculo da distância da rota
* ⏱️ Estimativa do tempo de deslocamento
* 🟢 Marcador para origem
* 🔴 Marcador para destino
* 🔵 Visualização da rota no mapa
* 🧹 Botão para limpar os pontos e iniciar uma nova rota
* 📱 Interface compatível com diferentes tamanhos de tela
* 🌎 Dados cartográficos baseados no OpenStreetMap

---

## 🛠️ Tecnologias utilizadas

### Backend

* Python
* Flask
* Requests

### Frontend

* HTML5
* CSS3
* JavaScript
* Leaflet.js

### Mapas

* OpenStreetMap

### Roteamento

* OSRM — Open Source Routing Machine

---

## 📋 Requisitos

Antes de executar o projeto, é necessário ter instalado:

* Python 3.10 ou superior
* pip
* Conexão com a internet

O projeto utiliza o serviço OSRM para calcular as rotas, portanto uma conexão com a internet é necessária durante o uso.

---

## 📥 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git
```

Entre na pasta:

```bash
cd SEU-REPOSITORIO
```

---

### 2. Crie um ambiente virtual

Windows:

```powershell
py -m venv venv
```

Linux/macOS:

```bash
python3 -m venv venv
```

---

### 3. Ative o ambiente virtual

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Windows CMD:

```cmd
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

---

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

---

## ▶️ Executando o projeto

Execute:

```bash
python app.py
```

No Windows também pode ser utilizado:

```powershell
py app.py
```

O Flask iniciará o servidor local.

Acesse no navegador:

```text
http://127.0.0.1:5000
```

---

## 🗺️ Como utilizar

### 1. Defina a origem

Clique em qualquer ponto do mapa.

O sistema criará um marcador:

🟢 **Origem**

---

### 2. Defina o destino

Clique em outro ponto do mapa.

O sistema criará:

🔴 **Destino**

---

### 3. Aguarde o cálculo

O sistema enviará as coordenadas para o OSRM.

O serviço encontrará uma rota utilizando a rede de ruas disponível no OpenStreetMap.

---

### 4. Visualize a rota

A rota será desenhada em azul sobre as ruas:

```text
🟢 Origem
    │
    ├──── Rua
    │
    ├──────── Avenida
    │
    └──── Rua
             │
             ▼
        🔴 Destino
```

Também serão exibidos:

* distância da rota;
* tempo estimado de deslocamento.

---

## 🔄 Fluxo do sistema

```text
                 USUÁRIO
                    │
                    ▼
             Clica no mapa
                    │
                    ▼
              Define origem
                    │
                    ▼
             Clica novamente
                    │
                    ▼
              Define destino
                    │
                    ▼
             Flask / Python
                    │
                    ▼
                  OSRM
                    │
                    ▼
        Rede de ruas do mapa
                    │
                    ▼
            Calcula a rota
                    │
                    ▼
          Retorna coordenadas
                    │
                    ▼
                Leaflet
                    │
                    ▼
          🚗 Rota desenhada
```

---

## 📁 Estrutura do projeto

```text
.
├── app.py
├── requirements.txt
└── README.md
```

---

## 🔌 API utilizada

O projeto utiliza o serviço público do **OSRM** para cálculo das rotas.

Endpoint utilizado:

```text
https://router.project-osrm.org/route/v1/driving/
```

As coordenadas são enviadas no formato:

```text
longitude,latitude
```

A geometria retornada pelo OSRM é convertida para o formato utilizado pelo Leaflet:

```text
latitude,longitude
```

---

## 🗺️ OpenStreetMap

Os dados cartográficos exibidos no mapa são fornecidos pelo OpenStreetMap.

O projeto utiliza os tiles:

```text
https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png
```

---

## ⚠️ Limitações

Este projeto utiliza uma infraestrutura pública para demonstração e desenvolvimento.

Para uso em produção com grande quantidade de usuários ou requisições, recomenda-se utilizar:

* servidor próprio de OSRM;
* GraphHopper;
* Valhalla;
* outro provedor de roteamento com API;
* infraestrutura própria de mapas e roteamento.

O servidor público do OSRM não deve ser considerado uma infraestrutura garantida para aplicações comerciais de grande escala.

---

## 🚀 Possíveis melhorias

Algumas funcionalidades que podem ser adicionadas futuramente:

* [ ] Pesquisa de endereço
* [ ] Geocodificação de endereços
* [ ] Botão "Minha localização"
* [ ] Rotas para carros
* [ ] Rotas para motos
* [ ] Rotas para bicicletas
* [ ] Rotas para pedestres
* [ ] Múltiplos destinos
* [ ] Adicionar vários pontos
* [ ] Otimização de múltiplas paradas
* [ ] Histórico de rotas
* [ ] Login de usuários
* [ ] Banco de dados
* [ ] API própria de roteamento
* [ ] Cálculo de distância total entre várias vistorias
* [ ] Integração com sistema de distribuição de vistorias
* [ ] Otimização de rotas para técnicos
* [ ] Dashboard de acompanhamento
* [ ] Exportação de rotas

---

## 🔐 Segurança

Para ambiente de produção, recomenda-se:

* utilizar HTTPS;
* configurar corretamente o servidor Flask;
* utilizar um servidor WSGI;
* limitar requisições à API de roteamento;
* implementar tratamento de erros;
* utilizar variáveis de ambiente para configurações;
* adicionar autenticação caso o sistema seja disponibilizado publicamente.

---

## 📄 Licença

Este projeto pode ser utilizado e modificado conforme a licença definida pelo proprietário do repositório.

Os dados cartográficos utilizados pelo projeto são provenientes do OpenStreetMap e estão sujeitos aos termos de uso e atribuição correspondentes.

---

## 👨‍💻 Desenvolvimento

Projeto desenvolvido para estudos e aplicações de:

* desenvolvimento web;
* algoritmos de roteamento;
* mapas digitais;
* geolocalização;
* APIs;
* Python;
* Flask;
* OpenStreetMap;
* OSRM.

---

## ⭐ Contribuições

Sugestões, melhorias e contribuições são bem-vindas.

Para contribuir:

```bash
git fork
```

Crie uma branch:

```bash
git checkout -b minha-melhoria
```

Faça suas alterações e depois envie um Pull Request.

---

## 📌 Status

🟢 **Em desenvolvimento**

A versão atual permite selecionar dois pontos livremente no mapa e calcular uma rota pelas ruas reais utilizando OpenStreetMap + OSRM.

```
```
