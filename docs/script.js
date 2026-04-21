const map = L.map('map').setView([-33.45, -70.65], 11);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png')
  .addTo(map);

let layer;

function cargar(nivel) {

  // eliminar capa anterior
  if (layer) map.removeLayer(layer);

  fetch(`data/soportes_${nivel}.csv`)
    .then(res => {
      if (!res.ok) throw new Error("No se pudo cargar CSV");
      return res.text();
    })
    .then(csv => {

      console.log("CSV cargado"); // debug

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
            total > 500 ? "#ff0000" :
            total > 200 ? "#ff9900" :
            "#00cc66";

          L.polygon(latlngs, {
            color: color,
            fillColor: color,
            fillOpacity: 0.5,
            weight: 1
          })
          .bindPopup(`
            <b>H3:</b> ${h}<br>
            <b>Soportes:</b> ${total}
          `)
          .addTo(layer);

        } catch (e) {
          console.log("Error H3:", h);
        }

      });

      layer.addTo(map);

      console.log("Hexágonos dibujados:", rows.length);

    })
    .catch(err => {
      console.error("ERROR:", err);
      alert("No se pudo cargar la data");
    });
}

// cargar inicial
cargar("h6");

// selector
document.getElementById("nivel").addEventListener("change", e => {
  cargar(e.target.value);
});