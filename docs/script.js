rows.forEach(row => {

  if (!row.trim()) return;

  const cols = row.split(",");

  const h = cols[0];
  const total = parseInt(cols[1]);

  if (!h || isNaN(total)) return;

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

});