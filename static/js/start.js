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
    document.getElementById("calculate").addEventListener("click", calculate);
});

function calculate() {
    // Получаем координаты передатчика и приемника
    var txLat = parseFloat(document.getElementById("transmitter-lat").value);
    var txLon = 360.0 - parseFloat(document.getElementById("transmitter-lon").value);
    var rxLat = parseFloat(document.getElementById("receiver-lat").value);
    var rxLon = 360.0 - parseFloat(document.getElementById("receiver-lon").value);
    // Проверяем, что координаты валидные
    if (isNaN(txLat) || isNaN(txLon) || isNaN(rxLat) || isNaN(rxLon)) {
        alert("Пожалуйста, введите корректные координаты.");
        return;
    }
    // Формируем данные для отправки

    function getEarthDielectricConstant(i) {
        switch (i){
            case 1: return 80;
            case 2: return 25;
            case 3: return 80;
            case 4: return 12;
            case 5: return 15;
            case 6: return 15;
            case 7: return 13;
            case 8: return 5;
            case 9: return 4;
            default: return 5; // Default to City
        }
    }

    function getEarthConductivity(i) {
        switch (i){
            case 1: return 5.0;
            case 2: return 0.02;
            case 3: return 0.01;
            case 4: return 0.007;
            case 5: return 0.005;
            case 6: return 0.005;
            case 7: return 0.002;
            case 8: return 0.001;
            case 9: return 0.001;
            default: return 0.001; // Default to City
        }
    }

    const data = {
        tx_lat: txLat,
        tx_lon: txLon,
        tx_height: parseFloat(document.getElementById("transmitter-height").value),
    
        rx_lat: rxLat,
        rx_lon: rxLon,
        rx_height: parseFloat(document.getElementById("receiver-height").value),
    
        erp: parseFloat(document.getElementById("erp").value),
        frequency: parseFloat(document.getElementById("frequency").value),
        
        polarization_type: document.getElementById("polarization").value,
        
        situations_fraction: parseFloat(document.getElementById("situations-fraction").value),
        time_fraction: parseFloat(document.getElementById("time-fraction").value),
    
        radioclimate: document.getElementById("radioclimate").value,
        atmospheric_bending_constant: parseFloat(document.getElementById("atmospheric-bending-constant").value),

        earth_dielectric_constant: getEarthDielectricConstant(parseInt(document.getElementById("terrain-type").value)),
        earth_conductivity: getEarthConductivity(parseInt(document.getElementById("terrain-type").value)),
    }

    // Отправляем POST запрос
    fetch('http://127.0.0.1:8000/input-data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Ошибка при отправке данных');
        }
        return response.json();
    })
    .then(result => {
        // alert('Успешный ответ:', result);
        window.location.href = '/results';
    })
    .catch(error => {
        alert('Ошибка:', error);
    });
}
