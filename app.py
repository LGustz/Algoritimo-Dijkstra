
from flask import Flask, render_template_string, request, jsonify
import requests

app = Flask(__name__)


# ============================================================
# HTML
# ============================================================

HTML_INTERFACE = """

<!DOCTYPE html>

<html lang="pt-BR">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>
        Rota por ruas - Botucatu
    </title>


    <!-- LEAFLET CSS -->

    <link
        rel="stylesheet"
        href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
    >


    <!-- LEAFLET JS -->

    <script
        src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js">
    </script>


    <style>

        * {
            box-sizing: border-box;
        }


        body {

            margin: 0;

            padding: 0;

            font-family: Arial, sans-serif;

        }


        #map {

            width: 100vw;

            height: 100vh;

        }


        #painel {

            position: absolute;

            top: 15px;

            left: 15px;

            width: 340px;

            background: white;

            padding: 20px;

            border-radius: 12px;

            box-shadow:
                0 4px 20px
                rgba(0, 0, 0, 0.25);

            z-index: 1000;

        }


        #painel h2 {

            margin-top: 0;

            margin-bottom: 8px;

        }


        #status {

            margin-top: 15px;

            padding: 12px;

            border-radius: 8px;

            background: #f1f3f5;

            line-height: 1.5;

        }


        button {

            width: 100%;

            padding: 11px;

            margin-top: 12px;

            border: none;

            border-radius: 7px;

            background: #007bff;

            color: white;

            font-size: 15px;

            font-weight: bold;

            cursor: pointer;

        }


        button:hover {

            background: #0056b3;

        }


        #limpar {

            background: #dc3545;

        }


        #limpar:hover {

            background: #a71d2a;

        }


        .origem {

            color: #198754;

            font-weight: bold;

        }


        .destino {

            color: #dc3545;

            font-weight: bold;

        }


        .info {

            margin-top: 12px;

            font-size: 13px;

            color: #555;

        }


        .coordenadas {

            font-size: 11px;

            color: #666;

        }

    </style>

</head>


<body>


    <!-- ====================================================
         PAINEL
    ===================================================== -->

    <div id="painel">


        <h2>
            🚗 Rota pelas ruas
        </h2>


        <div>

            Clique em qualquer lugar do mapa
            para escolher os pontos.

        </div>


        <div id="status">

            🟢

            <b>
                Clique no mapa para definir a origem
            </b>

        </div>


        <button
            id="limpar"
            onclick="limparMapa()"
        >

            Limpar pontos

        </button>


        <div class="info">

            A rota segue as ruas reais utilizando
            OpenStreetMap + OSRM.

        </div>


    </div>


    <!-- ====================================================
         MAPA
    ===================================================== -->

    <div id="map"></div>


    <script>


        // ==================================================
        // VARIÁVEIS
        // ==================================================

        let map;

        let origem = null;

        let destino = null;

        let marcadorOrigem = null;

        let marcadorDestino = null;

        let linhaRota = null;


        // ==================================================
        // INICIALIZAÇÃO
        // ==================================================

        window.onload = function() {


            map = L.map('map').setView(

                [
                    -22.8864,
                    -48.4429
                ],

                13

            );


            // ==============================================
            // OPENSTREETMAP
            // ==============================================

            L.tileLayer(

                'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',

                {

                    maxZoom: 19,

                    attribution:
                        '&copy; OpenStreetMap contributors'

                }

            ).addTo(map);


            // ==============================================
            // CLIQUE NO MAPA
            // ==============================================

            map.on(
                'click',
                clicarNoMapa
            );

        };


        // ==================================================
        // CLIQUE NO MAPA
        // ==================================================

        function clicarNoMapa(evento) {


            const lat =
                evento.latlng.lat;


            const lon =
                evento.latlng.lng;


            // ==============================================
            // PRIMEIRO CLIQUE
            // ==============================================

            if (!origem) {


                origem = {

                    lat: lat,

                    lon: lon

                };


                marcadorOrigem =
                    L.marker(

                        [
                            lat,
                            lon
                        ],

                        {

                            title:
                                'Origem'

                        }

                    )

                    .addTo(map)

                    .bindPopup(

                        '<b>🟢 Origem</b><br>' +

                        'Latitude: ' +
                        lat.toFixed(6) +

                        '<br>' +

                        'Longitude: ' +
                        lon.toFixed(6)

                    )

                    .openPopup();


                atualizarStatus(

                    '🟢 Origem definida.<br>' +

                    '👉 Agora clique no mapa para definir o destino.'

                );


                return;

            }


            // ==============================================
            // SEGUNDO CLIQUE
            // ==============================================

            if (!destino) {


                destino = {

                    lat: lat,

                    lon: lon

                };


                marcadorDestino =
                    L.marker(

                        [
                            lat,
                            lon
                        ],

                        {

                            title:
                                'Destino'

                        }

                    )

                    .addTo(map)

                    .bindPopup(

                        '<b>🔴 Destino</b><br>' +

                        'Latitude: ' +
                        lat.toFixed(6) +

                        '<br>' +

                        'Longitude: ' +
                        lon.toFixed(6)

                    )

                    .openPopup();


                atualizarStatus(

                    '⏳ Calculando rota pelas ruas...'

                );


                calcularRota();


                return;

            }

        }


        // ==================================================
        // CALCULAR ROTA
        // ==================================================

        function calcularRota() {


            fetch(

                '/calcular_rota',

                {

                    method: 'POST',

                    headers: {

                        'Content-Type':
                            'application/json'

                    },

                    body: JSON.stringify({

                        origem: origem,

                        destino: destino

                    })

                }

            )


            .then(

                function(resposta) {

                    return resposta.json();

                }

            )


            .then(

                function(data) {


                    // ======================================
                    // ERRO
                    // ======================================

                    if (data.erro) {


                        alert(
                            data.erro
                        );


                        limparMapa();


                        return;

                    }


                    // ======================================
                    // REMOVE ROTA ANTERIOR
                    // ======================================

                    if (linhaRota) {

                        map.removeLayer(
                            linhaRota
                        );

                    }


                    // ======================================
                    // DESENHA ROTA
                    // ======================================

                    linhaRota =
                        L.polyline(

                            data.coordenadas,

                            {

                                color:
                                    '#007bff',

                                weight: 7,

                                opacity: 0.9,

                                lineJoin:
                                    'round',

                                lineCap:
                                    'round'

                            }

                        ).addTo(map);


                    // ======================================
                    // AJUSTA ZOOM
                    // ======================================

                    map.fitBounds(

                        linhaRota.getBounds(),

                        {

                            padding:
                                [60, 60]

                        }

                    );


                    // ======================================
                    // RESULTADO
                    // ======================================

                    atualizarStatus(

                        '🟢 Origem definida' +

                        '<br>' +

                        '🔴 Destino definido' +

                        '<hr>' +

                        '🛣️ <b>Rota encontrada</b>' +

                        '<br><br>' +

                        '📏 Distância: ' +

                        '<b>' +

                        data.distancia +

                        ' km' +

                        '</b>' +

                        '<br><br>' +

                        '⏱️ Tempo estimado: ' +

                        '<b>' +

                        data.duracao +

                        '</b>'

                    );

                }

            )


            .catch(

                function(erro) {


                    console.error(
                        erro
                    );


                    alert(

                        'Erro ao calcular a rota.'

                    );


                    limparMapa();

                }

            );

        }


        // ==================================================
        // ATUALIZA STATUS
        // ==================================================

        function atualizarStatus(texto) {


            document.getElementById(
                'status'
            ).innerHTML = texto;

        }


        // ==================================================
        // LIMPAR
        // ==================================================

        function limparMapa() {


            origem = null;

            destino = null;


            // ==============================================
            // REMOVE MARCADOR ORIGEM
            // ==============================================

            if (marcadorOrigem) {

                map.removeLayer(
                    marcadorOrigem
                );

                marcadorOrigem = null;

            }


            // ==============================================
            // REMOVE MARCADOR DESTINO
            // ==============================================

            if (marcadorDestino) {

                map.removeLayer(
                    marcadorDestino
                );

                marcadorDestino = null;

            }


            // ==============================================
            // REMOVE ROTA
            // ==============================================

            if (linhaRota) {

                map.removeLayer(
                    linhaRota
                );

                linhaRota = null;

            }


            atualizarStatus(

                '🟢 <b>Clique no mapa para definir a origem</b>'

            );

        }

    </script>


</body>

</html>

"""


