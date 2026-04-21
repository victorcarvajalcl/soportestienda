const BASE = "https://victorcarvajalcl.github.io/soportestienda";

const map = L.map('map').setView([-33.45, -70.65], 11);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png')
  .addTo(map);

let layer;

function cargar(nivel) {

  if (layer) map.removeLayer(layer);

  fetch(`${BASE}/data/soportes_${nivel}.csv`)
    .then(res => res.text())
    .then(csv => {

      const rows = csv.trim().split("\n").slice(1);

      layer = L.layerGroup();

      rows.forEach(row => {

        if (!row.trim()) return;

        const cols = row.split(",");

        const h = cols[0];
        const total = parseInt(cols[1]);

        if (!h || isNaN(total)) return;

        try {
          const boundary = h3.cellToBoundary(h, true);
          const latlngs = boundary.map(c => [c[0], c[1]]);

          const color =
            total > 500 ? "red" :
            total > 200 ? "orange" :
            "green";

          L.polygon(latlngs, {
            color: color,
            fillOpacity: 0.5,
            weight: 1
          })
          .bindPopup(`Soportes: ${total}`)
          .addTo(layer);

        } catch (e) {
          console.log("Error H3:", h);
        }

      });

      layer.addTo(map);

    })
    .catch(err => console.error("Error:", err));
}

// inicial
cargar("h6");

// selector
document.getElementById("nivel").addEventListener("change", e => {
  cargar(e.target.value);
});