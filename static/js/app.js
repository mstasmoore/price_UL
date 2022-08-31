function pricePrediction(){
    var t = d3.select('results')

    var origin = document.getElementById("origin");
    var valueOrigin = origin.value;
    var destination = document.getElementById("destination");
    var valueDestination = destination.value;
    var weather = document.getElementById("weather");
    var valueWeather = weather.value;
    var vehicleType = document.getElementById("vehicleType");
    var valueVehType = vehicleType.value;
    var weekDay = document.getElementById("weekDay");
    var valueWeekDay = weekDay.value;

    d3.json(`https://lyftuberprediction.herokuapp.com/api/prediction/${valueOrigin}/${valueDestination}/${valueWeather}/${valueVehType}/${valueWeekDay}`, {
      method:"GET"
    })
    .then(json => {
        document.getElementById('bestResults').innerText = 'Your best choice would be: ';
        document.getElementById('bestCarType').innerText = json.type;
        document.getElementById('bestPrice').innerText = json.price;
    });

}

