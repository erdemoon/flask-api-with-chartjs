var ctx = document.getElementById("myChart").getContext("2d");
var timeHour = moment().format("h:mm");
var timeFromHour = moment().startOf("hour").fromNow();

let myChart;

var timeFormat = "DD.MM.YYYY HH:mm:ss";

fetch("http://127.0.0.1:5000/api/log")
  .then((response) => response.json())
  .then((data) => {
    setupChart(data);
  });

function setupChart(dataToParse) {
  myChart = new Chart(ctx, {
    type: "line",
    data: {
      datasets: [
        {
          label: "GET",
          data: parseDataForChart(dataToParse, "get"),
          backgroundColor: "rgba(235, 122, 59, 0.5)",
          borderColor: "rgba(255, 99, 132, 1)",
          borderWidth: 1,
          lineTension: 0,
          borderWidth: 3,
        },
        {
          label: "POST",
          data: parseDataForChart(dataToParse, "post"),
          backgroundColor: "rgba(54, 162, 235, 0.5)",
          borderColor: "rgba(54, 162, 235, 1)",
          borderWidth: 1,
          lineTension: 0,
          borderWidth: 3,
        },
        {
          label: "PUT",
          data: parseDataForChart(dataToParse, "put"),
          backgroundColor: "rgba(54, 12, 235, 0.5)",
          borderColor: "rgba(54, 12, 235, 1)",
          borderWidth: 1,
          lineTension: 0,
          borderWidth: 3,
        },
        {
          label: "DELETE",
          data: parseDataForChart(dataToParse, "delete"),
          backgroundColor: "rgba(255, 255, 0, 0.5)",
          borderColor: "rgba(54, 162, 25, 1)",
          borderWidth: 1,
          lineTension: 0,
          borderWidth: 3,
        },
      ],
    },
    options: {
      elements:{
        point:{
          radius:1,
        },
      },
      responsive: true,
      title: {
        display: true,
        text: "Chart.js Time Scale",
      },
      scales: {
        xAxes: [
          {
            type: "time",
            time: {
              parser: timeFormat,
              tooltipFormat: "ll",
              unitStepSize: 5,
            },
            scaleLabel: {
              display: true,
              labelString: "Time",
            },
            ticks:{
              min:moment().add(-1,"hours"),
              max:moment(),

            }
          },
        ],
        yAxes: [
          {
            scaleLabel: {
              display: true,
              labelString: "value",
            },
          },
        ],
      },
    },
  });

  myChart.canvas.parentNode.style.height = "100px";
  myChart.canvas.parentNode.style.width = "1200px";
  return myChart;
}

function parseDataForChart(data, method) {
  var data1 = [];
  for (item in data[method]) {
    data1.push(data[method][item]);
  }
  console.log(data1);
  return data1;
}

setInterval(function(){
  fetch("http://127.0.0.1:5000/api/log")
  .then((response) => response.json())
  .then((data) => {
    myChart.data.datasets[0].data=parseDataForChart(data, "get");
    myChart.data.datasets[1].data=parseDataForChart(data, "post");
    myChart.data.datasets[2].data=parseDataForChart(data, "put");
    myChart.data.datasets[3].data=parseDataForChart(data, "delete");
    myChart.options.scales.xAxes[0].ticks.max = moment()
    myChart.options.scales.xAxes[0].ticks.min = moment().add(-1,"hours")
    myChart.update();
  });
}, 5000);