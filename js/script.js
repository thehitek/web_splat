document.addEventListener("DOMContentLoaded", function () {
    // Инициализация карты
    var map = L.map('map').setView([55.751244, 37.618423], 5); // Москва по умолчанию

    // Подключаем OpenStreetMap
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    // Маркеры передатчика и приемника
    var transmitterMarker = L.marker([55.751244, 37.618423], { draggable: true }).addTo(map);
    var receiverMarker = L.marker([55.761244, 37.628423], { draggable: true }).addTo(map);

    // Обновление координат при перемещении маркеров
    function updateCoordinates() {
        let tPos = transmitterMarker.getLatLng();
        let rPos = receiverMarker.getLatLng();

        document.getElementById("transmitter-lat").value = tPos.lat.toFixed(6);
        document.getElementById("transmitter-lon").value = tPos.lng.toFixed(6);
        document.getElementById("receiver-lat").value = rPos.lat.toFixed(6);
        document.getElementById("receiver-lon").value = rPos.lng.toFixed(6);
    }

    transmitterMarker.on('dragend', updateCoordinates);
    receiverMarker.on('dragend', updateCoordinates);

    // График потерь сигнала
    var ctx = document.getElementById("chart").getContext("2d");
    var signalChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ["0km", "1km", "2km", "3km", "4km"],
            datasets: [{
                label: "Потери сигнала (дБ)",
                data: [0, -5, -10, -15, -20],
                borderColor: "#007BFF",
                borderWidth: 2,
                fill: false
            }]
        }
    });

    // Обработчик кнопки "Рассчитать"
    document.getElementById("calculate").addEventListener("click", function () {
        alert("Расчет запущен! Пока только демо-версия.");
        // Тут можно добавить логику для реального расчета зон покрытия
    });

    // Инициализация координат в полях ввода
    updateCoordinates();
});

