$(function () {
    $('#{{ element_id }}').highcharts({

	    chart: {
	        type: 'bubble',
	        zoomType: 'xy'
	    },
      credits: false,
	    title: {
	    	text: ''
	    },
      xAxis: {
        title: {
          text: 'Dividend Yield %'
        }
      },
      yAxis: {
        min: 0.1,
        max: 100,
        title: {
          text: 'P/E Ratio'
        }
      },
      tooltip: {
        headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
        pointFormat: '<span style="color:{point.color}"><b>{point.name}</b></span><br>P/E: {point.y:f}<br>Dividend Yield: {point.x:f}%<br>Market Cap: {point.z}<br/>'
      },
	    series: [{
          name: 'Stock',
	        data: {{ data | to_json }}
	    }]
	});

});
