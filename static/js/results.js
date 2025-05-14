import { kml } from "https://unpkg.com/@tmcw/togeojson?module";

const imageList = [
  { label: "Профиль местности", query: "static/splat/terrain_profile.png", id: "terrain_profile", type: "image" },
  { label: "График возвышений", query: "static/splat/elevation_profile.png", id: "elevation_profile", type: "image" },
  { label: "Высота ландшафта", query: "static/splat/height_profile.png", id: "height_profile", type: "image" },
  { label: "Высота ландшафта нормализованная", query: "static/splat/height_profile_norm.png", id: "height_profile_norm", type: "image" },
  { label: "Потери на пути", query: "static/splat/path_loss_profile.png", id: "path_loss_profile", type: "image" },
  { label: "Линия прямого луча", query: "static/splat/TX-to-RX.kml", id: "kml", type: "map" },
  { label: "Зона покрытия прямой видимости", query: "static/splat/tx_coverage_map.png", id: "tx_coverage_map", type: "image" },
  { label: "Карта потерь", query: "static/splat/tx_loss_map.png", id: "tx_loss_map", type: "image" },
  { label: "Карта напряженности", query: "static/splat/tx_field_map.png", id: "tx_field_map", type: "image" },
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