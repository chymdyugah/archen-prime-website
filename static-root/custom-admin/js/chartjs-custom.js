$(document).ready(function() {
    $.get("{% url 'mainapp:ajax' %}", function(data, status){
        var barChartData = {
            // labels : ["January","February","March","April","May","June","July"],
            labels : data.lgas_count,
            datasets : [
                {
                    fillColor : "rgba(220,220,220,0.5)",
                    strokeColor : "rgba(220,220,220,1)",
                    data : [65,59,90,81,56,55,40]
                }
            ]
    
        };
    
        new Chart(document.getElementById("bar").getContext("2d")).Bar(barChartData);    
    });

});