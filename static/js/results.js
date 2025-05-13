import { kml } from "https://unpkg.com/@tmcw/togeojson?module";

const imageList = [
  { label: "Terrain profile", query: "static/splat/terrain_profile.png", id: "terrain_profile", type: "image" },
  { label: "Elevation profile", query: "static/splat/elevation_profile.png", id: "elevation_profile", type: "image" },
  { label: "Height profile", query: "static/splat/height_profile.png", id: "height_profile", type: "image" },
  { label: "Height profile norm", query: "static/splat/height_profile_norm.png", id: "height_profile_norm", type: "image" },
  { label: "Path loss profile", query: "static/splat/path_loss_profile.png", id: "path_loss_profile", type: "image" },
  { label: "TX-RX line map", query: "static/splat/tx_rx_line_map.ppm", id: "tx_rx_line_map", type: "ppm" },
  { label: "KML file", query: "static/splat/TX-to-RX.kml", id: "kml", type: "map" },
];

const sidebar = document.getElementById('sidebar');
const imageEl = document.getElementById('image');
const mapEl = document.getElementById('kml-map');

imageList.forEach(item => {
  const button = document.createElement('button');
  button.textContent = item.label;
  button.id = item.id;
  button.addEventListener('click', () => {
    if (item.type === "image") {
      imageEl.src = item.query;
      imageEl.classList.remove('hidden');
      mapEl.classList.add('hidden');
    } else if (item.type === "map") {
      imageEl.classList.add('hidden');
      mapEl.classList.remove('hidden');
    }
  });
  sidebar.appendChild(button);
});

const firstButton = document.getElementById('terrain_profile');
firstButton.click(); // Trigger the click event on the first button to load the default image

document.addEventListener("DOMContentLoaded", function () {
  // Инициализация карты
  ymaps.ready(init);

  function init() {
    var map = new ymaps.Map('kml-map', {
      center: [30.487911, 59.902639], // СПб по умолчанию
      zoom: 10
    });

    // Загрузка через geoQuery
    fetch("static/splat/TX-to-RX.kml").then(function (response) {
      return response.text();
    }).then(function (xml) {
      const xmlJson = kml(new DOMParser().parseFromString(xml, "text/xml"));
      console.log(xmlJson);
      ymaps.geoQuery(xmlJson).addToMap(map);
    });
  }
});


function drawPPM(ppmData) {
  const lines = ppmData.split(/\r?\n/).filter(line => !line.startsWith('#'));
  const [format, width, height, maxColor] = lines.join(' ').split(/\s+/);
  
  if (format !== 'P3') {
      alert('Поддерживается только текстовый формат P3');
      return;
  }

  const pixels = lines.slice(4).join(' ').split(/\s+/).map(Number);
  const canvas = document.getElementById('canvas');
  const ctx = canvas.getContext('2d');
  
  canvas.width = parseInt(width);
  canvas.height = parseInt(height);
  const imageData = ctx.createImageData(canvas.width, canvas.height);
  
  let pixelIndex = 0;
  for (let i = 0; i < pixels.length; i += 3) {
      imageData.data[pixelIndex++] = pixels[i];     // R
      imageData.data[pixelIndex++] = pixels[i + 1]; // G
      imageData.data[pixelIndex++] = pixels[i + 2]; // B
      imageData.data[pixelIndex++] = 255;           // Alpha
  }
  
  ctx.putImageData(imageData, 0, 0);
}