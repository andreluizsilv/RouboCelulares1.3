{%load static %}
<script>
// Inicializa o mapa
var map = L.map('map').setView([-23.5505, -46.6333], 12); // Coordenadas do centro do mapa

// Adiciona a camada de tile do OpenStreetMap
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Dados dos bairros (recebidos do servidor)
var bairros = [
    {% for bairro in bairros_mais_atacados %}
    {
        "bairro": "{{ bairro.bairro}}",
        "latitude": {{ bairro.latitude|floatformat }},
        "longitude": {{ bairro.longitude|floatformat }},
        "num_ocorrencias": {{ bairro.num_ocorrencias }},
        "id": {{ bairro.id }}
    }{% if not forloop.last %},{% endif %}
    {% endfor %}
];


// Adiciona marcadores para cada bairro
bairros.forEach(function(bairro) {
    L.marker([bairro.latitude, bairro.longitude])
        .addTo(map)
        .bindPopup('<b>' + bairro.bairro + '</b><br>Número de Ocorrências: ' + bairro.num_ocorrencias)
        .on('click', function() {
            // Redireciona para a página de detalhes do bairro
            window.location.href = "/detalhes/" + bairro.id + "/";
        });
});
</script>