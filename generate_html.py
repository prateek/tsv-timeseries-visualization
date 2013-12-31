#!/usr/bin/env python
import csv
import sys
from sys import argv
from collections import defaultdict
from time import mktime
from datetime import datetime

if len(argv) != 2:
  print "Usage: ./generate_html <tsv-file>" 
  sys.exit(-1)

# data dict initialization
# field -> [ (unix_timestamp, value) ]
data_dict = defaultdict( lambda: [] )
vendors = []

# read tsv data
with open(argv[1], 'r') as tsvfile:
  tsv_reader = csv.DictReader( tsvfile, delimiter='\t' )
  vendors = [ field for field in tsv_reader.fieldnames if field != 'Date' ]
  for row in tsv_reader:
    date = datetime.strptime( row['Date'], "%d-%b-%y")
    date_ts = mktime( date.timetuple() )
    for vendor in vendors:
      data_dict[ vendor ].append( (date_ts, row[vendor] or 0) )

html_source="""
<!doctype>
<head>
	<link type="text/css" rel="stylesheet" href="css/graph.css">
	<link type="text/css" rel="stylesheet" href="css/detail.css">
	<link type="text/css" rel="stylesheet" href="css/legend.css">
	<link type="text/css" rel="stylesheet" href="css/lines.css">

	<script src="d3.v3.js"></script>

	<script src="rickshaw.js"></script>
  <style>
    #y_axis {
      position: absolute;
      top: 0;
      bottom: 0;
      width: 40px;
    }
  </style>
</head>
<body>

<div id="chart_container">
  <div id="y_axis"></div>
	<div id="chart"></div>
	<div id="legend_container">
		<div id="smoother" title="Smoothing"></div>
		<div id="legend"></div>
	</div>
	<div id="slider"></div>
</div>

<script>
// instantiate our graph!

var palette = new Rickshaw.Color.Palette( { scheme: 'colorwheel' } );

var graph = new Rickshaw.Graph( {
	element: document.getElementById("chart"),
	width: 960,
	height: 500,
	renderer: 'line',
	series: [
"""

for vendor in vendors:
  html_source = html_source + """
      {
        name: "%(name)s",
        data: %(list)s,
        color: palette.color(),
      }, 
  """ % {
    'name': vendor,
    'list': "[" + ", ".join([
      "{x: %d, y: %s}" % op for op in data_dict[vendor]
    ]) + "]"
  }

html_source = html_source + """
  ]
} );

var hoverDetail = new Rickshaw.Graph.HoverDetail( {
	graph: graph
} );

var legend = new Rickshaw.Graph.Legend( {
	graph: graph,
	element: document.getElementById('legend')

} );

var shelving = new Rickshaw.Graph.Behavior.Series.Toggle( {
	graph: graph,
	legend: legend
} );

var axes = new Rickshaw.Graph.Axis.Time( {
	graph: graph
} );
axes.render();

var y_ticks = new Rickshaw.Graph.Axis.Y( {
	graph: graph,
	orientation: 'left',
	tickFormat: Rickshaw.Fixtures.Number.formatKMBT,
	element: document.getElementById('y_axis'),
} );

graph.render();
</script>

</body>
"""
print html_source
