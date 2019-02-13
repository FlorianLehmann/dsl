$(document).ready(function() {
    var ctx = document.getElementById("stateChart").getContext("2d");

    var data = {
        labels: ["January", "February", "March", "April", "May", "June", "July"],
        datasets: [
            {
                label: "My First dataset",
                fillColor: "rgba(220,220,220,0.2)",
                strokeColor: "rgba(220,220,220,1)",
                pointColor: "rgba(220,220,220,1)",
                pointStrokeColor: "#fff",
                pointHighlightFill: "#fff",
                pointHighlightStroke: "rgba(220,220,220,1)",
                data: [0, 1, 1, 1, 0, 1, 0]
            },
            {
                label: "My Second dataset",
                fillColor: "rgba(151,187,205,0.2)",
                strokeColor: "rgba(151,187,205,1)",
                pointColor: "rgba(151,187,205,1)",
                pointStrokeColor: "#fff",
                pointHighlightFill: "#fff",
                pointHighlightStroke: "rgba(151,187,205,1)",
                data: [1, 0, 0, 0, 1, 0, 1]
            }
        ]
    };
    var options = {
        animation: false,
        scaleStartValue: 0,
        elements: {
            line: {
                tension: 0 // disables bezier curves
            }
        }
    };

    var myLineChart = new Chart(ctx).Line(data, options);

    setInterval(function() {
        addData(myLineChart, setLabels(), setData());
    }, 2000);

    function addData(chart, pointOne, pointTwo) {
        chart.datasets[0].points.push(pointOne);
        chart.datasets[1].points.push(pointTwo);
        chart.update();
    }

    function setLabels() {
        var nextMonthIndex = months.indexOf(data.labels[data.labels.length - 1]) + 1;
        var nextMonthName = months[nextMonthIndex] != undefined ? months[nextMonthIndex] : "January";
        return nextMonthName;
    }

    function setData() {
        return Math.random() > 0.5 ? 1 : 0;
    }

    var months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
    ];
});
