$(function(){
  $('.query-collapse').each(
      function()
      {
	  var $t = $(this);
	  var text = $t.html();
          var spl = text.split(/((?:SELECT|INSERT|FROM|INTO|WHERE|JOIN))/);
          var result = '';
	  $t.html('');
	  var expand = function(){
	    $t.html(text);
	  };
	  for (var i=0,l=spl.length; i<l;i++){
	      $t.append(spl[i].substring(0,20));
	      if (spl[i].length > 20)
		  $t.append($('<a class="ellipsis" href="javascript:;">...</a>').click(expand));
	  }
      });
  $('.sortable').tablesorter();    
  }
);


var w = 960,
    h = 800,
    i = 0,
    barHeight = 20,
    barWidth = w * .8,
    duration = 400,
    root;

var tree = d3.layout.tree()
    .size([h, 100]);

var diagonal = d3.svg.diagonal()
    .projection(function(d) { return [d.y, d.x]; });

var vis = d3.select("#chart").append("svg:svg")
    .attr("width", w)
    .attr("height", h)
  .append("svg:g")
    .attr("transform", "translate(20,30)");


function update(source) {

  // Compute the flattened node list. TODO use d3.layout.hierarchy.
  var nodes = tree.nodes(root);
  
  // Compute the "layout".
  nodes.forEach(function(n, i) {
    n.x = i * barHeight;
  });
  
  // Update the nodes…
  var node = vis.selectAll("g.node")
      .data(nodes, function(d) { return d.id || (d.id = ++i); });
  
  var nodeEnter = node.enter().append("svg:g")
      .attr("class", "node")
      .attr("transform", function(d) { return "translate(" + source.y0 + "," + source.x0 + ")"; })
      .style("opacity", 1e-6);

  // Enter any new nodes at the parent's previous position.
  nodeEnter.append("svg:rect")
      .attr("y", -barHeight / 2)
      .attr("height", barHeight)
      .attr("width", barWidth)
      .style("fill",color)
      .on("click", click);
  
  nodeEnter.append("svg:text")
      .attr("dy", 3.5)
      .attr("dx", 5.5)
    .each(function(d){
	      d3.select(this)
		  .selectAll('tspan')
		  .data(wrapText(d.name))
		  .enter()
		  .append('svg:tspan')
		  .attr('x',0)
		  .attr('dy', 10)
		  .text(function(dd){return dd;});

	  });
//      .text(function(d) { return d.name; });



  
  // Transition nodes to their new position.
  nodeEnter.transition()
      .duration(duration)
      .attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; })
      .style("opacity", 1);
  
  node.transition()
      .duration(duration)
      .attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; })
      .style("opacity", 1)
    .select("rect")
      .style("fill", color);
  
  // Transition exiting nodes to the parent's new position.
  node.exit().transition()
      .duration(duration)
      .attr("transform", function(d) { return "translate(" + source.y + "," + source.x + ")"; })
      .style("opacity", 1e-6)
      .remove();
  
  // Update the links…
  var link = vis.selectAll("path.link")
      .data(tree.links(nodes), function(d) { return d.target.id; });
  
  // Enter any new links at the parent's previous position.
  link.enter().insert("svg:path", "g")
      .attr("class", "link")
      .attr("d", function(d) {
        var o = {x: source.x0, y: source.y0};
        return diagonal({source: o, target: o});
      })
    .transition()
      .duration(duration)
      .attr("d", diagonal);
  
  // Transition links to their new position.
  link.transition()
      .duration(duration)
      .attr("d", diagonal);
  
  // Transition exiting nodes to the parent's new position.
  link.exit().transition()
      .duration(duration)
      .attr("d", function(d) {
        var o = {x: source.x, y: source.y};
        return diagonal({source: o, target: o});
      })
      .remove();
  
  // Stash the old positions for transition.
  nodes.forEach(function(d) {
    d.x0 = d.x;
    d.y0 = d.y;
  });
}

// Toggle children on click.
function click(d) {
  if (d.children) {
    d._children = d.children;
    d.children = null;
  } else {
    d.children = d._children;
    d._children = null;
  }
  update(d);
}

function color(d) {
    if (typeof(d.normtime)!='undefined')
	return d3.hsl(d.normtime*120, 1.0, 0.5);
  return d._children ? "#3182bd" : d.children ? "#c6dbef" : "#fd8d3c";
}

function wrapText(text){
    var line='',lines = [],
    words = text.split(' '), wc=0;
    for (var i = 0, l=words.length; i<l; i++){
	line +=' '+words[i];
	wc++;
	if (wc==5) {
	    lines.push(line);
	    line='';
	    wc=0;	    
	}
    }
    lines.push(line);
    return lines;
}