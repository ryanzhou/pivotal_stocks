$(function () {
  $('#{{ element_id }}').highcharts({
    chart: {
      type: 'pie'
    },
    credits: false,
    title: {
      text: '{{ chart.title() | to_human }}'
    },
    subtitle: {
      text: 'Click the slices to view {{ chart.pivot_table.column_label | to_human }}. Generated by Pivotal Stocks.'
    },
    plotOptions: {
      series: {
        dataLabels: {
          enabled: false
        },
        showInLegend: true
      }
    },

    tooltip: {
      headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
      pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:f}</b><br/>'
    },

    series: [{
      name: '{{ chart.pivot_table.row_label | to_human }}',
      colorByPoint: true,
      data: {{ chart.series_data() | to_json }}
    }],
    drilldown: {
      series: {{ chart.drilldown_series() | to_json }}
    }
  });
});
