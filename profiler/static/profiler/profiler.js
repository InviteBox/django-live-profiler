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