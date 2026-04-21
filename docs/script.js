const map = L.map('map').setView([-33.45, -70.65], 11);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

let layer;

function cargar(nivel) {

  if (layer) map.removeLayer(layer);

  fetch(`../data/soportes_${nivel}.csv`)
    .then(res => res.text())
    .then(csv => {

      const rows = csv.split("\n").slice(1);

      layer = L.layerGroup();

      rows.forEach(row => {

        const [h, total] = row.split(",");

        if (!h) return;

        const boundary = h3.cellToBoundary(h, true);
        const latlngs = boundary.map(c => [c[0], c[1]]);

        const color =
          total > 15 ? "red" :
          total > 8 ? "orange" :
          "green";

        L.polygon(latlngs, {
          color: color,
          fillOpacity: 0.5,
          weight: 1
        })
        .bindPopup(`Soportes: ${total}`)
        .addTo(layer);

      });

      layer.addTo(map);

    });
}

// inicial
cargar("h6");

// selector
document.getElementById("nivel").addEventListener("change", e => {
  cargar(e.target.value);
});