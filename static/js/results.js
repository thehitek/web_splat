const imageList = [
  { label: "Terrain profile", query: "static/splat/terrain_profile.png", id: "terrain_profile" },
  { label: "Elevation profile", query: "static/splat/elevation_profile.png", id: "elevation_profile" },
  { label: "Height profile", query: "static/splat/height_profile.png", id: "height_profile" },
  { label: "Height profile norm", query: "static/splat/height_profile_norm.png", id: "height_profile_norm" },
  { label: "Path loss profile", query: "static/splat/path_loss_profile.png", id: "path_loss_profile" },
  { label: "TX-RX line map", query: "static/splat/tx_rx_line_map.ppm", id: "tx_rx_line_map" },
];

const sidebar = document.getElementById('sidebar');
const imageEl = document.getElementById('image');

imageList.forEach(item => {
  const button = document.createElement('button');
  button.textContent = item.label;
  button.id = item.id;
  button.addEventListener('click', () => imageEl.src = item.query);
  sidebar.appendChild(button);
});

const firstButton = document.getElementById('terrain_profile');
firstButton.click(); // Trigger the click event on the first button to load the default image