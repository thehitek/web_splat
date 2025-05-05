document.addEventListener("DOMContentLoaded", function () {
    // Инициализация карты
    ymaps.ready(init);
    
    function init() {
        var map = new ymaps.Map('map', {
            center: [59.902639, 30.487911], // СПб по умолчанию
            zoom: 10
        });

        // Создаем метки
        var transmitterPlacemark = new ymaps.Placemark([59.9766112, 30.3161452], {
            hintContent: 'Передатчик',
            balloonContent: 'Координаты передатчика'
        }, {
            draggable: true,
            preset: 'islands#redIcon'
        });

        var receiverPlacemark = new ymaps.Placemark([59.902639, 30.487911], {
            hintContent: 'Приемник',
            balloonContent: 'Координаты приемника'
        }, {draggable: true, preset: 'islands#blueIcon'})
        
            // Добавляем метки на карту
        map.geoObjects.add(transmitterPlacemark);
        map.geoObjects.add(receiverPlacemark);
    
        // Функции обновления координат
        function updateTXCoordinates() {
            var tPos = transmitterPlacemark.geometry.getCoordinates();

            document.getElementById("transmitter-lat").value = tPos[0].toFixed(6);
            document.getElementById("transmitter-lon").value = tPos[1].toFixed(6);

        }
        function updateRXCoordinates() {
            var rPos = receiverPlacemark.geometry.getCoordinates();

            document.getElementById("receiver-lat").value = rPos[0].toFixed(6);
            document.getElementById("receiver-lon").value = rPos[1].toFixed(6);
        }

        // Обработчики перемещения меток
        transmitterPlacemark.events.add('dragend', updateTXCoordinates);
        receiverPlacemark.events.add('dragend', updateRXCoordinates);
    };

    // Обработчик кнопки "Рассчитать"
    document.getElementById("calculate").addEventListener("click", function () {
        alert("Расчет запущен! Пока только демо-версия.");
        // Тут можно добавить логику для реального расчета зон покрытия
    });
});

function calculate() {
    // Получаем координаты передатчика и приемника
    var txLat = parseFloat(document.getElementById("transmitter-lat").value);
    var txLon = parseFloat(document.getElementById("transmitter-lon").value);
    var rxLat = parseFloat(document.getElementById("receiver-lat").value);
    var rxLon = parseFloat(document.getElementById("receiver-lon").value);
    // Проверяем, что координаты валидные
    if (isNaN(txLat) || isNaN(txLon) || isNaN(rxLat) || isNaN(rxLon)) {
        alert("Пожалуйста, введите корректные координаты.");
        return;
    }
    
}