# ============================================================
# PÁGINA PRINCIPAL
# ============================================================

@app.route('/')
def home():

    return render_template_string(
        HTML_INTERFACE
    )


# ============================================================
# CALCULAR ROTA
# ============================================================

@app.route(
    '/calcular_rota',
    methods=['POST']
)
def calcular_rota():


    dados = request.get_json()


    if not dados:

        return jsonify({

            'erro':
                'Dados não recebidos.'

        }), 400


    origem = dados.get(
        'origem'
    )


    destino = dados.get(
        'destino'
    )


    if not origem or not destino:

        return jsonify({

            'erro':
                'Origem ou destino não informado.'

        }), 400


    try:


        # ====================================================
        # COORDENADAS
        # ====================================================

        lat_origem = float(origem['lat'])

        lon_origem = float(origem['lon'])


        lat_destino = float(destino['lat'])

        lon_destino = float(destino['lon'])


        # ====================================================
        # OSRM
        #
        # FORMATO:
        #
        # longitude,latitude
        # ====================================================

        url = (

            'https://router.project-osrm.org/'

            'route/v1/driving/'

            f'{lon_origem},{lat_origem};'

            f'{lon_destino},{lat_destino}'

            '?overview=full'

            '&geometries=geojson'

        )


        # ====================================================
        # CONSULTA OSRM
        # ====================================================

        resposta = requests.get(

            url,

            timeout=20

        )


        resposta.raise_for_status()


        dados_rota = resposta.json()


        # ====================================================
        # VERIFICA
        # ====================================================

        if (
            dados_rota.get('code')
            != 'Ok'
        ):

            return jsonify({

                'erro':
                    'Não foi encontrada uma rota pelas ruas entre os pontos.'

            }), 400


        rota = dados_rota['routes'][0]


        # ====================================================
        # DISTÂNCIA
        # ====================================================

        distancia_km = (

            rota['distance'] / 1000

        )


        # ====================================================
        # DURAÇÃO
        # ====================================================

        segundos = int(rota['duration'])


        minutos = round(segundos / 60)


        if minutos < 60:

            duracao = (
                f'{minutos} minutos'
            )

        else:

            horas = minutos // 60

            minutos_restantes = minutos % 60


            if minutos_restantes:

                duracao = (

                    f'{horas}h '
                    f'{minutos_restantes}min'

                )

            else:

                duracao = (
                    f'{horas}h'
                )


        # ====================================================
        # GEOMETRIA
        # ====================================================

        geometria =rota['geometry']['coordinates']


        # OSRM:
        #
        # longitude, latitude
        #
        # Leaflet:
        #
        # latitude, longitude

        coordenadas = [

            [
                ponto[1],
                ponto[0]
            ]

            for ponto in geometria

        ]


        # ====================================================
        # RETORNO
        # ====================================================

        return jsonify({

            'distancia':
                round(
                    distancia_km,
                    2
                ),

            'duracao':
                duracao,

            'coordenadas':
                coordenadas

        })


    # ========================================================
    # ERRO DE CONEXÃO
    # ========================================================

    except requests.exceptions.RequestException as erro:


        print(
            'Erro no OSRM:',
            erro
        )


        return jsonify({

            'erro':
                'Não foi possível acessar o serviço de mapas. '
                'Verifique sua conexão com a internet.'

        }), 500


    # ========================================================
    # ERRO GERAL
    # ========================================================

    except Exception as erro:


        print(
            'Erro interno:',
            erro
        )


        return jsonify({

            'erro':
                'Erro interno ao calcular a rota.'

        }), 500


# ============================================================
# INICIAR SERVIDOR
# ============================================================

if __name__ == '__main__':

    app.run(

        host='127.0.0.1',

        port=5000,

        debug=True

    )
