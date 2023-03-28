$(document).ready(function() {
    let input = $('#ticker-input');
    let stockChart = $('#stock-chart');
    let submitBtn = $('#submit-btn');

    input.autocomplete({
        source: function(request, response) {
            $.getJSON('/symbols', {query: request.term}, function(data) {
                let results = data.map(stock => {
                    return {
                        label: `${stock['1. symbol']} - ${stock['2. name']}`,
                        value: stock['1. symbol']
                    };
                });
                response(results);
            });
        },
        minLength: 1
    });

    submitBtn.on('click', function() {
        let ticker = input.val();
        $.get('/stock', {ticker: ticker}, function(graph_html) {
            stockChart.html(graph_html);
            stockChart.css("display", "block");
            console.log(stockChart.html())
        });
    });
});