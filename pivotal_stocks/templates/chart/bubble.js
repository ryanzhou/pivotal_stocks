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
        min: 0,
        max: 100,
        title: {
          text: 'P/E Ratio'
        }
      },
      yAxis: {
        min: 0,
        max: 12,
        title: {
          text: 'Dividend Yield'
        }
      },
      tooltip: {
        headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
        pointFormat: '<span style="color:{point.color}"><b>{point.name}</b></span><br>P/E Ratio: {point.x:f}<br>Dividend Yield: {point.y:.2f}%<br>Market Cap: ${point.z},000<br/>'
      },
	    series: {{ series | to_json }}
	});

});
